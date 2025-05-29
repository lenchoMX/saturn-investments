# Instrucciones para la Implementación de Importación y Filtrado de Minutas en Saturn Investments

## Introducción
Este documento extiende las instrucciones de `IMPLEMENTATION_MINUTES_ROOTCODE.md` para agregar funcionalidad de importación avanzada de minutas financieras y una interfaz de filtrado y visualización en el proyecto **Saturn Investments**. Se usará el modelo `SupportedMinute` en `core_app` para almacenar minutas soportadas y se integrará con `EconomicEvent` en `economic_events_app` para asociar eventos importados desde MetaTrader 5. Además, se implementará una interfaz para filtrar minutas por símbolo y mostrar su histórico de eventos.

## Objetivos
- Mejorar la importación de minutas desde un CSV de MetaTrader 5, asegurando que las minutas se busquen en la tabla `SupportedMinute` y, si no existen, se creen (similar a `firstOrCreate` en Laravel).
- Crear vistas y templates para permitir al usuario:
  - Seleccionar un símbolo (ej. EUR/USD).
  - Ver un listado de minutas soportadas relacionadas con ese símbolo (ej. "FOMC Minutes" si afecta a USD).
  - Mostrar el histórico de eventos de una minuta seleccionada.
- Mantener la estructura modular del proyecto y aprovechar las tablas existentes en la base de datos.

## Requisitos Previos
- **Entorno**: Proyecto Django `saturn_project` con `core_app` y `economic_events_app` configurados según `IMPLEMENTATION_MINUTES_ROOTCODE.md`.
- **Base de datos**: PostgreSQL con TimescaleDB habilitado y las tablas `core_app_supportedminute` y `economic_events_app_economicevent` creadas.
- **Dependencias**: Django, pandas, psycopg2 (instaladas en `requirements/python.txt`).
- **Estado actual**:
  - Modelo `SupportedMinute` en `core_app` con campos como `name`, `symbols_affected`, etc.
  - Modelo `EconomicEvent` en `economic_events_app` relacionado con `SupportedMinute`.
  - Vista `import_calendar` en `economic_events_app` para importar eventos desde CSV.

## Pasos de Implementación

### 1. Mejorar la Lógica de Importación de Minutas
**Objetivo**: Durante la importación de eventos desde un CSV, buscar o crear minutas en `SupportedMinute` para evitar duplicados y asociar eventos correctamente.

1. **Modificar `economic_events_app/views.py`**:
   - Actualiza la vista `import_calendar` para usar `get_or_create` en `SupportedMinute`:
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
                 # Buscar o crear la minuta soportada basada en el nombre del evento
                 supported_minute, created = SupportedMinute.objects.get_or_create(
                     name=row['Event'],
                     defaults={
                         'description': 'Imported from MetaTrader 5',
                         'impact': row['Impact'],
                         'country': row['Currency'],
                         'source': 'MetaTrader 5',
                         'frequency': 'Unknown',
                         'markets_affected': 'Forex',
                         'symbols_affected': row['Currency']
                     }
                 )
                 
                 # Crear o actualizar el evento económico
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
   - **Notas**:
     - Los valores por defecto en `get_or_create` (como `'description'` o `'frequency'`) son placeholders. Ajusta según los datos disponibles en el CSV o las necesidades del proyecto.
     - `symbols_affected` usa `row['Currency']` como base, pero podrías mejorarlo si el CSV incluye más detalles.

2. **Probar la Importación**:
   - Genera un CSV con el EA `calendar_ea.mq5` en MetaTrader 5.
   - Súbelo a través de la vista `import_calendar`.
   - Verifica en la base de datos que las minutas se crean solo si no existen:
     ```sql
     SELECT * FROM core_app_supportedminute;
     SELECT ee.event_name, sm.name AS minute_name 
     FROM economic_events_app_economicevent ee
     JOIN core_app_supportedminute sm ON ee.supported_minute_id = sm.id;
     ```

### 2. Implementar Vistas para Filtrado y Visualización
**Objetivo**: Crear una interfaz donde el usuario seleccione un símbolo, vea las minutas relacionadas y luego consulte el histórico de eventos de una minuta específica.

1. **Añadir Vistas en `core_app/views.py`**:
   ```python
   from django.shortcuts import render
   from .models import SupportedMinute
   from economic_events_app.models import EconomicEvent

   # Listar símbolos disponibles
   def symbols_list(request):
       symbols = SupportedMinute.objects.values_list('symbols_affected', flat=True).distinct()
       return render(request, 'core_app/symbols_list.html', {'symbols': symbols})

   # Listar minutas por símbolo
   def minutes_by_symbol(request, symbol):
       minutes = SupportedMinute.objects.filter(symbols_affected__contains=symbol)
       return render(request, 'core_app/minutes_by_symbol.html', {'minutes': minutes, 'symbol': symbol})

   # Mostrar histórico de eventos por minuta
   def events_by_minute(request, minute_id):
       minute = SupportedMinute.objects.get(id=minute_id)
       events = EconomicEvent.objects.filter(supported_minute=minute).order_by('-event_date')
       return render(request, 'core_app/events_by_minute.html', {'minute': minute, 'events': events})
   ```

