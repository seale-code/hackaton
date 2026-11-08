> **Estado del piloto (08/11/2026):** el alcance implementado está en [ALCANCE.md](ALCANCE.md). Las propuestas regionales de este documento son ampliaciones futuras, no cobertura disponible. La implementación y las fuentes consumidas se detallan en [README](../README.md) y [DATOS.md](DATOS.md).

# Comparación de destinos e itinerarios

Este documento reemplaza la priorización territorial de recursos sanitarios del enfoque anterior. Se conserva su ruta para mantener los enlaces del repositorio.

## Decisión del viajero

Relacionar las fechas de cada parada con información epidemiológica y orientación oficial. La comparación de itinerarios es una posible ampliación; el núcleo del MVP es consultar el recorrido y reconocer sus límites.

## Criterios propuestos

- Cobertura, escala territorial y antigüedad de las fuentes.
- Situación notificada y tendencia respecto al historial de la propia zona.
- Existencia y vigencia de avisos oficiales aplicables.
- Cobertura temporal de una estimación evaluada.
- Restricciones de presupuesto y duración, solo si el usuario las aporta y se implementa esa ampliación.

No ordenar países por número bruto de casos: población, vigilancia y definiciones pueden ser diferentes. Tampoco considerar un país sin notificaciones como la alternativa más segura.

## Comparación transparente

Presentar las alternativas en una tabla, manteniendo enfermedad, corte y escalas compatibles. Mostrar los criterios por separado. No definir un índice compuesto con pesos inventados ni sumar niveles de avisos oficiales de distintas enfermedades.

Si se incorpora un puntaje experimental, sus componentes, normalización, faltantes y sensibilidad deben quedar documentados y validados. Dicho puntaje no certifica seguridad sanitaria.

## Qué se necesitaría para optimizar

Una optimización formal requiere objetivo, variables de decisión y restricciones explícitas. Ejemplo de ampliación: comparar recorridos que cumplen fechas, presupuesto y destinos requeridos, mostrando junto a cada opción la información sanitaria disponible. Los costos, tiempos y reglas tendrían que obtenerse y verificarse; no existen todavía en el repositorio.

No se recomienda cancelar, cambiar o autorizar un viaje basándose únicamente en el modelo. Las indicaciones de una autoridad se atribuyen a esa autoridad y no se reemplazan por el puntaje del prototipo.

## Aporte de Ingeniería Industrial

Diseñar el proceso de planificación, elegir criterios comprensibles, analizar restricciones y evaluar utilidad con viajeros. La evaluación incluye si la persona puede interpretar diferencias sin confundir datos insuficientes con riesgo bajo.
