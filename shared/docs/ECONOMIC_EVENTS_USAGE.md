# Documentación para la Implementación de `economic_events_app` en Saturn Investments

## Introducción
Este documento describe la creación e integración de una nueva aplicación Django llamada `economic_events_app` dentro del proyecto **Saturn Investments**. Esta app gestionará datos de calendarios económicos, como eventos financieros con calificaciones de impacto (alto, medio, bajo), obtenidos de fuentes como MetaTrader 5. La implementación permitirá almacenar, visualizar y correlacionar estos eventos con datos históricos de mercados (ej. Forex, Commodities) para análisis en el proyecto.

## Objetivos
- Crear una nueva app Django (`economic_events_app`) para manejar eventos económicos de manera modular.
- Definir un modelo (`EconomicEvent`) para almacenar datos como fecha, país, nombre del evento, impacto, valores actual/pronosticado/anterior y fuente.
- Implementar vistas y templates para importar datos desde archivos CSV generados por MetaTrader 5.
- Facilitar la integración futura con datos de `historical_data` para análisis de impacto.

## Requisitos
- **Entorno**: Proyecto Django existente (`saturn_project`) con estructura modular (apps por mercado: `forex_app`, `commodities_app`, etc.).
- **Base de datos**: PostgreSQL con TimescaleDB habilitado.
- **Dependencias**: Django, pandas, psycopg2, y otras bibliotecas del proyecto.
- **Datos**: Archivos CSV generados desde MetaTrader 5 con el calendario económico.

## Pasos Generales de Implementación
1. **Crear la app `economic_events_app`**:
   - Usar `python manage.py startapp economic_events_app` para generar la estructura básica.
2. **Definir el modelo `EconomicEvent`**:
   - Incluir campos como `event_date`, `country`, `event_name`, `impact`, `actual`, `forecast`, `previous`, y `source`.
3. **Crear migraciones y aplicarlas**:
   - Generar y aplicar migraciones para crear la tabla `economic_events_app_economicevent`.
4. **Implementar vistas y templates**:
   - Crear vistas para importar datos desde CSV y mostrar eventos.
   - Desarrollar templates para la interfaz de importación y visualización.
5. **Integrar con MetaTrader 5**:
   - Usar MQL5 para exportar el calendario económico a CSV desde MT5.
   - Automatizar la importación del CSV a la base de datos mediante scripts Python.

## Notas Adicionales
- La app debe seguir la estructura modular del proyecto, con `/migrations`, `/templates`, `/models`, `/views`, `/urls`, y `/utils`.
- El modelo `EconomicEvent` debe ser flexible para futuras integraciones (ej. APIs como Trading Economics).
- La importación desde CSV es un paso inicial; se recomienda automatizar el proceso con tareas programadas (ej. Celery).