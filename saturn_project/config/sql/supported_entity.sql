-- config/sql/supported_entity.sql
INSERT INTO core_app_supportedentity (name, symbol, entity_type, description, active, created_at) VALUES
('EUR/USD', 'EURUSD', 'currency_pair', 'Par Euro/Dólar', TRUE, '2025-05-10 12:00:00+00'),
('USD/JPY', 'USDJPY', 'currency_pair', 'Par Dólar/Yen', TRUE, '2025-05-10 12:01:00+00'),
('USD/MXN', 'USDMXN', 'currency_pair', 'Par Dólar/Peso Mexicano', TRUE, '2025-05-10 12:01:00+00'),
('XAU/USD', 'XAUUSD', 'commodity', 'Oro vs Dólar', TRUE, '2025-05-10 12:02:00+00'),
('AAPL', 'AAPL', 'equity', 'Apple', TRUE, '2025-05-10 12:03:00+00'),
('CETES 28', 'CETES28', 'interest_rate', 'CETES 28', TRUE, '2025-05-10 12:04:00+00'),
('BTC/USD', 'BTCUSD', 'cryptocurrency', 'Bitcoin vs Dólar', TRUE, '2025-05-10 12:05:00+00');