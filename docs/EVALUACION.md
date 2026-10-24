# Plan de evaluación

## Antes de entrenar

Definir el evento objetivo, unidad geográfica, fecha de corte y horizonte. «Riesgo alto» necesita una definición observable; no elegir umbrales después de ver los resultados de prueba.

## Comparación temporal

- Reservar el periodo final como prueba y usar periodos anteriores para entrenamiento y validación.
- Separar por fecha todas las zonas para evitar mezclar semanas futuras en el entrenamiento.
- Dejar una separación suficiente para que las ventanas futuras de las etiquetas de entrenamiento no invadan validación o prueba.
- Ajustar imputación, escalado y selección de variables solo con entrenamiento.
- Calcular rezagos usando exclusivamente información disponible en la fecha de corte.
- Comparar con un baseline adecuado al objetivo y a la estacionalidad.

## Métricas según el objetivo

Para conteos: reportar MAE y error por zona/periodo frente a persistencia o referencia estacional. Para clasificación: reportar precisión, recall, matriz de confusión y PR-AUC cuando corresponda. Si se muestran probabilidades, evaluar calibración. No mezclar métricas de tareas diferentes como si fueran intercambiables.

## Explicación

La importancia global de variables no explica por sí sola una predicción particular ni demuestra causalidad. Mostrarla como resumen del modelo. Las explicaciones locales requieren un método específico y comprobaciones adicionales.

## Evidencia a guardar

Versión del dataset, fechas de partición, parámetros, semilla, métricas, comparación con baseline, faltantes y limitaciones. Registrar también si el modelo no mejora al baseline. Actualmente no hay resultados ni rendimiento demostrado.