2. **Configurar URLs en `core_app/urls.py`**:
   - Crea o actualiza el archivo con:
     ```python
     from django.urls import path
     from . import views

     urlpatterns = [
         path('symbols/', views.symbols_list, name='symbols_list'),
         path('symbols/<str:symbol>/minutes/', views.minutes_by_symbol, name='minutes_by_symbol'),
         path('minutes/<int:minute_id>/events/', views.events_by_minute, name='events_by_minute'),
     ]
     ```
   - Asegúrate de que las URLs estén incluidas en `saturn_project/urls.py`:
     ```python
     from django.urls import path, include

     urlpatterns = [
         path('core/', include('core_app.urls')),
         # Otras URLs...
     ]
     ```

3. **Crear Templates en `core_app/templates/core_app/`**:
   - **`symbols_list.html`**:
     ```html
     {% extends 'base.html' %}
     {% block content %}
     <h1>Selecciona un Símbolo</h1>
     <ul>
         {% for symbol in symbols %}
         <li><a href="{% url 'minutes_by_symbol' symbol %}">{{ symbol }}</a></li>
         {% endfor %}
     </ul>
     {% endblock %}
     ```
   - **`minutes_by_symbol.html`**:
     ```html
     {% extends 'base.html' %}
     {% block content %}
     <h1>Minutas para {{ symbol }}</h1>
     <ul>
         {% for minute in minutes %}
         <li><a href="{% url 'events_by_minute' minute.id %}">{{ minute.name }}</a></li>
         {% endfor %}
     </ul>
     {% endblock %}
     ```
   - **`events_by_minute.html`**:
     ```html
     {% extends 'base.html' %}
     {% block content %}
     <h1>Histórico de Eventos para {{ minute.name }}</h1>
     <table border="1">
         <thead>
             <tr>
                 <th>Fecha</th>
                 <th>Actual</th>
                 <th>Pronóstico</th>
                 <th>Previo</th>
             </tr>
         </thead>
         <tbody>
             {% for event in events %}
             <tr>
                 <td>{{ event.event_date }}</td>
                 <td>{{ event.actual }}</td>
                 <td>{{ event.forecast }}</td>
                 <td>{{ event.previous }}</td>
             </tr>
             {% endfor %}
         </tbody>
     </table>
     {% endblock %}
     ```

4. **Probar la Funcionalidad**:
   - Inicia el servidor: `python manage.py runserver`.
   - Navega a `http://localhost:8000/core/symbols/` y selecciona un símbolo.
   - Verifica que las minutas relacionadas aparezcan y que el histórico de eventos se muestre al seleccionar una minuta.

### 3. Verificar la Integridad de la Base de Datos
- Asegúrate de que `SupportedMinute` y `EconomicEvent` estén correctamente relacionados:
  ```sql
  SELECT sm.name, sm.symbols_affected, COUNT(ee.id) AS event_count
  FROM core_app_supportedminute sm
  LEFT JOIN economic_events_app_economicevent ee ON ee.supported_minute_id = sm.id
  GROUP BY sm.id, sm.name, sm.symbols_affected
  ORDER BY sm.name;
  ```

## Notas Adicionales
- **Importación**: La lógica con `get_or_create` asegura que las minutas no se dupliquen y que los eventos se asocien correctamente.
- **Filtrado**: El campo `symbols_affected` se usa para relacionar símbolos con minutas. Si necesitas una relación más precisa (ej. tabla intermedia), ajusta el modelo `SupportedMinute`.
- **Mejoras Futuras**:
  - Agregar filtros adicionales en las vistas (ej. por impacto o fecha).
  - Mejorar el diseño de los templates con CSS.
  - Automatizar la importación con una API externa (ej. Trading Economics).

## Conclusión
Con esta implementación, las minutas se importan de manera eficiente, evitando duplicados, y los usuarios pueden filtrarlas por símbolo y consultar su histórico de eventos. Los pasos son compatibles con la estructura existente y aprovechan los modelos y vistas actuales del proyecto.

Si necesitas ajustes o más detalles, revisa la documentación en `/docs` o contacta al equipo de soporte. 🚀 (Fecha y hora de creación: [insertar fecha actual]).