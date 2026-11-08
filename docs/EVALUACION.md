# Experimento retrospectivo del piloto

## Tarea y ejecución

Objetivo: conteo semanal **confirmado** de dengue, a 1 y 2 semanas, por separado para Piura, Sullana, Morropón y Paita. Ejecutar desde la raíz:

```bash
python -m src.models.evaluate --output reports/nueva_evaluacion
```

El directorio debe ser nuevo. Se guardan predicciones individuales, métricas por provincia/horizonte/partición/modelo y manifiesto del dataset y parámetros. [Ejecución disponible](../reports/evaluacion_piloto_2026-11-08/README.md).

## Método implementado

- Datos: snapshot original en revisión; se excluyen ejemplos con faltantes o años marcados sin casos registrados.
- Cada provincia se reindexa por fechas semanales, conservando huecos como faltantes. Una ausencia no se convierte en la semana siguiente ni en cero.
- Origen al cierre de la semana; objetivo h semanas después. Entrenamiento 2001–2021, validación 2022–2023 y prueba 2024. Las semanas completas de origen y objetivo deben estar dentro de su bloque (incluido el sábado final) para evitar que etiquetas de entrenamiento invadan validación.
- Variables de historia: conteo en origen, rezagos de 1, 2 y 3 semanas, seno y coseno de la fase anual. La alternativa climática añade temperaturas máxima/mínima y lluvia de la semana de origen.
- Referencias: persistencia (último conteo) y estacional de 52 semanas antes del objetivo. La referencia de 52 semanas es una aproximación, no una alineación exacta de semana epidemiológica entre años.
- Candidatos: StandardScaler ajustado solo en entrenamiento + Ridge(alpha=1.0), con y sin clima. Parámetro fijado de antemano, sin búsqueda ni reajuste sobre prueba. Predicciones negativas recortadas a cero.
- Todos los métodos se comparan sobre las mismas fechas completas; la necesidad de historia estacional limita también la muestra de los otros métodos.
- Métrica: MAE (casos por semana), número de predicciones y tamaño de entrenamiento. No se usan porcentajes de precisión ni probabilidad individual.

## Lo que este experimento no comprueba

No se reconstruyeron retrasos de notificación/publicación de casos ni disponibilidad histórica del clima. Se asumen disponibles al cierre de semana: es una evaluación retrospectiva con series revisadas, no una simulación operativa fiel. El conjunto incluye ceros antiguos sin justificar y un calendario provisional; ninguna métrica resuelve esas limitaciones.

2025 no se usa como prueba en esta primera ejecución. Para iterar tras observar 2024 será necesario otro periodo reservado; ya no puede tratarse como una prueba nueva no vista. El notebook anterior de partición aleatoria queda como antecedente, sin reutilizar sus métricas.

No hay intervalos, avisos sanitarios automáticos ni predicciones en la interfaz. La utilidad con viajeros y la contribución climática deben evaluarse separadamente; una mejora en una provincia no se generaliza al resto.
