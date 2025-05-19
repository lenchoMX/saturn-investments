# Instrucciones para la Implementación de `economic_events_app` por RootCode

## Requisitos Previos
- Acceso al repositorio del proyecto **Saturn Investments** en `/saturn_project`.
- Entorno virtual activado (`saturn`) con Python 3.11.9.
- Dependencias instaladas (`requirements/python.txt`).
- Base de datos PostgreSQL configurada con TimescaleDB.
- Conocimiento de Django, MQL5, y manejo de archivos CSV.

## Pasos Detallados de Implementación
### 1. Crear la App `economic_events_app`
- Ejecuta:
  ```bash
  python manage.py startapp economic_events_app
  ```
- Añade `'economic_events_app'` a `INSTALLED_APPS` en `settings.py`.

### 2. Definir el Modelo `EconomicEvent`
En `economic_events_app/models.py`:
```python
from django.db import models

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

    def __str__(self):
        return f"{self.event_name} ({self.country}) - {self.event_date}"
```

### 3. Crear y Aplicar Migraciones
- Ejecuta:
  ```bash
  python manage.py makemigrations economic_events_app
  python manage.py migrate
  ```

### 4. Implementar Vistas y Templates
#### Vista para Importar CSV
En `economic_events_app/views.py`:
```python
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import EconomicEvent

def import_calendar(request):
    if request.method == 'POST' and request.FILES.get('calendar_file'):
        file = request.FILES['calendar_file']
        fs = FileSystemStorage(location='output/raw_data/economic_events/')
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)

        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            EconomicEvent.objects.update_or_create(
                event_date=row['DateTime'],
                event_name=row['Event'],
                defaults={
                    'country': row['Currency'],
                    'impact': row['Impact'],
                    'actual': row['Actual'],
                    'forecast': row['Forecast'],
                    'previous': row['Previous'],
                }
            )
        return render(request, 'economic_events_app/success.html')
    return render(request, 'economic_events_app/import.html')
```

#### Templates
- **import.html**:
  ```html
  {% extends 'base.html' %}
  {% block content %}
  <form method="post" enctype="multipart/form-data">
      {% csrf_token %}
      <input type="file" name="calendar_file" accept=".csv" required>
      <button type="submit">Importar CSV</button>
  </form>
  {% endblock %}
  ```
- **success.html**:
  ```html
  {% extends 'base.html' %}
  {% block content %}
  <h1>Importación Exitosa</h1>
  <p>Los datos del calendario económico han sido importados correctamente.</p>
  {% endblock %}
  ```

### 5. Integrar con MetaTrader 5
- **Script MQL5 para Exportar CSV**:
  - En MetaEditor (MT5), crea un script que use `CalendarValueHistory` para obtener eventos y escribirlos en un CSV.
  - Ejemplo básico:
    ```mql5
    #include <Mql5/Calendar.mqh>
    void OnStart() {
       MqlCalendarValue values[];
       datetime from = D'2025.05.01';
       datetime to = D'2025.05.14';
       if(CalendarValueHistory(values, from, to)) {
          FileHandle handle = FileOpen("mt5_calendar.csv", FILE_WRITE|FILE_CSV);
          for(int i=0; i<ArraySize(values); i++) {
             string impact = (values[i].impact == 3) ? "High" : (values[i].impact == 2) ? "Medium" : "Low";
             FileWrite(handle, TimeToString(values[i].time), values[i].country, values[i].event_name, impact, values[i].actual, values[i].forecast, values[i].previous);
          }
          FileClose(handle);
       }
    }
    ```
  - Ejecuta el script en MT5 para generar `mt5_calendar.csv` en la carpeta `MQL5/Files`.

### 6. Pruebas
- **Importar CSV**:
  - Sube el CSV generado desde MT5 a través de `import.html`.
  - Verifica que los datos se inserten en `economic_events_app_economicevent` con:
    ```sql
    SELECT * FROM economic_events_app_economicevent;
    ```

## Notas
- Asegúrate de que el CSV tenga columnas como `DateTime`, `Currency`, `Event`, `Impact`, `Actual`, `Forecast`, `Previous`.
- El impacto debe mapearse a 'High', 'Medium', 'Low' en el script MQL5.
- Considera automatizar la generación y subida del CSV con tareas programadas (ej. Celery).
- Revisa los términos de uso de MT5 para asegurarte de que la exportación de datos sea permitida.