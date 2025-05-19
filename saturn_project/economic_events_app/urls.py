from django.urls import path
from . import views

app_name = 'economic_events_app'

urlpatterns = [
    path('', views.import_calendar, name='import_calendar'),
]