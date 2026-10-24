# Priorización y proceso de decisión

## Propósito

Transformar estimaciones de riesgo en un ranking transparente para explorar dónde concentrar la atención. El puntaje de prioridad es distinto de la probabilidad predictiva.

## Diseño pendiente

Evaluar riesgo, población expuesta, incidencia, vulnerabilidad y recursos/costos, solo cuando existan datos adecuados. Definir normalización, dirección de cada criterio, pesos, tratamiento de faltantes y desempates. Los pesos ilustrativos de los chats no son parámetros aprobados.

Ingeniería Industrial define y justifica los criterios y el flujo operativo; Informática implementa y comprueba los cálculos. Probar cómo cambia el ranking al modificar los pesos.

## Flujo previsto

Datos → estimación → revisión de calidad → priorización → revisión humana → propuesta de acción → seguimiento.

Documentar quién recibe la información, quién decide, qué restricciones existen y qué indicadores se pueden medir. En el MVP no se envían alertas oficiales ni se asignan recursos reales.

## Criterios de aceptación

- Varias zonas de Piura con datos comparables.
- Puntajes reproducibles y componentes visibles.
- Sin pesos o costos presentados como validados si son supuestos.
- Si faltan datos, mostrar la limitación o desactivar el ranking.
- Una clasificación ponderada se describe como ranking; solo hablar de optimización si se implementan objetivo y restricciones explícitas.
