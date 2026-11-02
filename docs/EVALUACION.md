# Evaluación del modelo y de la guía

## Elegir una tarea antes de entrenar

Seleccionar enfermedad, territorios, definición de casos, cobertura y un horizonte inicial. Dos alternativas de experimento, todavía por decidir:

- **Conteo:** estimar casos notificados en una semana futura definida.
- **Incremento:** clasificar un aumento respecto a una referencia histórica especificada previamente.

Un umbral debe quedar fijado con entrenamiento y conocimiento del dominio antes de revisar prueba. No llamar «brote» a cualquier aumento sin una definición y sustento adecuados.

## Viabilidad del dataset

1. Auditar por país, enfermedad y semana las fechas, faltantes, revisiones y periodos comparables.
2. Mantener separados sospechosos, probables, confirmados y otras definiciones hasta justificar su combinación.
3. Identificar si las series son incidentes semanales o acumulados. Sus diferencias requieren revisar reinicios y correcciones.
4. Distinguir semanas sin notificación de ceros observados.
5. Registrar cuándo estuvo disponible cada variable. Si no existe historial de publicaciones, declarar la evaluación como retrospectiva con series revisadas.

Más filas de otros países no garantizan más ejemplos comparables. Las áreas con distinta vigilancia y definición se evalúan de forma separada antes de considerar un modelo conjunto.

## Validación temporal

- Entrenar con el pasado y reservar periodos posteriores para validación y prueba.
- Usar fechas de corte comunes a todos los territorios de cada partición; no repartir filas al azar.
- Evitar que las ventanas futuras de las etiquetas de entrenamiento invadan el periodo reservado. Considerar también el retraso de publicación de esas etiquetas.
- Ajustar imputación, escalado, selección y umbrales solo con entrenamiento.
- Hacer evaluación con orígenes móviles si la longitud de las series lo permite.
- Si se afirma transferencia a un país no visto, reservarlo también geográficamente y medir ese resultado por separado.
- Documentar qué hacer ante un país o una enfermedad sin cobertura suficiente.

## Referencias y aporte del clima

Comparar, según disponibilidad, persistencia del último valor y una referencia estacional. La referencia estacional exige historia comparable suficiente.

Evaluar la misma tarea, cortes y muestra en tres versiones:

1. Antecedentes epidemiológicos y calendario.
2. Los anteriores más variables meteorológicas.
3. Los anteriores más índices climáticos relacionados con El Niño, si son pertinentes.

Medir el cambio de error y su variación entre países y periodos. Si el clima no mejora el resultado, documentarlo; no atribuirle una mejora por la importancia de variables. No se infiere causalidad de esta comparación.

Los valores meteorológicos futuros observados no se usarán como si hubieran sido conocidos al emitir el pronóstico. Una evaluación con pronósticos meteorológicos necesita sus versiones disponibles en cada fecha de corte.

## Métricas

| Tarea | Evidencia propuesta |
| --- | --- |
| Conteo | MAE y error por país, enfermedad y horizonte frente al baseline; documentar el tratamiento de conteos negativos si el algoritmo puede producirlos |
| Clasificación de incremento | Precisión, recall, matriz de confusión y PR-AUC cuando las clases lo permitan |
| Intervalos | Cobertura y amplitud empíricas en periodos reservados; no mostrar intervalos sin un método evaluado |
| Probabilidad del evento epidemiológico | Calibración antes de mostrarla; no equivale a probabilidad personal del viajero |

Reportar cantidad de observaciones y eventos por grupo. Un promedio agregado no debe ocultar países con pocos datos o bajo desempeño. No hay métricas regionales validadas en el repositorio.

## Pruebas del producto

Comprobar: cruce de itinerario/semana, salida fuera del horizonte, escala nacional frente a ciudad, datos desactualizados, faltantes, avisos oficiales separados y varias paradas.

Con viajeros, medir realización de tareas, comprensión de las fuentes y distinción entre situación observada y estimación. El éxito de consulta o una buena métrica predictiva no demuestran reducción de infecciones.

## Evidencia del experimento

Guardar dataset y versión, periodos, objetivo, horizonte, variables disponibles al corte, baseline, parámetros, semilla, métricas por grupo, predicciones de prueba y limitaciones. Ver [models/README.md](../models/README.md) y [reports/README.md](../reports/README.md).

El notebook de regresión del piloto de Piura es exploratorio y usa una partición aleatoria; sus resultados no sustituyen esta evaluación temporal. Ver [Antecedentes](ANTECEDENTES.md).
