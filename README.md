# Alerta temprana de dengue en Piura

Prototipo de hackatón para integrar casos históricos de dengue, variables climáticas e indicadores de El Niño, estimar riesgo futuro y apoyar la priorización de zonas de Piura.

**Flujo previsto:** datos → predicción → explicación → priorización → dashboard.

> Estado: estructura y documentación de trabajo. No hay todavía datos descargados, modelo entrenado, aplicación ejecutable ni resultados validados.

## Alcance

El piloto se enfoca en **Piura**. La selección de provincias o distritos dependerá de la cobertura y calidad de los datos. La ampliación a otras regiones queda fuera del MVP.

El dashboard previsto mostrará evolución histórica, riesgo estimado, factores asociados al modelo y un ranking de zonas. La definición de riesgo, el horizonte y los umbrales deben cerrarse con el equipo y el mentor antes del entrenamiento.

## Organización

| Ruta | Responsabilidad |
| --- | --- |
| `data/` | Guías para datos originales, intermedios, procesados y ejemplos |
| `notebooks/` | Exploración y experimentos reproducibles |
| `src/data/` | Limpieza, validación e integración de fuentes |
| `src/features/` | Variables temporales y objetivo predictivo |
| `src/models/` | Entrenamiento, evaluación e inferencia |
| `src/prioritization/` | Criterios y cálculo del ranking de zonas |
| `app/` | Dashboard; Streamlit es la propuesta de trabajo |
| `models/` | Metadatos de modelos y referencia a artefactos |
| `reports/` | Métricas, figuras y evidencias de evaluación |
| `tests/` | Pruebas de datos, tiempo, inferencia y priorización |
| `docs/` | Alcance, arquitectura, fuentes, equipo y demo |
| `scripts/` | Automatizaciones reproducibles |
| `.github/` | Plantillas de issues y pull requests |

Las carpetas contienen guías iniciales, no módulos implementados.

## Documentación

- [Alcance y decisiones pendientes](docs/ALCANCE.md)
- [Arquitectura propuesta](docs/ARQUITECTURA.md)
- [Fuentes y contrato de datos](docs/DATOS.md)
- [Evaluación del modelo](docs/EVALUACION.md)
- [Priorización y proceso de decisión](docs/PRIORIZACION.md)
- [Distribución del trabajo](docs/EQUIPO.md)
- [Roadmap](docs/ROADMAP.md)
- [Guion de demo](docs/DEMO.md)
- [Cómo colaborar](CONTRIBUTING.md)

## Tecnologías propuestas

Python, pandas, scikit-learn, Streamlit y Plotly. Random Forest como candidato junto con un baseline sencillo; XGBoost y SHAP son opcionales. Estas son propuestas recogidas de la planificación, no dependencias instaladas ni decisiones técnicas cerradas.

Los comandos de instalación y ejecución se documentarán al implementar la primera versión. No se incluye un comando de arranque que todavía no funcione.

## Primer paso

Comprobar si las fuentes permiten construir una serie por zona y semana en Piura. A partir de esa evidencia, cerrar la unidad geográfica, el objetivo y el horizonte. Si solo hay datos departamentales, podrá evaluarse una serie de Piura, pero no un ranking real entre distritos.

## Uso de resultados

Prototipo académico para evaluación retrospectiva y demostración. Las salidas no constituyen alertas oficiales ni decisiones de intervención. Distinguir siempre datos reales, ejemplos sintéticos y estimaciones del modelo.
