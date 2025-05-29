# Listado de Expert Advisors (EAs) de Saturn Investments

Este documento describe los Expert Advisors (EAs) utilizados en el proyecto **Saturn Investments**, escritos en MQL5 para MetaTrader 5. Cada EA incluye una descripción de su propósito y funcionalidad, para facilitar su reutilización y modificación.

## EAs Disponibles

### 1. `calendar_ea.mq5`
- **Ubicación**: `/shared/mt5_scripts/eas/calendar_ea.mq5`
- **Propósito**: Extrae el calendario económico de MetaTrader 5 y genera un archivo CSV con eventos financieros, incluyendo fecha, país, nombre del evento, impacto (alto, medio, bajo), y valores actual/pronosticado/anterior.
- **Uso**: 
  - Ejecutar en MetaTrader 5 para generar `mt5_calendar.csv` en `MQL5/Files`.
  - Importar el CSV en `economic_events_app` para análisis.
- **Estado**: Pendiente de implementación.
- **Notas para modificación**:
  - Añadir filtros por impacto o moneda.
  - Incluir más detalles del evento (ej. descripción).

### 2. [Placeholder para futuros EAs]
- **Ubicación**: `/shared/mt5_scripts/eas/`
- **Propósito**: [Por definir]
- **Uso**: [Por definir]