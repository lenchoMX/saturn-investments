# Instrucciones para la Implementación del Índice de Minutas Soportadas por RootCode

## Introducción
Este documento proporciona instrucciones detalladas para implementar un índice de minutas financieras soportadas en el proyecto **Saturn Investments**. El índice se almacenará en un modelo `SupportedMinute` en `core_app`, y se integrará con `EconomicEvent` en `economic_events_app` para mapear eventos importados desde MetaTrader 5. Además, se configurará una vista para visualizar el índice y se habilitará la gestión mediante el admin de Django.

## Objetivos
- Crear el modelo `SupportedMinute` en `core_app` para almacenar minutas soportadas con campos como nombre, descripción, impacto, país, fuente, frecuencia, mercados afectados y símbolos afectados.
- Relacionar `EconomicEvent` con `SupportedMinute` para mapear eventos a minutas soportadas.
- Poblar el índice con datos iniciales (ej. minutas de FOMC, ECB, BoE).
- Crear una vista y template para visualizar el índice.
- Configurar el admin de Django para gestionar las minutas.

## Requisitos Previos
- **Entorno**: Proyecto Django `saturn_project` con estructura modular (`core_app`, `economic_events_app`, `forex_app`, etc.).
- **Base de datos**: PostgreSQL con TimescaleDB habilitado.
- **Dependencias**: Django, pandas, psycopg2 (instaladas en `requirements/python.txt`).
- **Estado actual**:
  - `core_app` existe y contiene modelos como `SupportedEntity`.
  - `economic_events_app` existe con el modelo `EconomicEvent` y vistas para importar datos desde CSV (generados por MetaTrader 5).
- **Acceso**: Repositorio del proyecto y entorno virtual activado (`saturn`).

## Pasos de Implementación

### 1. Crear el Modelo `SupportedMinute` en `core_app`
1. **Abrir `core_app/models.py`** y añadir el siguiente modelo:
   ```python
   from django.db import models

   class SupportedMinute(models.Model):
       IMPACT_CHOICES = [
           ('High', 'High'),
           ('Medium', 'Medium'),
           ('Low', 'Low'),
       ]

       name = models.CharField(max_length=100, unique=True)  # Ej. "FOMC Minutes"
       description = models.TextField()  # Ej. "Discusión sobre tasas de interés en EE. UU."
       impact = models.CharField(max_length=20, choices=IMPACT_CHOICES, default='High')  # Impacto esperado
       country = models.CharField(max_length=50)  # Ej. "United States"
       source = models.CharField(max_length=100)  # Ej. "Federal Reserve"
       frequency = models.CharField(max_length=50)  # Ej. "Every 6 weeks"
       markets_affected = models.CharField(max_length=200)  # Ej. "Forex, Equities"
       symbols_affected = models.CharField(max_length=200)  # Ej. "EUR/USD, USD/JPY"

       def __str__(self):
           return f"{self.name} ({self.country})"
   ```

2. **Generar y aplicar migraciones**:
   ```bash
   python manage.py makemigrations core_app
   python manage.py migrate
   ```
   - Esto creará la tabla `core_app_supportedminute` en la base de datos.

### 2. Relacionar `EconomicEvent` con `SupportedMinute`
1. **Modificar `economic_events_app/models.py`** para añadir una relación con `SupportedMinute`:
   ```python
   from django.db import models
   from core_app.models import SupportedMinute

   class EconomicEvent(models.Model):
       IMPACT_CHOICES = [
           ('High', 'High'),
           ('Medium', 'Medium'),
           ('Low', 'Low'),
       ]
       event_date = models.DateTimeField()
       country = models.CharField(max_length=50)
       event_name = models.CharField(max_length=255)
       impact = models.CharField(max_length=20, choices=IMPACT_CHOICES)
       actual = models.CharField(max_length=50, blank=True, null=True)
       forecast = models.CharField(max_length=50, blank=True, null=True)
       previous = models.CharField(max_length=50, blank=True, null=True)
       source = models.CharField(max_length=100, default='MetaTrader 5')
       supported_minute = models.ForeignKey(SupportedMinute, on_delete=models.SET_NULL, null=True, blank=True)

       def __str__(self):
           return f"{self.event_name} ({self.country}) - {self.event_date}"
   ```

2. **Generar y aplicar migraciones**:
   ```bash
   python manage.py makemigrations economic_events_app
   python manage.py migrate
   ```

