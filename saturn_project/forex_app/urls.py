from django.urls import path
from . import views

app_name = 'forex_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('import/', views.import_data, name='import'),
    path('analysis/', views.analysis, name='analysis'),
    path('viz/', views.visualization, name='viz'),
]