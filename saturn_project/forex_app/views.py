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
from core_app.models import SupportedEntity  # Importar el modelo

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
                files = request.FILES.getlist('file')  # Obtener lista de archivos
                currency_pair_symbol = request.POST.get('currency_pair')  # Obtener el symbol seleccionado
                logging.info(f"Archivos subidos: {[f.name for f in files]}")

                # Verificar que se haya seleccionado un par
                if not currency_pair_symbol:
                    messages.error(request, 'Debe seleccionar un par de divisas.')
                    return render(request, 'forex_app/import.html', {
                        'form': form,
                        'currency_pairs': SupportedEntity.objects.filter(entity_type='currency_pair', active=True).order_by('name'),
                        'title': 'Importar Datos Forex'
                    })

                # Verificar si el símbolo es válido
                if not SupportedEntity.objects.filter(symbol=currency_pair_symbol, entity_type='currency_pair', active=True).exists():
                    messages.error(request, 'El par de divisas seleccionado no es válido o no está soportado.')
                    return render(request, 'forex_app/import.html', {
                        'form': form,
                        'currency_pairs': SupportedEntity.objects.filter(entity_type='currency_pair', active=True).order_by('name'),
                        'title': 'Importar Datos Forex'
                    })

                symbol = currency_pair_symbol  # Usar el símbolo seleccionado

                # Cargar configuración de zonas horarias
                try:
                    with open('config/timezones.json', 'r') as f:
                        timezone_config = json.load(f)
                except FileNotFoundError:
                    timezone_config = {'HistData.com': 'UTC'}
                    messages.warning(request, 'Archivo timezones.json no encontrado. Usando UTC por defecto.')

                # Procesar cada archivo
                overall_stats = {'total_files': len(files), 'total_rows': 0, 'valid_rows': 0, 'inserted_rows': 0, 'errors': []}
                batch_size = 10000
                tz = pytz.timezone(timezone_config.get('HistData.com', 'UTC'))

                # Limpiar tabla temporal una sola vez antes de procesar todos los archivos
                TempHistoricalData.objects.all().delete()
                logging.info("Tabla temp_historical_data limpiada.")

                for file in files:
                    file_stats = {'file_name': file.name, 'total_rows': 0, 'valid_rows': 0, 'inserted_rows': 0, 'errors': []}
                    logging.info(f"Procesando archivo: {file.name}")

                    # Guardar archivo en /output/raw_data/forex/
                    fs = FileSystemStorage(location='output/raw_data/forex/')
                    filename = fs.save(file.name, file)
                    file_path = fs.path(filename)

                    # Leer CSV
                    with open(file_path, 'r', encoding='utf-8') as csv_file:
                        reader = csv.reader(csv_file)
                        next(reader, None)  # Saltar encabezado si existe
                        batch = []

                        for row in reader:
                            file_stats['total_rows'] += 1
                            overall_stats['total_rows'] += 1
                            if len(row) < 7:
                                error_msg = f"Fila {file_stats['total_rows']} en {file.name}: Formato inválido, menos de 7 columnas"
                                file_stats['errors'].append(error_msg)
                                overall_stats['errors'].append(error_msg)
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
                                file_stats['valid_rows'] += 1
                                overall_stats['valid_rows'] += 1

                                # Insertar lote
                                if len(batch) >= batch_size:
                                    TempHistoricalData.objects.bulk_create(batch)
                                    batch = []
                                    logging.info(f"Insertado lote de {batch_size} filas en temp_historical_data desde {file.name}")

                            except (ValueError, KeyError) as e:
                                error_msg = f"Fila {file_stats['total_rows']} en {file.name}: {str(e)}"
                                file_stats['errors'].append(error_msg)
                                overall_stats['errors'].append(error_msg)
                                logging.error(f"Error en fila {file_stats['total_rows']} de {file.name}: {str(e)}")

                        # Insertar lote final para este archivo
                        if batch:
                            TempHistoricalData.objects.bulk_create(batch)
                            logging.info(f"Insertado lote final de {len(batch)} filas en temp_historical_data desde {file.name}")

                    # Borrar archivo temporal después de procesarlo
                    os.remove(file_path)
                    file_stats['inserted_rows'] = file_stats['valid_rows']

                # Transferir todos los datos de la tabla temporal a historical_data después de procesar todos los archivos
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

                overall_stats['inserted_rows'] = overall_stats['valid_rows']
                TempHistoricalData.objects.all().delete()
                logging.info("Tabla temp_historical_data limpiada tras transferencia.")

                # Guardar informe, asegurándose de que los directorios existan
                os.makedirs('output/reports', exist_ok=True)
                with open('output/reports/import_report.txt', 'a') as f:
                    f.write(f"Importación {datetime.now()}: {overall_stats}\n")

                # Respuesta
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'progress': 100,
                        'message': 'Importación completada con éxito.',
                        'stats': overall_stats
                    })
                messages.success(request, 'Importación completada con éxito.')
                return render(request, 'forex_app/success.html', {
                    'title': 'Importación Completada',
                    'stats': overall_stats
                })

            else:
                errors = form.errors.as_json()
                logging.info(f"Errores del formulario: {errors}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': f'Formulario inválido: {errors}'})
                messages.error(request, f'Formulario inválido: {errors}')
        else:
            form = ImportFileForm()
            currency_pairs = SupportedEntity.objects.filter(
                entity_type='currency_pair',
                active=True
            ).order_by('name')

        return render(request, 'forex_app/import.html', {
            'form': form,
            'currency_pairs': currency_pairs,
            'title': 'Importar Datos Forex'
        })

    except ProgrammingError as e:
        logging.error(f"Error de base de datos en import_data: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f'Error de base de datos: {str(e)}'})
        messages.error(request, f'Error de base de datos: {str(e)}')
        return render(request, 'forex_app/import.html', {
            'form': ImportFileForm(),
            'currency_pairs': SupportedEntity.objects.filter(entity_type='currency_pair', active=True).order_by('name'),
            'title': 'Importar Datos Forex'
        })
    except Exception as e:
        logging.error(f"Error inesperado en import_data: {str(e)}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': f'Error en el servidor: {str(e)}'})
        messages.error(request, f'Error en el servidor: {str(e)}')
        return render(request, 'forex_app/import.html', {
            'form': ImportFileForm(),
            'currency_pairs': SupportedEntity.objects.filter(entity_type='currency_pair', active=True).order_by('name'),
            'title': 'Importar Datos Forex'
        })

def analysis(request):
    return render(request, 'forex_app/analysis.html', {'title': 'Análisis Forex'})

def visualization(request):
    return render(request, 'forex_app/viz.html', {'title': 'Visualización Forex'})