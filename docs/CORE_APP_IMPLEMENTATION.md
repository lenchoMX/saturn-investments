# Implementación de `core_app` en Saturn Investments

Este documento proporciona instrucciones paso a paso para implementar la aplicación `core_app` en el proyecto **Saturn Investments** usando Visual Studio Code (VSCode). Asegúrate de seguir cada paso cuidadosamente para integrar correctamente el `core_app` con las demás aplicaciones.

## Requisitos Previos
- Tener el proyecto **Saturn Investments** clonado y configurado en VSCode.
- Estar en el entorno virtual `saturn` activado.
- Tener Django y las dependencias instaladas (según `requirements.txt`).
- Tener acceso al panel de administración de Django.

## Pasos para Implementar `core_app`

### 1. Crear la Aplicación `core_app`
- Abre VSCode y navega al directorio raíz del proyecto (`/saturn-investments/`).
- Abre la terminal integrada en VSCode (`Terminal > New Terminal`).
- Asegúrate de que el entorno virtual esté activado:
  - En Windows: `saturn\Scripts\activate.bat`
  - En Linux/macOS: `source saturn/bin/activate`
- Ejecuta el siguiente comando para crear la aplicación:
  ```bash
  python manage.py startapp core_app
  ```
- Esto generará la carpeta `core_app` en `/saturn-investments/core_app/`.

### 2. Definir el Modelo en `core_app`
- Abre el archivo `/saturn-investments/core_app/models.py` en VSCode.
- Añade el siguiente código para definir el modelo `SupportedEntity`:
  ```python
  from django.db import models

  class SupportedEntity(models.Model):
      ENTITY_TYPES = (
          ('currency_pair', 'Par de divisas'),
          ('commodity', 'Commodity'),
          ('equity', 'Acción'),
          ('interest_rate', 'Tasa de interés'),
          ('cryptocurrency', 'Criptomoneda'),
      )

      name = models.CharField(max_length=10, unique=True, help_text="Ejemplo: EUR/USD, XAU/USD, AAPL")
      entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES, help_text="Tipo de entidad")
      description = models.CharField(max_length=100, blank=True, help_text="Descripción opcional")
      active = models.BooleanField(default=True, help_text="Indica si la entidad está activa")
      created_at = models.DateTimeField(auto_now_add=True)

      def __str__(self):
          return self.name

      class Meta:
          verbose_name = "Entidad Soportada"
          verbose_name_plural = "Entidades Soportadas"
  ```
- Guarda el archivo.

### 3. Registrar el Modelo en el Admin
- Abre `/saturn-investments/core_app/admin.py`.
- Añade el siguiente código:
  ```python
  from django.contrib import admin
  from .models import SupportedEntity

  @admin.register(SupportedEntity)
  class SupportedEntityAdmin(admin.ModelAdmin):
      list_display = ('name', 'entity_type', 'active', 'created_at')
      list_filter = ('entity_type', 'active')
      search_fields = ('name', 'description')
  ```
- Guarda el archivo.

### 4. Actualizar `settings.py`
- Abre `/saturn-investments/saturn_project/saturn_project/settings.py`.
- En la lista `INSTALLED_APPS`, añade `'core_app'`, así:
  ```python
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'forex_app',
      'commodities_app',  # Si ya existe
      'core_app',  # Añade esta línea
  ]
  ```
- Guarda el archivo.

### 5. Migrar la Base de Datos
- En la terminal de VSCode, ejecuta:
  ```bash
  python manage.py makemigrations core_app
  python manage.py migrate
  ```
- Verifica que no haya errores y que la tabla `core_app_supportedentity` se cree en la base de datos.

### 6. Integrar `core_app` en `forex_app`
- Abre `/saturn-investments/forex_app/views.py`.
- Modifica o crea una vista como `forex_index`:
  ```python
  from django.shortcuts import render
  from core_app.models import SupportedEntity

  def forex_index(request):
      currency_pairs = SupportedEntity.objects.filter(entity_type='currency_pair', active=True)
      context = {'currency_pairs': currency_pairs}
      return render(request, 'forex_app/index.html', context)
  ```
- Abre o crea `/saturn-investments/forex_app/templates/forex_app/index.html` y añade:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Forex - Saturn Investments</title>
  </head>
  <body>
      <h1>Pares de Divisas Disponibles</h1>
      <select name="currency_pair">
          {% for pair in currency_pairs %}
              <option value="{{ pair.name }}">{{ pair.name }}</option>
          {% endfor %}
      </select>
  </body>
  </html>
  ```
- Asegúrate de que la URL esté configurada en `/saturn-investments/forex_app/urls.py`:
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('', views.forex_index, name='forex_index'),
  ]
  ```

### 7. Probar la Implementación
- Inicia el servidor con:
  ```bash
  python manage.py runserver
  ```
- Accede a `http://127.0.0.1:8000/admin/` y añade algunas entidades (e.g., `EUR/USD`, `USD/JPY`).
- Ve a `http://127.0.0.1:8000/forex/` y verifica que el dropdown muestre las entidades.

¡Con estos pasos, `core_app` estará completamente implementado y listo para ser utilizado en el proyecto!