# File Structure de Saturn Investments

Estructura de directorios y archivos del proyecto:
/saturn_investiment
├── /saturn_project                 # Proyecto Django (carpeta principal)
│   ├── /commodities_app            # Aplicación para el mercado de Commodities
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /models.py              # Modelos de datos para Commodities
│   │   ├── /views.py               # Vistas para Commodities
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   └── /tests.py               # Pruebas unitarias
│   ├── /config                     # Configuraciones
│   │   ├── /sql                    # Archivos SQL para datos iniciales
│   │   │   ├── economic_events.sql # Datos de eventos económicos
│   │   │   ├── supported_entity.sql# Entidades soportadas
│   │   │   └── supported_minute.sql# Minutas soportadas
│   │   └── timezones.json          # Zonas horarias
│   ├── /core_app                   # Aplicación para entidades y minutas soportadas
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML para entidades y minutas soportadas
│   │   │   ├── /core_app           # Subcarpeta con plantillas específicas
│   │   │   │   ├── events_by_minute.html      # Eventos por minuta
│   │   │   │   ├── export_data.html           # Exportador de datos
│   │   │   │   ├── minutes_by_symbol.html     # Minutas por símbolo
│   │   │   │   ├── supported_entities.html    # Entidades soportadas
│   │   │   │   ├── supported_minutes.html     # Minutas soportadas
│   │   │   │   └── symbols_list.html          # Lista de símbolos
│   │   ├── /management             # Comandos personalizados de Django
│   │   │   └── /commands           # Subcarpeta con comandos
│   │   │       └── core_migrate_fresh.py  # Comando para migración fresca
│   │   ├── /models.py              # Modelos de datos para entidades y minutas soportadas
│   │   ├── /views.py               # Vistas para entidades y minutas soportadas
│   │   ├── /urls.py                # Configuración de URLs para entidades y minutas soportadas
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   ├── /tests.py               # Pruebas unitarias
│   │   └── /populate_minutes.py    # Script para poblar minutas soportadas
│   ├── /crypto_app                 # Aplicación para el mercado de Cryptocurrencies
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /models.py              # Modelos de datos para Cryptocurrencies
│   │   ├── /views.py               # Vistas para Cryptocurrencies
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   └── /tests.py               # Pruebas unitarias
│   ├── /economic_events_app        # Aplicación para eventos económicos
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para eventos económicos
│   │   │   └── /economic_events_app  # Subcarpeta con plantillas específicas
│   │   │       ├── economic_calendar.html  # Calendario económico
│   │   │       ├── import.html             # Importación de datos
│   │   │       └── success.html            # Mensaje de éxito
│   │   ├── /models.py              # Modelos de datos para eventos económicos
│   │   ├── /views.py               # Vistas para eventos económicos (importación, etc.)
│   │   ├── /urls.py                # Configuración de URLs para eventos económicos
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   └── /apps.py                # Configuración de la aplicación
│   ├── /equities_app               # Aplicación para el mercado de Equities
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /models.py              # Modelos de datos para Equities
│   │   ├── /views.py               # Vistas para Equities
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   └── /tests.py               # Pruebas unitarias
│   ├── /forex_app                  # Aplicación para el mercado Forex
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML específicas para Forex
│   │   │   └── /forex_app          # Subcarpeta con plantillas específicas
│   │   │       ├── analysis.html   # Análisis de datos
│   │   │       ├── import.html     # Importación de datos
│   │   │       ├── index.html      # Página principal de Forex
│   │   │       ├── success.html    # Mensaje de éxito
│   │   │       └── viz.html        # Visualización de datos
│   │   ├── /models.py              # Modelos de datos para Forex
│   │   ├── /views.py               # Vistas para Forex (index, show, update, import, etc.)
│   │   ├── /urls.py                # Configuración de URLs para Forex
│   │   ├── /forms.py               # Formularios para Forex
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   └── /tests.py               # Pruebas unitarias
│   ├── /interest_rates_app         # Aplicación para el mercado de Interest Rates
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /models.py              # Modelos de datos para Interest Rates
│   │   ├── /views.py               # Vistas para Interest Rates
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   └── /tests.py               # Pruebas unitarias
│   ├── /saturn_app                 # Aplicación principal de Django
│   │   ├── /migrations             # Migraciones de la base de datos
│   │   ├── /templates              # Plantillas HTML para las vistas
│   │   │   ├── /components         # Componentes reutilizables
│   │   │   │   ├── navbar.html     # Barra de navegación
│   │   │   │   └── offcanvas.html  # Menú desplegable
│   │   │   ├── /registration       # Plantillas de autenticación
│   │   │   │   └── login.html      # Página de inicio de sesión
│   │   │   ├── /saturn_app         # Plantillas específicas de la app
│   │   │   │   └── index.html      # Página principal
│   │   │   └── base.html           # Plantilla base
│   │   ├── /management             # Comandos personalizados de Django
│   │   │   └── /commands           # Subcarpeta con comandos
│   │   │       ├── clear_historical_data.py  # Limpiar datos históricos
│   │   │       ├── forex_migrate_fresh.py    # Migración fresca para Forex
│   │   │       └── setup_database.py         # Configuración de base de datos
│   │   ├── /models.py              # Modelos de datos para la base de datos
│   │   ├── /views.py               # Vistas para manejar las solicitudes
│   │   ├── /admin.py               # Configuración del admin de Django
│   │   ├── /apps.py                # Configuración de la aplicación
│   │   └── /tests.py               # Pruebas unitarias
│   ├── /saturn_project             # Configuración del proyecto Django
│   │   ├── /settings.py            # Configuración del proyecto (base de datos, etc.)
│   │   ├── /urls.py                # Configuración de URLs del proyecto
│   │   ├── /asgi.py                # Configuración ASGI
│   │   └── /wsgi.py                # Configuración WSGI
│   └── manage.py                   # Script de gestión de Django
├── /shared                         # Archivos y documentación compartidos
│   ├── /docs                       # Documentación del proyecto
│   │   ├── CONTRIBUTING.md         # Guía de contribución
│   │   ├── CORE_APP_USAGE.md       # Uso de la aplicación core
│   │   ├── CRONOGRAM.md            # Cronograma del proyecto
│   │   ├── CUSTOM_COMMANDS.md      # Comandos personalizados
│   │   ├── DATABASE_SETUP.md       # Configuración de la base de datos
│   │   ├── ECONOMIC_EVENTS_USAGE.md# Uso de eventos económicos
│   │   ├── FILE_STRUCTURE.md       # Estructura de archivos (este documento)
│   │   ├── GETTING_STARTED.md      # Guía de inicio
│   │   ├── HARDWARE_SETUP.md       # Configuración de hardware
│   │   ├── PLAN_FOREX_DATA_IMPORT.md # Plan de importación de datos Forex
│   │   ├── schema.sql              # Esquema SQL
│   │   ├── SUPPORTED_MARKETS.md    # Mercados soportados
│   │   ├── WORKFLOW.md             # Flujo de trabajo
│   │   └── /Implementation         # Documentación de implementación
│   │       ├── CORE_APP_IMPLEMENTATION.md              # Implementación de core_app
│   │       ├── ECONOMIC_EVENTS_IMPLEMENTATION.md       # Implementación de eventos económicos
│   │       ├── IMPLEMENTATION_ECONOMIC_CALENDAR.markdown # Implementación del calendario económico
│   │       ├── IMPLEMENTATION_MINUTES_IMPORT_AND_FILTER.markdown # Importación y filtrado de minutas
│   │       └── IMPLEMENTATION_MINUTES_ROOTCODE.md      # Código raíz de minutas
│   └── /mt5_scripts                # Scripts y EAs para MetaTrader 5
│       ├── calendar_ea.txt         # EA para obtener el calendario económico
│       └── EAS_LIST.md             # Listado y descripciones de EAs
├── /output                         # Archivos generados (no presente en el repositorio, pero ignorado por .gitignore)
│   ├── /charts                     # Gráficos de mercados y eventos
│   └── /models                     # Modelos de ML entrenados
├── /data                           # Datos (no presente en el repositorio, pero ignorado por .gitignore)
├── README.md                       # Descripción general del proyecto
├── requirements.txt                # Dependencias de Python
└── .gitignore                      # Archivos y carpetas a ignorar por Git