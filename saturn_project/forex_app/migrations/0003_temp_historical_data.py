# Custom migration to create temp_historical_data as a hypertable in TimescaleDB

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('forex_app', '0002_historical_data'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Drop the table if it exists to avoid conflicts
            DROP TABLE IF EXISTS temp_historical_data CASCADE;
            
            -- Create the temp_historical_data table
            CREATE TABLE temp_historical_data (
                timestamp TIMESTAMPTZ NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                market VARCHAR(50),
                open_price DOUBLE PRECISION,
                high_price DOUBLE PRECISION,
                low_price DOUBLE PRECISION,
                close_price DOUBLE PRECISION,
                volume BIGINT,
                data_source VARCHAR(50),
                timeframe VARCHAR(10),
                last_updated TIMESTAMPTZ DEFAULT NOW(),
                PRIMARY KEY (timestamp, symbol)
            );
            
            -- Configure as hypertable with timestamp as the partitioning column
            SELECT create_hypertable('temp_historical_data', 'timestamp');
            
            -- Create index for faster queries
            CREATE INDEX idx_symbol_temp ON temp_historical_data (symbol, timestamp);
            """,
            reverse_sql="DROP TABLE IF EXISTS temp_historical_data CASCADE;"
        ),
    ]