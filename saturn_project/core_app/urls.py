from django.urls import path
from . import views

app_name = 'core_app'
urlpatterns = [
    path('supported-entities/', views.supported_entities, name='supported_entities_index'),
]