-- config/sql/supported_entity.sql
INSERT INTO core_app_supportedentity (name, symbol, entity_type, description, active, created_at) VALUES
('EUR/USD', 'EURUSD', 'currency_pair', 'Par Euro/Dólar', TRUE, '2025-05-10 12:00:00+00'),

('USD/CAD', 'USDCAD', 'currency_pair', 'Par Dólar/Dólar canadiense', TRUE, '2025-05-10 12:01:00+00'),
('USD/CHF', 'USDCHF', 'currency_pair', 'Par Dólar/Franco Suizo', TRUE, '2025-05-10 12:01:00+00'),
('USD/CZK', 'USDCZK', 'currency_pair', 'Par Dólar/Corona Checa', TRUE, '2025-05-10 12:01:00+00'),
('USD/DKK', 'USDDKK', 'currency_pair', 'Par Dólar/Corona Danesa', TRUE, '2025-05-10 12:01:00+00'),
('USD/HKD', 'USDHKD', 'currency_pair', 'Par Dólar/Dólar de Hong Kong', TRUE, '2025-05-10 12:01:00+00'),
('USD/HUF', 'USDHUF', 'currency_pair', 'Par Dólar/Forinto Húngaro', TRUE, '2025-05-10 12:01:00+00'),
('USD/JPY', 'USDJPY', 'currency_pair', 'Par Dólar/Yen japonés', TRUE, '2025-05-10 12:01:00+00'),
('USD/MXN', 'USDMXN', 'currency_pair', 'Par Dólar/Peso Mexicano', TRUE, '2025-05-10 12:01:00+00'),
('USD/NOK', 'USDNOK', 'currency_pair', 'Par Dólar/Corona Noruega', TRUE, '2025-05-10 12:01:00+00'),
('USD/PLN', 'USDPLN', 'currency_pair', 'Par Dólar/Złoty Polaco', TRUE, '2025-05-10 12:01:00+00'),
('USD/SEK', 'USDSEK', 'currency_pair', 'Par Dólar/Corona Sueca', TRUE, '2025-05-10 12:01:00+00'),
('USD/SGD', 'USDSGD', 'currency_pair', 'Par Dólar/Dólar de Singapur', TRUE, '2025-05-10 12:01:00+00'),
('USD/TRY', 'USDTRY', 'currency_pair', 'Par Dólar/Lira Turca', TRUE, '2025-05-10 12:01:00+00'),
('USD/ZAR', 'USDZAR', 'currency_pair', 'Par Dólar/Rand Sudafricano', TRUE, '2025-05-10 12:01:00+00'),

('XAU/USD', 'XAUUSD', 'commodity', 'Oro vs Dólar', TRUE, '2025-05-10 12:02:00+00'),
('AAPL', 'AAPL', 'equity', 'Apple', TRUE, '2025-05-10 12:03:00+00'),
('CETES 28', 'CETES28', 'interest_rate', 'CETES 28', TRUE, '2025-05-10 12:04:00+00'),
('BTC/USD', 'BTCUSD', 'cryptocurrency', 'Bitcoin vs Dólar', TRUE, '2025-05-10 12:05:00+00');