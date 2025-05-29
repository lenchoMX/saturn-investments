# Instrucciones para la Implementación del Calendario Económico en Saturn Investments

## Introducción
Este documento detalla los pasos para agregar una sección de calendario económico en el proyecto **Saturn Investments**, similar a https://www.mql5.com/en/economic-calendar, utilizando los datos importados y almacenados en la base de datos. La sección se integrará en `economic_events_app` y permitirá a los usuarios visualizar y filtrar eventos económicos.

## Objetivos
- Crear una vista y template para mostrar un calendario económico con eventos importados.
- Implementar filtros por moneda, impacto y rango de fechas.
- Añadir paginación para manejar grandes conjuntos de datos.
- Integrar la sección en la navegación del proyecto.

## Requisitos Previos
- **Entorno**: Proyecto Django `saturn_project` con `economic_events_app` configurado.
- **Base de datos**: PostgreSQL con TimescaleDB y la tabla `economic_events_app_economicevent` poblada.
- **Dependencias**: Django, pandas, django-tables2 (para tablas y paginación).
- **Estado actual**: Modelo `EconomicEvent` en `economic_events_app/models.py` con campos como `event_date`, `country`, `event_name`, `impact`, `actual`, `forecast`, `previous`.

## Pasos de Implementación

### 1. Instalar Dependencias Adicionales
- Instalar `django-tables2` para tablas con paginación y ordenamiento:
  ```bash
  pip install django-tables2
  ```

### 2. Crear la Vista del Calendario Económico
1. **Añadir una vista en `economic_events_app/views.py`**:
   ```python
   from django.shortcuts import render
   from .models import EconomicEvent
   import django_tables2 as tables

   class EconomicEventTable(tables.Table):
       class Meta:
           model = EconomicEvent
           fields = ('event_date', 'country', 'event_name', 'impact', 'actual', 'forecast', 'previous')
           attrs = {'class': 'table table-striped'}

   def economic_calendar(request):
       events = EconomicEvent.objects.all().order_by('event_date')
       table = EconomicEventTable(events)
       table.paginate(page=request.GET.get('page', 1), per_page=50)
       return render(request, 'economic_events_app/economic_calendar.html', {'table': table})
   ```

2. **Configurar URLs en `economic_events_app/urls.py`**:
   - Crear o actualizar el archivo con:
     ```python
     from django.urls import path
     from . import views

     urlpatterns = [
         path('calendar/', views.economic_calendar, name='economic_calendar'),
     ]
     ```
   - Asegurarse de incluir las URLs en `saturn_project/urls.py`:
     ```python
     from django.urls import path, include

     urlpatterns = [
         path('economic-events/', include('economic_events_app.urls')),
         # Otras URLs...
     ]
     ```

3. **Crear el template `economic_events_app/templates/economic_events_app/economic_calendar.html`**:
   ```html
   {% extends 'base.html' %}
   {% load django_tables2 %}
   {% block content %}
   <h1>Calendario Económico</h1>
   {% render_table table %}
   {% endblock %}
   ```

### 3. Implementar Filtrado
1. **Modificar la vista para aceptar parámetros de filtrado**:
   ```python
   from django.db.models import Q

   def economic_calendar(request):
       events = EconomicEvent.objects.all().order_by('event_date')
       
       # Filtros
       currency = request.GET.get('currency')
       impact = request.GET.get('impact')
       date_from = request.GET.get('date_from')
       date_to = request.GET.get('date_to')
       
       if currency:
           events = events.filter(country=currency)
       if impact:
           events = events.filter(impact=impact)
       if date_from:
           events = events.filter(event_date__gte=date_from)
       if date_to:
           events = events.filter(event_date__lte=date_to)
       
       table = EconomicEventTable(events)
       table.paginate(page=request.GET.get('page', 1), per_page=50)
       return render(request, 'economic_events_app/economic_calendar.html', {'table': table})
   ```

2. **Actualizar el template para incluir formularios de filtrado**:
   ```html
   {% extends 'base.html' %}
   {% load django_tables2 %}
   {% block content %}
   <h1>Calendario Económico</h1>
   <form method="get">
       <label for="currency">Moneda:</label>
       <input type="text" name="currency" id="currency" value="{{ request.GET.currency }}">
       <label for="impact">Impacto:</label>
       <select name="impact" id="impact">
           <option value="">Todos</option>
           <option value="High" {% if request.GET.impact == "High" %}selected{% endif %}>Alto</option>
           <option value="Medium" {% if request.GET.impact == "Medium" %}selected{% endif %}>Medio</option>
           <option value="Low" {% if request.GET.impact == "Low" %}selected{% endif %}>Bajo</option>
       </select>
       <label for="date_from">Desde:</label>
       <input type="date" name="date_from" id="date_from" value="{{ request.GET.date_from }}">
       <label for="date_to">Hasta:</label>
       <input type="date" name="date_to" id="date_to" value="{{ request.GET.date_to }}">
       <button type="submit">Filtrar</button>
   </form>
   {% render_table table %}
   {% endblock %}
   ```

### 4. Integrar en la Navegación
- **Añadir un enlace en el template base o dashboard**:
  ```html
  <a href="{% url 'economic_calendar' %}">Calendario Económico</a>
  ```

## Notas Adicionales
- **Performance**: Para grandes conjuntos de datos, considera indexar campos como `event_date` y `country`.
- **Estilo**: Personaliza el CSS de la tabla para que coincida con el diseño de https://www.mql5.com/en/economic-calendar.
- **Mejoras Futuras**: Implementa detalles del evento al hacer clic, usando una vista adicional.

## Conclusión
Esta implementación crea una sección de calendario económico en `economic_events_app`, con filtrado y paginación, usando datos importados. La integración es sencilla y mantiene la estructura modular del proyecto.

Si necesitas ajustes, revisa la documentación en `/docs` o contacta al equipo de soporte. 🚀 (Fecha y hora de creación: 20 de octubre de 2023, 10:00 AM GMT).