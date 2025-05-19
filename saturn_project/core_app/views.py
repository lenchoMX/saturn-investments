from django.shortcuts import render
from .models import SupportedEntity, SupportedMinute
from economic_events_app.models import EconomicEvent

def supported_entities(request):
    entities = SupportedEntity.objects.all()
    context = {
        'entities': entities,
        'entity_types': SupportedEntity.ENTITY_TYPES,
    }
    return render(request, 'core_app/supported_entities.html', context)

def supported_minutes_index(request):
    minutes = SupportedMinute.objects.all().order_by('name')
    return render(request, 'core_app/supported_minutes.html', {'minutes': minutes})

# Listar símbolos disponibles
def symbols_list(request):
    symbols = SupportedMinute.objects.values_list('symbols_affected', flat=True).distinct()
    return render(request, 'core_app/symbols_list.html', {'symbols': symbols})

# Listar minutas por símbolo
def minutes_by_symbol(request, symbol):
    minutes = SupportedMinute.objects.filter(symbols_affected__contains=symbol)
    return render(request, 'core_app/minutes_by_symbol.html', {'minutes': minutes, 'symbol': symbol})

# Mostrar histórico de eventos por minuta
def events_by_minute(request, minute_id):
    minute = SupportedMinute.objects.get(id=minute_id)
    events = EconomicEvent.objects.filter(supported_minute=minute).order_by('-event_date')
    return render(request, 'core_app/events_by_minute.html', {'minute': minute, 'events': events})
