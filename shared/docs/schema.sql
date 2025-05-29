-- sql/schema.sql
-- Definición de la tabla historical_data para datos históricos de mercados financieros.
-- Nota: Falta implementar la tabla para eventos económicos (economic_events), que se añadirá en el futuro.
CREATE TABLE historical_data (
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
SELECT create_hypertable('historical_data', 'timestamp');
CREATE INDEX idx_symbol ON historical_data (symbol, timestamp);


