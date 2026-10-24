# Arquitectura propuesta

## Flujo

Fuentes históricas → validación y limpieza → tabla zona/semana → variables y objetivo → evaluación temporal → estimaciones → priorización → dashboard.

## Componentes

- `src/data/`: ingesta reproducible, normalización territorial, fechas y calidad.
- `src/features/`: rezagos, acumulados históricos y objetivo futuro.
- `src/models/`: baseline, modelo candidato, métricas e inferencia.
- `src/prioritization/`: ranking con criterios configurables y trazabilidad.
- `app/`: consulta y visualización; no entrenar en cada interacción.

Propuesta inicial: un proyecto Python con Streamlit. No se requiere todavía una API independiente ni una base de datos; decidirlo si los requisitos lo justifican.

## Contratos

Ver [datos](DATOS.md). Separar observaciones históricas, resultados predictivos y puntajes de prioridad. Cada resultado debe conservar zona, fecha de corte, horizonte, versión del modelo y origen de los datos.

## Estado real

Solo hay documentación y directorios. No se implementaron los componentes ni se seleccionaron versiones de dependencias.

## Registro de decisiones

Registrar fecha, contexto, alternativas, decisión y consecuencias para: unidad territorial, objetivo, horizonte, tecnologías, tratamiento de faltantes y criterios de priorización.
