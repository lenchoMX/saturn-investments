import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import EconomicEvent
from core_app.models import SupportedMinute

def import_calendar(request):
    if request.method == 'POST' and request.FILES.get('calendar_file'):
        file = request.FILES['calendar_file']
        fs = FileSystemStorage(location='output/raw_data/economic_events/')
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        try:
            # Intentar leer el CSV con codificación UTF-8, si falla usar cp1252 para manejar caracteres extendidos
            try:
                df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='cp1252', on_bad_lines='skip')
            inserted_count = 0
            for index, row in df.iterrows():
                # Buscar o crear la minuta soportada basada en el nombre del evento
                supported_minute, created = SupportedMinute.objects.get_or_create(
                    name=row['Event'],
                    defaults={
                        'description': 'Imported from MetaTrader 5',
                        'impact': row['Impact'],
                        'country': row['Currency'],
                        'source': 'MetaTrader 5',
                        'frequency': 'Unknown',
                        'markets_affected': 'Forex',
                        'symbols_affected': row['Currency']
                    }
                )
                
                # Crear o actualizar el evento económico
                # Convertir el formato de fecha del CSV (YYYY.MM.DD HH:MM) a YYYY-MM-DD HH:MM
                date_str = row['DateTime']
                if date_str and isinstance(date_str, str):
                    try:
                        formatted_date = date_str.replace('.', '-')
                    except Exception as e:
                        formatted_date = None
                        print(f"Error al formatear fecha {date_str}: {e}")
                else:
                    formatted_date = None

                _, created = EconomicEvent.objects.update_or_create(
                    event_date=formatted_date if formatted_date else None,
                    event_name=row['Event'],
                    defaults={
                        'country': row['Currency'],
                        'impact': row['Impact'],
                        'actual': row['Actual'] if pd.notna(row['Actual']) else '',
                        'forecast': row['Forecast'] if pd.notna(row['Forecast']) else '',
                        'previous': row['Previous'] if pd.notna(row['Previous']) else '',
                        'source': row.get('Source', 'MetaTrader 5'),
                        'supported_minute': supported_minute,
                    }
                )
                if created:
                    inserted_count += 1
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'stats': {'inserted_rows': inserted_count}
                })
            return render(request, 'economic_events_app/success.html')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
            raise
    return render(request, 'economic_events_app/import.html')

import django_tables2 as tables
from django.db.models import Q

class EconomicEventTable(tables.Table):
    class Meta:
        model = EconomicEvent
        fields = ('event_date', 'country', 'event_name', 'impact', 'actual', 'forecast', 'previous')
        attrs = {'class': 'table table-striped'}

def economic_calendar(request):
    from datetime import datetime, timedelta
    
    # Obtener la fecha de hoy a las 00:00:00 y la fecha de dentro de 7 días
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    next_week = today + timedelta(days=7)
    
    events = EconomicEvent.objects.all().order_by('event_date')
    
    # Filtros
    currency = request.GET.get('currency')
    impact = request.GET.get('impact')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Si no se especifica un rango de fechas, mostrar eventos desde hoy hasta dentro de 7 días
    if not date_from and not date_to:
        events = events.filter(event_date__gte=today, event_date__lte=next_week)
        date_from = today.strftime('%Y-%m-%d')
        date_to = next_week.strftime('%Y-%m-%d')
    else:
        if date_from:
            events = events.filter(event_date__gte=date_from)
        if date_to:
            events = events.filter(event_date__lte=date_to)
    
    if currency:
        events = events.filter(country=currency)
    if impact:
        events = events.filter(impact=impact)
    
    # Calcular fechas para navegación por semanas
    if date_from and date_to:
        try:
            current_from = datetime.strptime(date_from, '%Y-%m-%d')
            current_to = datetime.strptime(date_to, '%Y-%m-%d')
            prev_from = current_from - timedelta(days=7)
            prev_to = current_to - timedelta(days=7)
            next_from = current_from + timedelta(days=7)
            next_to = current_to + timedelta(days=7)
            prev_from_str = prev_from.strftime('%Y-%m-%d')
            prev_to_str = prev_to.strftime('%Y-%m-%d')
            next_from_str = next_from.strftime('%Y-%m-%d')
            next_to_str = next_to.strftime('%Y-%m-%d')
        except ValueError:
            prev_from_str = prev_to_str = next_from_str = next_to_str = ""
    else:
        prev_from_str = prev_to_str = next_from_str = next_to_str = ""
    
    table = EconomicEventTable(events)
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'economic_events_app/economic_calendar.html', {
        'table': table,
        'date_from': date_from,
        'date_to': date_to,
        'currency': currency,
        'impact': impact,
        'prev_from': prev_from_str,
        'prev_to': prev_to_str,
        'next_from': next_from_str,
        'next_to': next_to_str
    })