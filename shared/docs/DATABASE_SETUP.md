# Database Setup de Saturn Investments

Instrucciones para configurar TimescaleDB:

## Requisitos
- Ubuntu 22.04 LTS (o compatible).
- PostgreSQL con extensión TimescaleDB instalada.

## Pasos
1. Instalar TimescaleDB:
   - Seguir las instrucciones oficiales en https://docs.timescale.com/install/latest/ para instalar TimescaleDB como extensión de PostgreSQL en Ubuntu 22.04 LTS. Este paso es obligatorio antes de crear bases de datos o tablas con características de TimescaleDB (como hypertables).
2. Configurar los datos de conexión:
   - Editar el archivo de configuración en Django (por ejemplo, `settings.py` en el proyecto Django) con las credenciales de tu base de datos PostgreSQL (usuario, contraseña, host, puerto).
3. Crear la base de datos `saturn_db`:
   - Manualmente: Ejecutar `CREATE DATABASE saturn_db;` en PostgreSQL.
   - Automáticamente: Usar un script de Django o migraciones para crear la base de datos y las tablas si está disponible.
4. Ejecutar los scripts SQL para definir las tablas:
   - Manualmente: `psql -U tu_usuario -d saturn_db -f src/sql/schema/schema.sql` (este archivo define la tabla `historical_data` y otras).
   - Nota: Si hay scripts adicionales como `create_economic_events.sql`, se añadirán en el futuro. Por ahora, solo `schema.sql` está implementado.
5. Verificar la conexión desde Django:
   - Ejecutar `python manage.py migrate` para aplicar migraciones iniciales y asegurar que la conexión a `saturn_db` funciona correctamente.

Más detalles se añadirán en la fase de desarrollo.