from django.shortcuts import render
from .models import SupportedEntity

def supported_entities(request):
    entities = SupportedEntity.objects.all()
    context = {
        'entities': entities,
        'entity_types': SupportedEntity.ENTITY_TYPES,
    }
    return render(request, 'core_app/supported_entities.html', context)
