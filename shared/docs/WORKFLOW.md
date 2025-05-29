# Workflow de Saturn Investments

Este documento describe el flujo de trabajo para desarrollar y usar el proyecto.

## Desarrollo
1. **Configuración del Entorno:**
   - Instalar dependencias desde `/requirements/python.txt`.
   - Configurar TimescaleDB siguiendo `DATABASE_SETUP.md`.
2. **Importación de Datos:**
   - Usar la interfaz web de Django para importar datos financieros.
   - **Forex desde HistData.com**:
     - Descargar datos históricos en M1 desde [HistData.com](http://www.histdata.com/) para pares de divisas como EUR/USD, USD/JPY, USD/MXN.
     - Guardar los archivos CSV (por ejemplo, `DAT_MT_USDMXN_M1_2010.csv`) en `/output/raw_data/forex/`.
     - Acceder a la ruta `/forex/import/` en la interfaz web de Django (proporcionada por `forex_app`) para subir y procesar los archivos CSV. El proceso de importación sigue estos pasos:
       1. **Importación a Tabla Temporal**: Los datos se importan primero a una tabla temporal (`temp_historical_data`) para evitar problemas de datos duplicados o incompletos. Antes de la importación, se borra toda la información existente en la tabla temporal.
       2. **Validación y Transferencia**: Si la importación a la tabla temporal es exitosa, los datos se transfieren a la tabla principal `historical_data`, y la tabla temporal se limpia.
       3. **Progreso en el Navegador**: Durante la importación, se muestra en el navegador el progreso (si es posible, con porcentaje de avance) tanto para la importación a la tabla temporal como a la tabla principal.
     - Revisar muestras de datos generadas en `/output/samples/` a través de la interfaz web para validar el formato antes de la importación completa.
     - Consultar reportes de importación en `/output/reports/import_report.txt` o mediante vistas en la interfaz web para estadísticas (filas totales, válidas, insertadas).
     - **Nota sobre Zonas Horarias**: Los datos de HistData.com se estandarizan a UTC durante la importación (configurable en `/config/timezones.json`) para comparaciones con eventos económicos como minutas de la FED. Esto asegura consistencia al comparar datos de diferentes fuentes que pueden no especificar su zona horaria.
     - **Estructura de la tabla `historical_data`**: Campos incluyen `timestamp` (TIMESTAMPTZ), `symbol` (VARCHAR), `market` (VARCHAR), `open_price` (DOUBLE PRECISION), `high_price`, `low_price`, `close_price`, `volume` (BIGINT), `data_source` (VARCHAR), `timeframe` (VARCHAR), `last_updated` (TIMESTAMPTZ).
   - Repetir el proceso para otros mercados (Commodities, Equities, Interest Rates, Cryptocurrencies) usando las rutas correspondientes en la interfaz web (por ejemplo, `/commodities/import/`, `/equities/import/`).
3. **Análisis y Visualización:**
   - Usar vistas específicas en la interfaz web de Django (por ejemplo, `/forex/analysis/`, `/forex/viz/`) para ejecutar análisis y generar gráficos, que se guardarán en `/output/charts`.
4. **Expert Advisors:**
   - Gestionar el desarrollo y prueba de EAs a través de una sección dedicada en la interfaz web de Django (por ejemplo, `/forex/ea/`).
5. **Frontend y Backend con Django:**
   - Configurar y personalizar la interfaz y lógica en las aplicaciones específicas de Django (`forex_app`, `commodities_app`, etc.), accesibles a través de rutas como `/forex/`, `/commodities/`, etc.

## Uso
- Acceder a la interfaz web mediante el servidor de Django ejecutando `python manage.py runserver` para visualizar datos y análisis.
- Navegar entre mercados usando el dropdown en el navbar para acceder a rutas como `/forex/`, `/commodities/`, etc.
- Consultar gráficos generados en `/output/charts` a través de vistas en la interfaz web.

Más detalles se añadirán conforme avance el proyecto.