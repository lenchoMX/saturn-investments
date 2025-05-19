# File Structure de Saturn Investments

Estructura de directorios y archivos del proyecto:
/saturn-investments
├── /saturn_project                 # Proyecto Django (carpeta principal)
│   ├── /mt5_scripts
│   │   ├── /eas
│   │   │   ├── calendar_ea.mq5  # EA para obtener el calendario económico
│   │   │   └── otros_eas.mq5    # Futuros EAs
│   │   ├── /indicators          # Para indicadores personalizados (futuro)
│   │   ├── /scripts             # Para scripts MQL5 (futuro)
│   │   └── EAS_LIST.md          # Documento con el listado y descripciones de EAs
│   ├── /saturn_app                 # Aplicación principal de Django (carpeta)
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML para las vistas
│   │   ├── /static                 # Archivos estáticos (CSS, JS, imágenes)
│   │   ├── /models                 # Modelos de datos para la base de datos
│   │   ├── /views                  # Vistas para manejar las solicitudes
│   │   └── /urls                   # Configuración de URLs para la aplicación
│   ├── /forex_app                  # Aplicación para el mercado Forex
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para Forex
│   │   ├── /static                 # Archivos estáticos específicos para Forex
│   │   ├── /models                 # Modelos de datos para Forex
│   │   ├── /views                  # Vistas para Forex (index, show, update, import, etc.)
│   │   ├── /urls                   # Configuración de URLs para Forex
│   │   └── /utils                  # Utilidades como lógica de importación de datos
│   ├── /commodities_app            # Aplicación para el mercado de Commodities
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para Commodities
│   │   ├── /static                 # Archivos estáticos específicos para Commodities
│   │   ├── /models                 # Modelos de datos para Commodities
│   │   ├── /views                  # Vistas para Commodities (index, show, update, import, etc.)
│   │   ├── /urls                   # Configuración de URLs para Commodities
│   │   └── /utils                  # Utilidades como lógica de importación de datos
│   ├── /equities_app               # Aplicación para el mercado de Equities
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para Equities
│   │   ├── /static                 # Archivos estáticos específicos para Equities
│   │   ├── /models                 # Modelos de datos para Equities
│   │   ├── /views                  # Vistas para Equities (index, show, update, import, etc.)
│   │   ├── /urls                   # Configuración de URLs para Equities
│   │   └── /utils                  # Utilidades como lógica de importación de datos
│   ├── /interest_rates_app         # Aplicación para el mercado de Interest Rates
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para Interest Rates
│   │   ├── /static                 # Archivos estáticos específicos para Interest Rates
│   │   ├── /models                 # Modelos de datos para Interest Rates
│   │   ├── /views                  # Vistas para Interest Rates (index, show, update, import, etc.)
│   │   ├── /urls                   # Configuración de URLs para Interest Rates
│   │   └── /utils                  # Utilidades como lógica de importación de datos
│   ├── /crypto_app                 # Aplicación para el mercado de Cryptocurrencies
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para Cryptocurrencies
│   │   ├── /static                 # Archivos estáticos específicos para Cryptocurrencies
│   │   ├── /models                 # Modelos de datos para Cryptocurrencies
│   │   ├── /views                  # Vistas para Cryptocurrencies (index, show, update, import, etc.)
│   │   ├── /urls                   # Configuración de URLs para Cryptocurrencies
│   │   └── /utils                  # Utilidades como lógica de importación de datos
│   ├── /economic_events_app        # Aplicación para eventos económicos
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para eventos económicos
│   │   ├── /models                 # Modelos de datos para eventos económicos
│   │   ├── /views                  # Vistas para eventos económicos (importación, etc.)
│   │   └── /urls                   # Configuración de URLs para eventos económicos
│   ├── /core_app                   # Aplicación para entidades y minutas soportadas
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML para entidades y minutas soportadas
│   │   ├── /models                 # Modelos de datos para entidades y minutas soportadas
│   │   ├── /views                  # Vistas para entidades y minutas soportadas
│   │   ├── /urls                   # Configuración de URLs para entidades y minutas soportadas
│   │   └── /populate_minutes.py    # Script para poblar minutas soportadas
│   └── /saturn_project             # Configuración del proyecto Django
│       ├── /settings               # Configuración del proyecto (base de datos, etc.)
│       └── /urls                   # Configuración de URLs del proyecto
├── /output                         # Archivos generados
│   ├── /charts                     # Gráficos de mercados y eventos (ej. eurusd_impact.png)
│   └── /models                     # Modelos de ML entrenados (ej. forex_regression.pkl)
├── /config                         # Configuraciones
│   └── markets                     # Lista de símbolos por mercado (ej. markets.json)
├── /requirements                   # Dependencias del proyecto
│   └── python.txt                  # Dependencias de Python (ej. django, yfinance, scikit-learn)
├── /docs                           # Documentación
│   ├── README.md                   # Descripción general del proyecto
│   ├── WORKFLOW.md                 # Flujo de trabajo para desarrollo y uso
│   ├── FILE_STRUCTURE.md           # Descripción de la estructura de archivos
│   ├── CRONOGRAM.md                # Cronograma del proyecto
│   ├── HARDWARE_SETUP.md           # Instrucciones para configurar el hardware
│   ├── SUPPORTED_MARKETS.md        # Lista de mercados soportados (ej. Forex, Commodities)
│   └── DATABASE_SETUP.md           # Instrucciones para configurar TimescaleDB y ejecutar SQL
├── /saturn                         # Entorno virtual
├── .env.example                    # Ejemplo de variables de entorno (ej. DB_HOST, DB_USER)
└── .gitignore                      # Archivos a ignorar por Git