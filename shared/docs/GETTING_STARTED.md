# Cómo Comenzar a Usar Saturn Investments

Este documento proporciona una guía paso a paso para configurar y comenzar a usar el proyecto Saturn Investments. Sigue estas instrucciones para preparar tu entorno de desarrollo y ejecutar los componentes iniciales del proyecto. Este archivo se actualizará conforme el proyecto avance.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:
- Un sistema operativo compatible (se recomienda Ubuntu 22.04 LTS para la configuración del servidor de base de datos, pero el desarrollo puede realizarse en Windows, macOS o Linux).
- Acceso a internet para descargar dependencias y herramientas.
- Conocimientos básicos de terminal o línea de comandos.

## Pasos para Configurar el Proyecto

### 1. Instalar la Versión Correcta de Python
- **Versión Requerida**: Python 3.11.9 (según lo especificado en `README.md`).
- **Instrucciones**:
  - Descarga e instala Python 3.11.9 desde el sitio oficial [python.org](https://www.python.org/downloads/release/python-3119/) o usa un gestor de versiones como `pyenv` (en Linux/macOS) para instalar esta versión específica.
  - Verifica la instalación ejecutando `python --version` o `python3 --version` en tu terminal. Asegúrate de que la salida muestre `Python 3.11.9`.
  - En Windows, asegúrate de agregar Python al PATH durante la instalación para que sea accesible desde la terminal.

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

### 3. Instalar PostgreSQL
- **Versión Requerida**: No se especifica una versión exacta en la documentación, pero se recomienda usar la versión más reciente compatible con TimescaleDB (por ejemplo, PostgreSQL 14 o 15, según lo soportado por TimescaleDB en https://docs.timescale.com/install/latest/).
- **Instrucciones**:
  - **Windows**: Descarga e instala PostgreSQL desde [postgresql.org](https://www.postgresql.org/download/windows/). Durante la instalación, configura un usuario y contraseña (anótalos, los necesitarás para la configuración en Django).
  - **Ubuntu/Linux**: Sigue las instrucciones en [postgresql.org](https://www.postgresql.org/download/linux/ubuntu/) o usa `sudo apt update && sudo apt install postgresql-14 postgresql-contrib` (ajusta la versión si es necesario).
  - **macOS**: Usa Homebrew con `brew install postgresql` o descarga desde [postgresql.org](https://www.postgresql.org/download/macosx/).
  - Verifica la instalación ejecutando `psql --version` en la terminal para confirmar que PostgreSQL está instalado y accesible.

### 4. Instalar TimescaleDB
- **Propósito**: TimescaleDB es una extensión de PostgreSQL optimizada para datos de series temporales, usada en este proyecto para almacenar datos históricos de mercados financieros.
- **Instrucciones**:
  - Sigue las instrucciones oficiales en [https://docs.timescale.com/install/latest/](https://docs.timescale.com/install/latest/) para instalar TimescaleDB como extensión de PostgreSQL.
  - **Ubuntu/Linux**: Generalmente implica añadir el repositorio de TimescaleDB y ejecutar comandos como `sudo apt install timescaledb-2-postgresql-14` (ajusta según tu versión de PostgreSQL).
  - **Windows**: TimescaleDB no tiene soporte oficial completo para Windows, por lo que se recomienda usar un entorno Linux (como WSL2) o una máquina virtual con Ubuntu 22.04 LTS para la base de datos. Sigue las instrucciones de instalación en Linux dentro de ese entorno.
  - **Verificación**: Conéctate a PostgreSQL con `psql -U postgres` y ejecuta `\dx` para listar las extensiones instaladas; deberías ver `timescaledb` en la lista.

### 5. Instalar Django
- **Propósito**: Django es el framework principal para el desarrollo del backend y frontend del proyecto.
- **Instrucciones**:
  - Asegúrate de que tu entorno virtual esté activado (ver paso 2).
  - Ejecuta el comando `pip install django` para instalar la versión más reciente de Django.
  - Verifica la instalación con `django-admin --version` para confirmar que Django está instalado correctamente.

### 6. Configurar el Proyecto Django
- **Propósito**: Crear la estructura inicial del proyecto Django y configurar la conexión a la base de datos.
- **Instrucciones**:
  - Ejecuta `django-admin startproject saturn_project` para crear un nuevo proyecto Django llamado "saturn_project".
  - Navega al directorio del proyecto con `cd saturn_project`.
  - Edita el archivo `saturn_project/settings.py` para configurar la conexión a la base de datos `saturn_db` con las credenciales de PostgreSQL (usuario, contraseña, host, puerto).
  - Ejecuta `python manage.py migrate` para aplicar las migraciones iniciales y crear las tablas básicas de Django.

### 7. Integrar Bootstrap y Sweetalert2
- **Propósito**: Usar Bootstrap para el diseño responsivo y Sweetalert2 para alertas atractivas en la interfaz de usuario.
- **Instrucciones**:
  - No es necesario instalar estas librerías localmente. Se usarán mediante CDN en las plantillas HTML de Django para mantener el proyecto ligero.
  - En tus plantillas HTML (en `saturn_app/templates/`), incluye los enlaces a los CDNs de Bootstrap y Sweetalert2 según se detalla en la documentación de cada librería.

## Notas Adicionales
- Este documento se actualizará conforme el proyecto avance con pasos adicionales, como la creación de aplicaciones específicas dentro de Django o la configuración de otros componentes (por ejemplo, MetaTrader 5).
- Si encuentras problemas durante la configuración, consulta los archivos de documentación en `/docs` (como `DATABASE_SETUP.md` o `WORKFLOW.md`) para más detalles o busca ayuda en los canales de soporte del proyecto.

¡Con estos pasos, deberías tener el entorno básico configurado para comenzar a trabajar en Saturn Investments!