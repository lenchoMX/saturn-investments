# File Structure de Saturn Investments

Estructura de directorios y archivos del proyecto:
/saturn-investments
├── /src                 # Código fuente del backend
│   ├── /core            # Funcionalidad compartida
│   │   ├── db           # Conexión a TimescaleDB
│   │   └── utils        # Utilidades generales (formato de datos, cálculos comunes)
│   ├── /markets         # Módulos por tipo de mercado
│   │   ├── /forex       # Mercado Forex
│   │   │   ├── data     # Importación de datos (ej. EURUSD=X, USDJPY=X)
│   │   │   ├── analysis # Análisis de datos (ej. RSI, medias móviles)
│   │   │   └── viz      # Visualización de datos (ej. gráficos de precios)
│   │   ├── /commodities # Mercado de Commodities
│   │   │   ├── data     # Importación (ej. oro, petróleo)
│   │   │   ├── analysis # Análisis básico
│   │   │   └── viz      # Visualización (ej. gráficos)
│   │   ├── /equities    # Mercado de Equities
│   │   │   ├── data     # Importación (ej. AAPL, MSFT)
│   │   │   ├── analysis # Análisis básico
│   │   │   └── viz      # Visualización (ej. gráficos)
│   │   ├── /interest_rates # Mercado de tasas de interés
│   │   │   ├── data     # Importación (ej. CETES, T-Bills)
│   │   │   ├── analysis # Análisis de tasas
│   │   │   └── viz      # Visualización (ej. gráficos)
│   │   └── /crypto      # Mercado de Criptomonedas
│   │       ├── data     # Importación (ej. BTC-USD)
│   │       ├── analysis # Análisis básico
│   │       └── viz      # Visualización (ej. gráficos)
│   ├── /events          # Gestión de eventos económicos (ej. minutas de la FED)
│   │   ├── data         # Importación de eventos (ej. fechas de minutas)
│   │   ├── analysis     # Análisis de impacto en mercados
│   │   └── viz          # Visualización de impacto (ej. gráficos EUR/USD y oro)
│   ├── /ml              # Machine Learning
│   │   ├── /forex       # Modelos para Forex (ej. regresión lineal + placeholders)
│   │   ├── /commodities # Modelos para Commodities (placeholders)
│   │   ├── /equities    # Modelos para Equities (placeholders)
│   │   ├── /interest_rates # Modelos para tasas (placeholders)
│   │   └── /crypto      # Modelos para criptomonedas (placeholders)
│   ├── /api             # Endpoints de Flask
│   │   ├── main         # Aplicación Flask
│   │   └── routes       # Rutas de la API (ej. /import/forex, /charts/events)
│   ├── /sql             # Archivos SQL para la base de datos
│   │   ├── schema       # Definición de tablas (ej. datos_historicos, eventos_economicos)
│   │   └── migrations   # Cambios futuros en la base de datos (ej. nuevas columnas)
│   └── /ea              # Expert Advisors para MetaTrader 5
│       ├── /forex       # EAs específicos para Forex
│       │   ├── candles  # EA para velas japonesas (ej. comprobar su efectividad)
│       │   └── other    # Otros EAs para Forex (ej. recolector de datos)
│       └── /utils       # Utilidades para EAs (ej. funciones comunes en MQL5)
├── /saturn-web          # Código fuente del frontend (Laravel)
│   ├── /app             # Lógica del backend de Laravel (controladores, modelos)
│   ├── /resources       # Vistas y recursos del frontend (HTML, CSS, JS)
│   ├── /routes          # Rutas del frontend (ej. /forex, /events)
│   └── /public          # Archivos públicos (ej. gráficos generados por el backend)
├── /output              # Archivos generados
│   ├── /charts          # Gráficos de mercados y eventos (ej. eurusd_impact.png)
│   └── /models          # Modelos de ML entrenados (ej. forex_regression.pkl)
├── /config              # Configuraciones
│   └── markets          # Lista de símbolos por mercado (ej. markets.json)
├── /requirements        # Dependencias del proyecto
│   ├── python.txt       # Dependencias de Python (ej. yfinance, flask, scikit-learn)
│   └── php.txt          # Dependencias de PHP (ej. Laravel, Composer)
├── /docs                # Documentación
│   ├── README           # Descripción general del proyecto
│   ├── WORKFLOW         # Flujo de trabajo para desarrollo y uso
│   ├── FILE_STRUCTURE   # Descripción de la estructura de archivos
│   ├── CRONOGRAM        # Cronograma del proyecto
│   ├── HARDWARE_SETUP   # Instrucciones para configurar el hardware
│   ├── SUPPORTED_MARKETS # Lista de mercados soportados (ej. Forex, Commodities)
│   └── DATABASE_SETUP   # Instrucciones para configurar TimescaleDB y ejecutar SQL
├── .env.example         # Ejemplo de variables de entorno (ej. DB_HOST, DB_USER)
└── .gitignore           # Archivos a ignorar por Git