from django.contrib import admin
from .models import SupportedEntity

@admin.register(SupportedEntity)
class SupportedEntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type', 'active', 'created_at')
    list_filter = ('entity_type', 'active')
    search_fields = ('name', 'description')
