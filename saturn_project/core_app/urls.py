from django.urls import path
from . import views

app_name = 'core_app'

urlpatterns = [
    path('supported-entities/', views.supported_entities, name='supported_entities_index'),
    path('supported-minutes/', views.supported_minutes_index, name='supported_minutes'),
]