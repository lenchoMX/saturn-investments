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
            df = pd.read_csv(file_path)
            inserted_count = 0
            for index, row in df.iterrows():
                # Buscar una minuta soportada que coincida con el nombre del evento
                supported_minute = SupportedMinute.objects.filter(name=row['Event']).first()
                
                _, created = EconomicEvent.objects.update_or_create(
                    event_date=row['DateTime'],
                    event_name=row['Event'],
                    defaults={
                        'country': row['Currency'],
                        'impact': row['Impact'],
                        'actual': row['Actual'],
                        'forecast': row['Forecast'],
                        'previous': row['Previous'],
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