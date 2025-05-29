# Documentación de Uso de `core_app`

El `core_app` es una aplicación central en el proyecto **Saturn Investments** que gestiona las entidades financieras soportadas, como pares de divisas, commodities, acciones, tasas de interés y criptomonedas. Su propósito es centralizar la información sobre estas entidades para que pueda ser utilizada de manera dinámica en las demás aplicaciones del proyecto (como `forex_app`, `commodities_app`, etc.).

## Funcionalidades Principales

- **Gestión de Entidades Soportadas**: Permite agregar, editar y eliminar entidades financieras a través del panel de administración de Django.
- **Consulta Dinámica**: Las vistas y templates de otras aplicaciones pueden consultar las entidades activas para generar dropdowns, reportes, gráficos y estadísticas sin necesidad de actualizar manualmente el código.
- **Escalabilidad**: Facilita la adición de nuevas entidades o mercados sin modificar la lógica de las aplicaciones existentes.

## Cómo Usar `core_app`

### 1. Acceso al Panel de Administración
- Inicia sesión en el panel de administración de Django (`http://127.0.0.1:8000/admin/`).
- En la sección "Core App", selecciona "Entidades Soportadas" para gestionar las entidades financieras.

### 2. Agregar una Nueva Entidad
- Haz clic en "Añadir Entidad Soportada".
- Completa los campos:
  - **Nombre**: Símbolo de la entidad (e.g., `EUR/USD`, `XAU/USD`, `AAPL`).
  - **Tipo de Entidad**: Selecciona el tipo correspondiente (e.g., "Par de divisas", "Commodity").
  - **Descripción**: Opcional, para añadir detalles (e.g., "Oro vs Dólar").
  - **Activo**: Marca si la entidad está activa y debe ser visible en las aplicaciones.
- Guarda la entidad.

### 3. Consultar Entidades en Otras Aplicaciones
- Las vistas en aplicaciones como `forex_app` pueden consultar las entidades activas. Por ejemplo:
  ```python
  from core_app.models import SupportedEntity
  currency_pairs = SupportedEntity.objects.filter(entity_type='currency_pair', active=True)
  ```
- En los templates, las entidades se pueden mostrar dinámicamente:
  ```html
  <select name="currency_pair">
      {% for pair in currency_pairs %}
          <option value="{{ pair.name }}">{{ pair.name }}</option>
      {% endfor %}
  </select>
  ```

### 4. Filtrar y Buscar Entidades
- En el panel de administración, puedes filtrar entidades por tipo y estado (activo/inactivo).
- Usa la búsqueda para encontrar entidades por nombre o descripción.

## Ejemplo de Uso
Supongamos que deseas añadir un nuevo par de divisas (`USD/JPY`) para Forex:
1. Accede al admin y añade una nueva entidad con nombre `USD/JPY`, tipo "Par de divisas", y marca como activa.
2. En la vista `forex_index` de `forex_app`, el dropdown automáticamente incluirá `USD/JPY` sin necesidad de modificar el código.

Este enfoque asegura que todas las secciones del proyecto (reportes, gráficos, etc.) usen la misma información actualizada de las entidades soportadas.