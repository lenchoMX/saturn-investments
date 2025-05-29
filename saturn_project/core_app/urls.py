from django.urls import path
from . import views

app_name = 'core_app'

urlpatterns = [
    path('supported-entities/', views.supported_entities, name='supported_entities_index'),
    path('supported-minutes/', views.supported_minutes_index, name='supported_minutes'),
    path('symbols/', views.symbols_list, name='symbols_list'),
    path('symbols/<str:symbol>/minutes/', views.minutes_by_symbol, name='minutes_by_symbol'),
    path('minutes/<int:minute_id>/events/', views.events_by_minute, name='events_by_minute'),
    path('export-data/', views.export_data, name='export_data'),
]