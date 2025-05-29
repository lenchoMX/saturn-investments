# Contribuyendo a Saturn Investments

Este documento proporciona una guía detallada sobre cómo trabajar con el proyecto Saturn Investments, desde la configuración del entorno hasta el desarrollo y uso de la aplicación. Sigue estos pasos para contribuir al proyecto, que está disponible en GitHub.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:
- Un sistema operativo compatible (se recomienda Ubuntu 22.04 LTS para la configuración del servidor de base de datos, pero el desarrollo puede realizarse en Windows, macOS o Linux).
- Python 3.11.9 (según lo especificado en `README.md`).
- PostgreSQL con la extensión TimescaleDB instalada.
- Acceso a internet para descargar dependencias y herramientas.
- Conocimientos básicos de terminal o línea de comandos.

## Pasos para Configurar el Proyecto

### 1. Clonar el Repositorio
- Clona el repositorio de GitHub en tu máquina local:
  ```
  git clone https://github.com/tu_usuario/saturn-investments.git
  cd saturn-investments
  ```

### 2. Crear un Entorno Virtual
- **Propósito**: Un entorno virtual aísla las dependencias del proyecto para evitar conflictos con otras instalaciones de Python en tu sistema.
- **Instrucciones**:
  - Abre una terminal en el directorio raíz del proyecto (`c:/Projects/Software/Python/saturn_investiment` en Windows o la ruta equivalente en otros sistemas).
  - Ejecuta el comando `python -m venv saturn` (o `python3 -m venv saturn` en Linux/macOS si `python` no apunta a Python 3.11.9) para crear un entorno virtual en la carpeta `saturn`.
  - Activa el entorno virtual:
    - En Windows, ejecuta `saturn\Scripts\activate.bat` desde la terminal.
    - En Linux/macOS, ejecuta `source saturn/bin/activate`.
  - Una vez activado, verás `(saturn)` al inicio de la línea de comandos, indicando que estás dentro del entorno virtual.
  - Verifica la versión de Python con `python --version` para confirmar que estás usando Python 3.11.9 dentro del entorno virtual.

### 3. Instalar las Dependencias
- **Propósito**: Instalar las dependencias necesarias para el proyecto listadas en `requirements.txt`.
- **Instrucciones**:
  - Asegúrate de que tu entorno virtual esté activado.
  - Ejecuta el comando `pip install -r requirements.txt` para instalar las versiones específicas de las dependencias (Django, psycopg2-binary, etc.).

### 4. Configurar la Conexión a la Base de Datos
- **Propósito**: Configurar las credenciales de tu base de datos PostgreSQL/TimescaleDB en el archivo de configuración de Django.
- **Instrucciones**:
  - Abre el archivo `saturn_project/saturn_project/settings.py` en el directorio del proyecto.
  - Busca la sección `DATABASES` y actualiza las credenciales con tus datos de PostgreSQL:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'saturn_db',
            'USER': 'tu_usuario',
            'PASSWORD': 'tu_contraseña',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
  - Guarda los cambios. Asegúrate de no cometer este archivo con datos sensibles a un repositorio público; usa `.gitignore` para excluirlo si es necesario, o utiliza variables de entorno para manejar las credenciales.

### 5. Crear la Base de Datos
- **Propósito**: Crear la base de datos `saturn_db` si no existe, utilizando un comando de gestión personalizado de Django.
- **Instrucciones**:
  - Asegúrate de que tu entorno virtual esté activado y de que estás en el directorio del proyecto (`saturn_project`).
  - Ejecuta el comando:
    ```
    python manage.py setup_database
    ```
  - Este comando verificará si la base de datos `saturn_db` existe y la creará si no es así. Revisa los mensajes en la terminal para confirmar que la base de datos se creó con éxito o para identificar cualquier error.

### 6. Aplicar Migraciones Iniciales
- **Propósito**: Crear las tablas básicas de Django en la base de datos.
- **Instrucciones**:
  - Asegúrate de que tu entorno virtual esté activado y de que estás en el directorio del proyecto (`saturn_project`).
  - Ejecuta el comando:
    ```
    python manage.py migrate
    ```
  - Este comando aplicará las migraciones iniciales de Django, creando las tablas necesarias para la autenticación, administración, etc.

### 7. Verificar el Servidor de Desarrollo
- **Propósito**: Iniciar el servidor de desarrollo de Django para verificar que todo está configurado correctamente.
- **Instrucciones**:
  - Asegúrate de que tu entorno virtual esté activado y de que estás en el directorio del proyecto (`saturn_project`).
  - Ejecuta el comando:
    ```
    python manage.py runserver
    ```
  - Abre un navegador y accede a `http://127.0.0.1:8000/` para confirmar que la página de bienvenida de Django aparece.

## Desarrollo y Contribución

### Estructura del Proyecto
- Consulta `FILE_STRUCTURE.md` en la carpeta `docs` para entender la organización de las aplicaciones Django específicas para cada mercado (`forex_app`, `commodities_app`, etc.).
- Toda la lógica de negocio, incluidos los importadores de datos, se maneja a través de la interfaz web de Django, utilizando vistas y formularios.

### Flujo de Trabajo
- Consulta `WORKFLOW.md` en la carpeta `docs` para detalles sobre cómo importar datos, realizar análisis y visualizar resultados a través de la interfaz web.
- Usa el navbar con el dropdown de mercados para navegar entre las diferentes secciones (Forex, Commodities, etc.).

### Creación de Modelos y Migraciones Personalizadas
- Para integrar tablas personalizadas como `historical_data` (definida en `schema.sql`), crea modelos en Django en la aplicación correspondiente (por ejemplo, `forex_app/models.py`). Ten en cuenta que las características de TimescaleDB como `hypertable` pueden requerir SQL personalizado aplicado mediante migraciones manuales.
- Para aplicar SQL personalizado, usa:
  ```
  python manage.py makemigrations
  python manage.py sqlmigrate <app_name> <migration_number>
  ```
  Luego, ajusta las migraciones para incluir el SQL de `schema.sql`.

## Notas Adicionales
- Si encuentras problemas durante la configuración, consulta los archivos de documentación en `/docs` para más detalles o busca ayuda en los canales de soporte del proyecto.
- Asegúrate de seguir las convenciones de código de Django para mantener la consistencia en el proyecto.
- Para contribuir, crea un fork del repositorio, realiza tus cambios en una rama específica y envía un pull request para revisión.

¡Con estos pasos, deberías tener el entorno configurado y estar listo para contribuir a Saturn Investments!