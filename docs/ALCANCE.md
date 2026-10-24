# Alcance del MVP

## Contexto recuperado

Esta documentación recoge lo tratado en los chats «Preguntas Para Mentor» y «Nombres para hackatón», revisados el 24 de octubre de 2026. Se conserva la última indicación explícita: enfocarse solo en Piura. Los chats son antecedentes de planificación, no evidencia de disponibilidad de datos ni validación científica.

## Problema y objetivo

Anticipar incrementos de dengue en zonas de Piura a partir de información epidemiológica y climática, incluyendo indicadores de El Niño, y convertir las estimaciones en una priorización explicable.

Usuarios previstos: equipos que analizan información para prevención y planificación territorial. Validar necesidades y flujo con el mentor; no se ha documentado validación con usuarios finales.

## MVP previsto

1. Integrar datos históricos de dengue, clima e indicadores de El Niño.
2. Entrenar y comparar un baseline con un modelo predictivo sencillo.
3. Mostrar en un dashboard histórico, estimaciones, limitaciones y factores del modelo.
4. Ordenar zonas mediante criterios transparentes de priorización.

## Decisiones abiertas

| Decisión | Estado |
| --- | --- |
| Región piloto | Piura, según última indicación del usuario |
| Unidad geográfica | Provincias o distritos, según datos disponibles |
| Objetivo | Elegir incremento de casos, número de casos o evento definido de riesgo |
| Horizonte | Se propuso 2–4 semanas; falta elegir uno y justificarlo |
| Riesgo bajo/medio/alto | Definición y umbrales pendientes |
| Tecnologías | Python + pandas + scikit-learn + Streamlit + Plotly propuestos |
| Priorización | Variables, pesos y restricciones pendientes de validación |

## Fuera del MVP

Cobertura nacional, alertas operativas automáticas, asignación real de recursos, predicciones clínicas individuales y optimización compleja. Otras regiones, XGBoost y SHAP quedan como posibles ampliaciones.

## Criterios de aceptación

- Dataset reproducible con fuentes, fechas, cobertura y faltantes documentados.
- Evaluación temporal en periodos no usados para ajustar el modelo.
- Comparación con baseline y limitaciones visibles, aunque no exista mejora.
- Dashboard que identifique fecha de corte, horizonte y procedencia de los datos.
- Ranking reproducible con criterios explícitos, solo si hay varias zonas comparables.
- Demo completa sin presentar cifras sintéticas como resultados reales.
