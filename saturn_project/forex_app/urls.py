from django.urls import path
from . import views

app_name = 'forex_app'
urlpatterns = [
    path('', views.index, name='forex_index'),
    path('import/', views.import_data, name='forex_import'),
    path('analysis/', views.analysis, name='forex_analysis'),
    path('viz/', views.visualization, name='forex_viz'),
]