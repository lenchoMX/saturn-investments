# Database Setup de Saturn Investments

Instrucciones para configurar TimescaleDB:

## Requisitos
- Ubuntu 22.04 LTS (o compatible).
- PostgreSQL con extensión TimescaleDB instalada.

## Pasos
1. Instalar TimescaleDB:
   - Seguir las instrucciones oficiales en https://docs.timescale.com/install/latest/.
2. Crear la base de datos `saturn_db`:
   - `CREATE DATABASE saturn_db;`
3. Ejecutar los scripts SQL:
   - `psql -U tu_usuario -d saturn_db -f /src/sql/schema/create_historical_data.sql`
   - `psql -U tu_usuario -d saturn_db -f /src/sql/schema/create_economic_events.sql`
4. Verificar la conexión desde `/src/core/db`.

Más detalles se añadirán en la fase de desarrollo.