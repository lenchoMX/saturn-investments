# Plan para la Implementación de la Importación de Datos Históricos de Forex

## Objetivo
Configurar el módulo de Forex para importar datos históricos de pares de divisas desde HistData.com, organizarlos y almacenarlos en TimescaleDB, mapeando los datos a la tabla `historical_data` según la estructura definida en `src/sql/schema.sql`, y manejando discrepancias de zonas horarias para comparaciones con otros mercados y eventos económicos.

## Pasos del Plan

1. **Descarga de Datos Históricos de HistData.com**:
   - Acceder al sitio web de HistData.com y descargar los archivos ZIP que contienen datos históricos en M1 para los pares de divisas deseados (por ejemplo, EUR/USD, USD/JPY, USD/MXN).
   - Los archivos están organizados por año (por ejemplo, `DAT_MT_USDMXN_M1_2010.csv`), y cada archivo CSV incluye columnas para fecha, hora, apertura, máximo, mínimo, cierre y volumen.
   - Descargar los datos por bimestre o trimestre si es posible, o por año completo, para facilitar la gestión de grandes volúmenes de datos.
   - Guardar los archivos descargados en un directorio temporal como `/output/raw_data/forex/` para su posterior procesamiento.

2. **Creación de la Estructura de Directorios**:
   - Crear el directorio `/src/markets/forex/` con subdirectorios `/data`, `/analysis` y `/viz`, siguiendo la estructura definida en FILE_STRUCTURE.md.
   - Crear `/output/raw_data/forex/` para almacenar los archivos CSV descargados de HistData.com.
   - Crear `/output/samples/` para guardar muestras de datos procesados para revisión.

3. **Revisión de una Muestra de Datos**:
   - Extraer y revisar un archivo CSV de muestra (por ejemplo, datos de EUR/USD para un bimestre de 2010) para confirmar el formato y la integridad de los datos.
   - Generar un archivo de muestra reducido (por ejemplo, los primeros 100 registros) y guardarlo en `/output/samples/` para que el usuario lo revise y apruebe antes de la importación completa.

4. **Desarrollo del Script de Importación de Datos**:
   - Crear un script Python en `/src/markets/forex/data/import_data.py` para leer los archivos CSV de HistData.com y guardarlos en TimescaleDB usando modelos de Django si es posible, o consultas SQL directas para manejar hypertables.
   - **Convenciones de Código**: Todos los nombres de variables, clases y funciones en el código Python estarán en inglés (por ejemplo, `historical_data`, `import_data`, `process_batch`), siguiendo las convenciones estándar de programación. Los comentarios y notas dentro del código estarán en español para facilitar la comprensión del equipo.
   - El script debe:
     - Leer los archivos CSV desde `/output/raw_data/forex/`.
     - Procesar los datos por lotes (por ejemplo, 10,000 registros a la vez) para manejar eficientemente millones de registros sin problemas de memoria.
     - Conectarse a la base de datos `saturn_db` siguiendo las configuraciones en `settings.py` de Django.
     - Mapear los datos de HistData.com a la tabla `historical_data` con los siguientes campos:
       - `timestamp`: Combinar fecha y hora del CSV (por ejemplo, "2010.11.14,17:05" a un formato TIMESTAMPTZ). Ver el paso 5 para el manejo de zonas horarias.
       - `symbol`: Extraer del nombre del archivo o configurar manualmente (por ejemplo, "USDMXN" de `DAT_MT_USDMXN_M1_2010.csv`).
       - `market`: Establecer como "Forex".
       - `open_price`, `high_price`, `low_price`, `close_price`: Mapear directamente desde las columnas del CSV (renombrando para seguir convenciones en inglés).
       - `volume`: Mapear desde la columna de volumen del CSV.
       - `data_source`: Establecer como "HistData.com".
       - `timeframe`: Establecer como "M1" (1 minuto).
       - `last_updated`: Usar la fecha y hora actuales por defecto.
     - Registrar el progreso y cualquier error en un archivo de log en `/output/logs/`.
   - Asegurarse de manejar diferentes formatos de fecha y hora si varían entre archivos o pares de divisas.

5. **Manejo de Zonas Horarias para Comparaciones de Mercado**:
   - **Problema**: HistData.com no especifica la zona horaria de sus datos (puede ser GMT, EET u otra dependiendo del broker origen en MetaTrader). Esto crea discrepancias al comparar datos de Forex con otros mercados (como bonos) o eventos económicos (como minutas de la FED), que pueden estar en zonas horarias diferentes (por ejemplo, EST/EDT para eventos de EE.UU.).
   - **Solución**: 
     - Asumir una zona horaria por defecto para los datos de HistData.com (por ejemplo, GMT/UTC+0, común en datos de Forex) y convertir el campo `timestamp` a UTC durante la importación, ya que `TIMESTAMPTZ` en TimescaleDB permite almacenar datos con zona horaria.
     - Crear un archivo de configuración en `/config/timezones.json` o similar, donde se pueda especificar la zona horaria asumida para cada fuente de datos (por ejemplo, "HistData.com": "UTC+0").
     - En el script de importación, permitir la conversión de zonas horarias si se conoce la zona horaria correcta más adelante, o estandarizar todos los datos a UTC para consistencia en análisis comparativos.
     - Para eventos económicos como las minutas de la FED, asegurarse de que su `timestamp` también se almacene en UTC, permitiendo comparaciones precisas con los datos de Forex.
   - Documentar este enfoque en el script y en la documentación para que el usuario pueda ajustar la zona horaria si obtiene información más precisa sobre los datos de HistData.com.

6. **Validación de Datos Importados**:
   - Implementar una función en el script de importación para validar los datos (por ejemplo, verificar que no haya valores nulos en campos críticos como `close_price`).
   - Generar un informe básico de los datos importados (por ejemplo, número de registros por par de divisas y rango de fechas) y guardarlo en `/output/reports/`.

7. **Documentación del Proceso**:
   - Actualizar `/docs/WORKFLOW.md` con instrucciones detalladas sobre cómo descargar datos de HistData.com, dónde almacenarlos, cómo ejecutar el script de importación y la estructura de la tabla `historical_data`. Asegurarse de que todas las referencias en los archivos markdown usen `historical_data` como nombre de la tabla.
   - Incluir una sección sobre el manejo de zonas horarias y cómo estandarizar los datos a UTC para comparaciones con otros mercados y eventos económicos.

## Diagrama de Flujo (Mermaid)
```mermaid
flowchart TD
    A[Inicio] --> B[Descargar datos históricos de HistData.com por año o bimestre]
    B --> C[Guardar CSVs en /output/raw_data/forex/]
    C --> D[Revisar muestra de datos y generar archivo de ejemplo en /output/samples/]
    D --> E[Crear estructura de directorios: /src/markets/forex/data/]
    E --> F[Desarrollar script de importación en Python para CSVs a TimescaleDB]
    F --> G[Mapear datos a tabla historical_data: timestamp, symbol, open_price, etc.]
    G --> H[Manejar zonas horarias: asumir UTC y estandarizar a TIMESTAMPTZ]
    H --> I[Procesar datos por lotes para manejar millones de registros]
    I --> J[Validar datos y generar informe en /output/reports/]
    J --> K[Actualizar documentación en /docs/WORKFLOW.md con historical_data]
    K --> L[Fin: Datos históricos listos para análisis]