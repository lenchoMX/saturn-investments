# Workflow de Saturn Investments

Este documento describe el flujo de trabajo para desarrollar y usar el proyecto.

## Desarrollo
1. **Configuración del Entorno:**
   - Instalar dependencias desde `/requirements/python.txt` y `/requirements/php.txt`.
   - Configurar TimescaleDB siguiendo `DATABASE_SETUP.md`.
2. **Importación de Datos:**
   - Usar scripts en `/src/markets/*/data` para importar datos financieros.
3. **Análisis y Visualización:**
   - Ejecutar análisis en `/src/markets/*/analysis` y generar gráficos en `/src/markets/*/viz`.
4. **Expert Advisors:**
   - Desarrollar y probar EAs en `/src/ea/forex/`.
5. **Frontend:**
   - Configurar y personalizar la interfaz en `/saturn-web`.

## Uso
- Acceder a la interfaz web en `/saturn-web` para visualizar datos y análisis.
- Consultar gráficos generados en `/output/charts`.

Más detalles se añadirán conforme avance el proyecto.