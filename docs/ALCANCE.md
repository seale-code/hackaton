# Alcance: guía del viajero en Sudamérica

## Definición actual

Guía inteligente que reúne información sobre dengue, Zika y chikungunya según los destinos y las fechas de un viaje por Sudamérica. Combinaría datos epidemiológicos, estacionalidad e información climática con orientación oficial y estimaciones a corto plazo cuando existan datos y evaluación suficientes.

El usuario principal es el viajero. El sistema apoya la preparación informada del recorrido. Las estimaciones corresponden a zonas y periodos, no a la probabilidad individual de infección.

## Dirección confirmada y propuestas de implementación

| Aspecto | Estado |
| --- | --- |
| Producto | Guía para viajeros según destinos y fechas; dirección actual del proyecto |
| Ámbito de la idea | Sudamérica; reemplaza el enfoque exclusivo en Piura |
| Enfermedades de interés | Dengue, Zika y chikungunya |
| Fuentes y modelo | Integración de información epidemiológica y climática; implementación pendiente |
| Países del primer piloto | Por seleccionar mediante inventario de datos |
| Tamaño del piloto | Dos o tres países como propuesta, no como cobertura disponible |
| Enfermedad del primer modelo | Por elegir según cantidad, continuidad y comparabilidad de registros |
| Unidad geográfica | País inicialmente; nivel subnacional solo si la fuente lo permite |
| Objetivo del modelo | Aumento de casos o conteo futuro; debe elegirse uno antes de entrenar |
| Horizonte | 2–4 semanas como propuesta a validar; un horizonte inicial se fijará en la ficha del experimento |
| Nombre de marca | Pendiente; no se adopta un nombre definitivo en esta actualización |
| Stack | Python + pandas + scikit-learn + Streamlit + Plotly propuestos |

## Primera versión propuesta

1. Itinerario de varias paradas con fechas de llegada y salida.
2. Ficha por destino con serie histórica, situación notificada y fecha de corte.
3. Tendencia predictiva para una enfermedad y territorios evaluados, cuando corresponda.
4. Orientación y avisos oficiales con enlaces, fechas y ámbito territorial.
5. Indicación explícita de cobertura insuficiente, faltantes y fechas fuera del horizonte.
6. Resumen del recorrido que mantenga separados históricos, avisos y estimaciones.

No se necesita una cuenta de usuario ni datos clínicos personales para demostrar este recorrido.

## Criterios de aceptación del MVP

- Cada parada se vincula a un identificador territorial y a la escala realmente disponible.
- No se asignan valores de una serie nacional como si fueran observaciones de una ciudad.
- Cada dato o aviso tiene fuente, periodo y fecha de actualización visibles.
- Las estimaciones tienen fecha de corte, horizonte, objetivo y referencia de evaluación.
- El modelo se compara con un baseline en periodos posteriores al entrenamiento.
- Fechas fuera del horizonte muestran contexto histórico y avisos, sin extender predicciones.
- Si no existe cobertura, el resultado indica información insuficiente y no una categoría de seguridad.
- La demo distingue datos reales, sintéticos y resultados experimentales.
- La experiencia se prueba con usuarios potenciales antes de afirmar utilidad demostrada.

## Ampliaciones posibles

Comparar fechas o itinerarios alternativos, ampliar países o enfermedades, integrar datos subnacionales y analizar presupuesto/duración. Una optimización formal requeriría función objetivo, restricciones, datos y evaluación propios; no está implementada.

## Fuera del alcance inicial

Diagnóstico, cálculo de probabilidad personal de infección, prescripción de vacunas o medicamentos, certificación de destinos seguros, alertas oficiales propias, cobertura subnacional de todo el continente y pronósticos para fechas lejanas sin validación.

El envío de notificaciones y el uso de integraciones privadas como NOTI o Netlab no forman parte del alcance acordado.

## Relación con el reto

La contribución temática se plantea en clima y preparación frente a riesgos sanitarios. Se evaluará el aporte del clima frente a un modelo que use solo antecedentes epidemiológicos. El agua tiene un vínculo ambiental indirecto; no se propone gestionar infraestructura hídrica. La aceptación en la categoría requiere contrastar las bases oficiales de la hackatón.