### 3. Poblar el Índice de Minutas
1. **Crear un script para poblar `SupportedMinute`**:
   - Crea el archivo `core_app/populate_minutes.py` con el siguiente contenido:
     ```python
     from core_app.models import SupportedMinute

     def populate_supported_minutes():
         minutes_data = [
             {
                 'name': 'FOMC Minutes',
                 'description': 'Minutas de las reuniones del Comité Federal de Mercado Abierto, discutiendo tasas de interés y política monetaria.',
                 'impact': 'High',
                 'country': 'United States',
                 'source': 'Federal Reserve',
                 'frequency': 'Every 6 weeks',
                 'markets_affected': 'Forex, Equities, Commodities',
                 'symbols_affected': 'EUR/USD, USD/JPY, S&P 500',
             },
             {
                 'name': 'ECB Minutes',
                 'description': 'Minutas de las reuniones del Banco Central Europeo, incluyendo decisiones de política monetaria.',
                 'impact': 'High',
                 'country': 'Eurozone',
                 'source': 'European Central Bank',
                 'frequency': 'Every 4 weeks',
                 'markets_affected': 'Forex, Equities',
                 'symbols_affected': 'EUR/USD, EUR/GBP',
             },
             {
                 'name': 'BoE Minutes',
                 'description': 'Minutas del Comité de Política Monetaria del Banco de Inglaterra.',
                 'impact': 'High',
                 'country': 'United Kingdom',
                 'source': 'Bank of England',
                 'frequency': 'Monthly',
                 'markets_affected': 'Forex, Equities',
                 'symbols_affected': 'GBP/USD, GBP/EUR',
             },
             {
                 'name': 'BoJ Minutes',
                 'description': 'Minutas de las reuniones de política monetaria del Banco de Japón.',
                 'impact': 'High',
                 'country': 'Japan',
                 'source': 'Bank of Japan',
                 'frequency': 'Monthly',
                 'markets_affected': 'Forex, Equities',
                 'symbols_affected': 'USD/JPY, EUR/JPY',
             },
             {
                 'name': 'Banxico Minutes',
                 'description': 'Minutas de las reuniones de política monetaria del Banco de México.',
                 'impact': 'Medium',
                 'country': 'Mexico',
                 'source': 'Banco de México',
                 'frequency': 'Every 6 weeks',
                 'markets_affected': 'Forex',
                 'symbols_affected': 'USD/MXN, EUR/MXN',
             },
         ]

         for data in minutes_data:
             SupportedMinute.objects.update_or_create(
                 name=data['name'],
                 defaults=data
             )

     if __name__ == "__main__":
         populate_supported_minutes()
     ```

2. **Ejecutar el script**:
   ```bash
   python manage.py shell < core_app/populate_minutes.py
   ```

3. **Verificar los datos**:
   - Usa el siguiente comando SQL para confirmar que las minutas se insertaron:
     ```sql
     SELECT * FROM core_app_supportedminute;
     ```

### 4. Actualizar la Vista de Importación para Mapear Eventos
1. **Modificar `economic_events_app/views.py`** para mapear eventos a minutas soportadas durante la importación:
   ```python
   import pandas as pd
   from django.shortcuts import render
   from django.core.files.storage import FileSystemStorage
   from .models import EconomicEvent
   from core_app.models import SupportedMinute

   def import_calendar(request):
       if request.method == 'POST' and request.FILES.get('calendar_file'):
           file = request.FILES['calendar_file']
           fs = FileSystemStorage(location='output/raw_data/economic_events/')
           filename = fs.save(file.name, file)
           file_path = fs.path(filename)

           df = pd.read_csv(file_path)
           for index, row in df.iterrows():
               # Buscar una minuta soportada que coincida con el nombre del evento
               supported_minute = SupportedMinute.objects.filter(name=row['Event']).first()
               
               EconomicEvent.objects.update_or_create(
                   event_date=row['DateTime'],
                   event_name=row['Event'],
                   defaults={
                       'country': row['Currency'],
                       'impact': row['Impact'],
                       'actual': row['Actual'],
                       'forecast': row['Forecast'],
                       'previous': row['Previous'],
                       'source': row.get('Source', 'MetaTrader 5'),
                       'supported_minute': supported_minute,
                   }
               )
           return render(request, 'economic_events_app/success.html')
       return render(request, 'economic_events_app/import.html')
   ```

### 5. Crear una Vista para Visualizar el Índice
1. **Añadir una vista en `core_app/views.py`**:
   ```python
   from django.shortcuts import render
   from .models import SupportedMinute

   def supported_minutes_index(request):
       minutes = SupportedMinute.objects.all().order_by('name')
       return render(request, 'core_app/supported_minutes.html', {'minutes': minutes})
   ```

