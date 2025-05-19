from django.shortcuts import render
from .models import SupportedEntity, SupportedMinute

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
