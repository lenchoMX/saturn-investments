# Comandos Personalizados en Saturn Investments

Este documento detalla los comandos personalizados disponibles en el proyecto Saturn Investments, creados para facilitar tareas específicas de gestión de datos y migraciones en la aplicación Django.

## 1. `clear_historical_data`

**Descripción**: Este comando elimina todos los registros de la tabla `historical_data`, útil para limpiar datos históricos antes de una nueva importación o para pruebas.

**Ubicación**: `saturn_app/management/commands/clear_historical_data.py`

**Uso**:
```bash
python saturn_project/manage.py clear_historical_data
```

**Salida Esperada**:
- Si tiene éxito, muestra un mensaje indicando cuántos registros fueron eliminados.
- Si ocurre un error, muestra un mensaje de error con detalles.

**Notas**:
- Este comando no elimina la estructura de la tabla, solo los datos.
- Úsalo con precaución, ya que los datos eliminados no se pueden recuperar a menos que tengas una copia de seguridad.

## 2. `forex_migrate_fresh`

**Descripción**: Este comando borra las tablas de la aplicación `forex_app` de la base de datos y vuelve a aplicar las migraciones específicas de `forex_app`, similar a `php artisan migrate:fresh` en Laravel, pero limitado a esta aplicación. Es útil para reiniciar las tablas de `forex_app` durante el desarrollo sin afectar las tablas de Django u otras aplicaciones.

**Ubicación**: `saturn_app/management/commands/forex_migrate_fresh.py`

**Uso**:
```bash
python manage.py saturn_project/forex_migrate_fresh
```

**Salida Esperada**:
- Solicita confirmación antes de proceder (ingresa 'y' para confirmar).
- Si se confirma, muestra mensajes indicando las tablas de `forex_app` que se están borrando (bajo el encabezado "Drop migrations:") y las migraciones que se aplican para recrear las tablas (bajo el encabezado "Running migrations:").
- Si ocurre un error, muestra un mensaje de error con detalles.
- Si no se confirma, cancela la operación con un mensaje de error.

**Notas**:
- Este comando solo afecta las tablas asociadas con la aplicación `forex_app`.
- No elimina datos ni tablas de Django (como `auth_user`, `django_migrations`, etc.) ni de otras aplicaciones.
- Es ideal para entornos de desarrollo cuando necesitas reiniciar las tablas de `forex_app` sin afectar el resto del sistema.
- **Advertencia**: Este comando elimina datos de las tablas de `forex_app`. Asegúrate de tener una copia de seguridad si hay datos importantes.

## 3. `setup_database`

**Descripción**: Este comando verifica si la base de datos `saturn_db` existe y la crea si no es así. Es útil para la configuración inicial del entorno.

**Ubicación**: `saturn_app/management/commands/setup_database.py`

**Uso**:
```bash
python manage.py saturn_project/setup_database
```

**Salida Esperada**:
- Muestra mensajes indicando si la base de datos ya existe o si se creó con éxito.
- Si ocurre un error (por ejemplo, problemas de permisos), muestra un mensaje de error con detalles.

**Notas**:
- Este comando no aplica migraciones; solo crea la base de datos vacía.
- Debe ejecutarse antes de `migrate` si la base de datos no existe.

## Notas Generales
- Todos los comandos personalizados deben ejecutarse desde el directorio del proyecto (`saturn_project`) con el entorno virtual activado.
- Asegúrate de revisar los mensajes de salida para confirmar que las operaciones se completaron con éxito o para diagnosticar errores.
- Para activar el entorno virtual en Windows, usa:
  ```bash
  c:\Projects\Software\Python\saturn_investiment\saturn\Scripts\activate.bat
  ```
  En Linux/macOS, usa:
  ```bash
  source c:/Projects/Software/Python/saturn_investiment/saturn/bin/activate
  ```

## 4. `core_migrate_fresh`

**Descripción**: Este comando borra las tablas de la aplicación `core_app` y la tabla `economic_events_app_economicevent` de la base de datos, vuelve a aplicar las migraciones específicas de `core_app` y `economic_events_app`, y ejecuta la importación de datos desde los archivos SQL `supported_entity.sql`, `supported_minute.sql` y `economic_events.sql`. Es útil para reiniciar las tablas de `core_app` y `economic_events_app` durante el desarrollo sin afectar las tablas de Django u otras aplicaciones, y para poblar la base de datos con datos iniciales.

**Ubicación**: `core_app/management/commands/core_migrate_fresh.py`

**Uso**:
```bash
python saturn_project/manage.py core_migrate_fresh
```

**Salida Esperada**:
- Solicita confirmación antes de proceder (ingresa 'y' para confirmar).
- Si se confirma, muestra mensajes indicando las tablas de `core_app` y `economic_events_app_economicevent` que se están borrando (bajo el encabezado "Drop migrations:") y las migraciones que se aplican para recrear las tablas (bajo el encabezado "Running migrations:").
- También muestra mensajes sobre la importación de datos desde los archivos SQL `supported_entity.sql`, `supported_minute.sql` y `economic_events.sql`.
- Si ocurre un error, muestra un mensaje de error con detalles.
- Si no se confirma, cancela la operación con un mensaje de error.

**Notas**:
- Este comando afecta las tablas asociadas con las aplicaciones `core_app` y `economic_events_app`.
- No elimina datos ni tablas de Django (como `auth_user`, `django_migrations`, etc.) ni de otras aplicaciones.
- Es ideal para entornos de desarrollo cuando necesitas reiniciar las tablas de `core_app` y `economic_events_app` sin afectar el resto del sistema.
- **Advertencia**: Este comando elimina datos de las tablas de `core_app` y `economic_events_app`. Asegúrate de tener una copia de seguridad si hay datos importantes.
Si tienes preguntas sobre estos comandos o necesitas comandos adicionales, por favor indícalo para poder asistirte.