2. **Crear el template `core_app/templates/core_app/supported_minutes.html`**:
   - Asegúrate de que la carpeta `core_app/templates/core_app` exista.
   - Añade el siguiente contenido:
     ```html
     {% extends 'base.html' %}
     {% block content %}
     <h1>Índice de Minutas Soportadas</h1>
     <table border="1">
         <thead>
             <tr>
                 <th>Nombre</th>
                 <th>Descripción</th>
                 <th>Impacto</th>
                 <th>País</th>
                 <th>Fuente</th>
                 <th>Frecuencia</th>
                 <th>Mercados Afectados</th>
                 <th>Símbolos Afectados</th>
             </tr>
         </thead>
         <tbody>
             {% for minute in minutes %}
             <tr>
                 <td>{{ minute.name }}</td>
                 <td>{{ minute.description }}</td>
                 <td>{{ minute.impact }}</td>
                 <td>{{ minute.country }}</td>
                 <td>{{ minute.source }}</td>
                 <td>{{ minute.frequency }}</td>
                 <td>{{ minute.markets_affected }}</td>
                 <td>{{ minute.symbols_affected }}</td>
             </tr>
             {% endfor %}
         </tbody>
     </table>
     {% endblock %}
     ```

3. **Configurar URLs**:
   - En `core_app/urls.py`, crea o actualiza el archivo con:
     ```python
     from django.urls import path
     from . import views

     urlpatterns = [
         path('supported-minutes/', views.supported_minutes_index, name='supported_minutes'),
     ]
     ```
   - Asegúrate de que las URLs de `core_app` estén incluidas en `saturn_project/urls.py`:
     ```python
     from django.urls import path, include

     urlpatterns = [
         path('core/', include('core_app.urls')),
         # Otras URLs...
     ]
     ```

### 6. Configurar el Admin de Django
1. **Registrar `SupportedMinute` en `core_app/admin.py`**:
   ```python
   from django.contrib import admin
   from .models import SupportedMinute

   admin.site.register(SupportedMinute)
   ```

2. **Acceder al Admin**:
   - Asegúrate de que un superusuario esté creado:
     ```bash
     python manage.py createsuperuser
     ```
   - Inicia el servidor de desarrollo:
     ```bash
     python manage.py runserver
     ```
   - Accede a `/admin` (ej. `http://localhost:8000/admin`) y verifica que `SupportedMinute` esté disponible para gestionar.

### 7. Pruebas
1. **Verificar la Población de Datos**:
   - Después de ejecutar el script `populate_minutes.py`, asegúrate de que las minutas estén en la base de datos:
     ```sql
     SELECT * FROM core_app_supportedminute;
     ```
   - Deberías ver las minutas como "FOMC Minutes", "ECB Minutes", etc.

2. **Probar la Importación de Eventos**:
   - Usa el EA `calendar_ea.mq5` para generar un CSV desde MetaTrader 5.
   - Sube el CSV a través de la vista `import_calendar` en `economic_events_app`.
   - Verifica que los eventos se asocien correctamente con `SupportedMinute`:
     ```sql
     SELECT ee.event_name, ee.event_date, sm.name AS minute_name
     FROM economic_events_app_economicevent ee
     LEFT JOIN core_app_supportedminute sm ON ee.supported_minute_id = sm.id;
     ```

3. **Probar la Vista del Índice**:
   - Navega a `http://localhost:8000/core/supported-minutes/` y verifica que la tabla muestre todas las minutas soportadas.

4. **Probar el Admin**:
   - En `/admin`, añade una nueva minuta (ej. "RBA Minutes" para el Reserve Bank of Australia) y verifica que se guarde correctamente.

## Notas Adicionales
- **Mantenimiento**: Usa el admin de Django para añadir o modificar minutas según sea necesario.
- **Escalabilidad**: Si necesitas más campos en `SupportedMinute` (ej. `url` para el enlace oficial de la minuta), añádelos al modelo y actualiza las migraciones.
- **Integración con Datos Históricos**: Usa el campo `symbols_affected` para correlacionar minutas con datos de `historical_data` (ej. analizar el impacto de "FOMC Minutes" en EUR/USD).
- **Automatización**: Considera usar una API como Trading Economics en el futuro para actualizar automáticamente el índice de minutas soportadas.
- **Seguridad**: Asegúrate de que `/admin` esté protegido con un usuario y contraseña seguros.

## Conclusión
Esta implementación crea un índice de minutas soportadas en `core_app`, lo integra con `economic_events_app`, y permite visualizar y gestionar las minutas a través de una vista pública y el admin de Django. Los pasos son claros y aseguran que el índice sea funcional y mantenible.

Si hay problemas durante la implementación o necesitas ajustes, contacta al equipo de soporte o revisa la documentación del proyecto en `/docs`. 🚀 (Fecha y hora de creación: 11:47 AM CST, 14 de mayo de 2025).