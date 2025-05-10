from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import csv
import os
import re
import json
import logging
from datetime import datetime
import pytz
from django.db.utils import ProgrammingError
from .forms import ImportFileForm
from .models import HistoricalData, TempHistoricalData

# Configurar logging
logging.basicConfig(
    filename='output/logs/import.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def index(request):
    return render(request, 'forex_app/index.html', {'title': 'Forex Market'})

def import_data(request):
    try:
        if request.method == 'POST':
            logging.info(f"request.FILES: {request.FILES}")
            form = ImportFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                logging.info(f"Archivo subido: {file.name}")
                # Extraer símbolo del nombre del archivo (ej. DAT_MT_USDMXN_M1_2010.csv)
                match = re.match(r'DAT_MT_(\w+)_M1_\d{4}\.csv', file.name)
                symbol = match.group(1) if match else 'UNKNOWN'

                # Guardar archivo en /output/raw_data/forex/
                fs = FileSystemStorage(location='output/raw_data/forex/')
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)

                # Cargar configuración de zonas horarias
                try:
                    with open('config/timezones.json', 'r') as f:
                        timezone_config = json.load(f)
                except FileNotFoundError:
                    timezone_config = {'HistData.com': 'UTC'}
                    messages.warning(request, 'Archivo timezones.json no encontrado. Usando UTC por defecto.')

                # Procesar CSV
                stats = {'total_rows': 0, 'valid_rows': 0, 'inserted_rows': 0, 'errors': []}
                batch_size = 10000
                tz = pytz.timezone(timezone_config.get('HistData.com', 'UTC'))

                # Limpiar tabla temporal
                TempHistoricalData.objects.all().delete()
                logging.info("Tabla temp_historical_data limpiada.")

                # Leer CSV
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader, None)  # Saltar encabezado si existe
                    batch = []

                    for row in reader:
                        stats['total_rows'] += 1
                        if len(row) < 7:
                            stats['errors'].append(f"Fila {stats['total_rows']}: Formato inválido, menos de 7 columnas")
                            continue

                        try:
                            # Parsear fecha y hora (formato: 2010.11.14,17:05)
                            date_str = f"{row[0]},{row[1]}"
                            dt = datetime.strptime(date_str, '%Y.%m.%d,%H:%M')
                            dt = tz.localize(dt).astimezone(pytz.UTC)

                            # Crear registro temporal
                            record = TempHistoricalData(
                                timestamp=dt,
                                symbol=symbol,
                                open_price=float(row[2]) if row[2] else None,
                                high_price=float(row[3]) if row[3] else None,
                                low_price=float(row[4]) if row[4] else None,
                                close_price=float(row[5]) if row[5] else None,
                                volume=int(row[6]) if row[6] else None
                            )
                            batch.append(record)
                            stats['valid_rows'] += 1

                            # Insertar lote
                            if len(batch) >= batch_size:
                                TempHistoricalData.objects.bulk_create(batch)
                                # TempHistoricalData.objects.bulk_create(records, ignore_conflicts=True)
                                batch = []
                                logging.info(f"Insertado lote de {batch_size} filas en temp_historical_data")

                        except (ValueError, KeyError) as e:
                            stats['errors'].append(f"Fila {stats['total_rows']}: {str(e)}")
                            logging.error(f"Error en fila {stats['total_rows']}: {str(e)}")

                    # Insertar lote final
                    if batch:
                        TempHistoricalData.objects.bulk_create(batch)
                        logging.info(f"Insertado lote final de {len(batch)} filas en temp_historical_data")

                # Transferir a historical_data
                batch = []
                for temp_data in TempHistoricalData.objects.all().iterator():
                    batch.append(HistoricalData(
                        timestamp=temp_data.timestamp,
                        symbol=temp_data.symbol,
                        market=temp_data.market,
                        open_price=temp_data.open_price,
                        high_price=temp_data.high_price,
                        low_price=temp_data.low_price,
                        close_price=temp_data.close_price,
                        volume=temp_data.volume,
                        data_source=temp_data.data_source,
                        timeframe=temp_data.timeframe
                    ))
                    if len(batch) >= batch_size:
                        HistoricalData.objects.bulk_create(batch)
                        batch = []
                        logging.info(f"Transferido lote de {batch_size} filas a historical_data")

                if batch:
                    HistoricalData.objects.bulk_create(batch)
                    logging.info(f"Transferido lote final de {len(batch)} filas a historical_data")

                stats['inserted_rows'] = stats['valid_rows']
                TempHistoricalData.objects.all().delete()
                logging.info("Tabla temp_historical_data limpiada tras transferencia.")

                # Guardar informe
                with open('output/reports/import_report.txt', 'a') as f:
                    f.write(f"Importación {datetime.now()}: {stats}\n")

                # Borrar archivo temporal
                os.remove(file_path)

                # Respuesta
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'progress': 100,
                        'message': 'Importación completada con éxito.',
                        'stats': stats
                    })
                messages.success(request, 'Importación completada con éxito.')
                return render(request, 'forex_app/success.html', {
                    'title': 'Importación Completada',
                    'stats': stats
                })

            else:
                errors = form.errors.as_json()
                logging.info(f"Errores del formulario: {errors}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': f'Formulario inválido: {errors}'})
                messages.error(request, f'Formulario inválido: {errors}')
        else:
            form = ImportFileForm()

        return render(request, 'forex_app/import.html', {'form': form, 'title': 'Importar Datos Forex'})

    except ProgrammingError as e:
        logging.error(f"Error de base de datos en import_data: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f'Error de base de datos: {str(e)}'})
        messages.error(request, f'Error de base de datos: {str(e)}')
        return render(request, 'forex_app/import.html', {'form': ImportFileForm(), 'title': 'Importar Datos Forex'})
    except Exception as e:
        logging.error(f"Error inesperado en import_data: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f'Error en el servidor: {str(e)}'})
        messages.error(request, f'Error en el servidor: {str(e)}')
        return render(request, 'forex_app/import.html', {'form': ImportFileForm(), 'title': 'Importar Datos Forex'})

def analysis(request):
    return render(request, 'forex_app/analysis.html', {'title': 'Análisis Forex'})

def visualization(request):
    return render(request, 'forex_app/viz.html', {'title': 'Visualización Forex'})