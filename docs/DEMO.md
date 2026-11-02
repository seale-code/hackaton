# Demo: guía climática y sanitaria del viajero

Este es el guion previsto. La aplicación todavía no está implementada.

## Historia a demostrar

Una persona prepara varias paradas por Sudamérica y necesita relacionar sus fechas con información sanitaria comprensible y trazable.

1. Introducir dos destinos y fechas; indicar si el itinerario es ficticio.
2. Mostrar qué escala y periodo cubre cada fuente.
3. Consultar el histórico de una enfermedad, diferenciando dato observado de faltante.
4. Si existe un modelo evaluado, mostrar una estimación dentro del horizonte y su referencia de evaluación.
5. Seleccionar una fecha fuera de ese horizonte y comprobar que se muestra contexto histórico, sin extender el pronóstico.
6. Consultar avisos y orientación oficial con fuente y fecha.
7. Abrir un destino sin cobertura y mostrar información insuficiente.
8. Revisar el resumen por parada y explicar los límites del resultado.

No elegir países para la presentación como si ya estuvieran integrados. La selección depende del inventario de datos.

## Evidencia para acompañar la presentación

| Afirmación | Evidencia necesaria |
| --- | --- |
| «Tenemos datos de estos países» | Archivos, catálogo y cobertura por territorio/enfermedad |
| «El modelo anticipa aumentos» | Objetivo, horizonte, prueba temporal y comparación con baseline |
| «El clima mejora el resultado» | Comparación con/sin clima usando los mismos cortes y muestra |
| «La guía facilita planificar» | Tareas y resultados de pruebas con viajeros |
| «Mostramos orientación oficial» | URL, organismo, fecha, ámbito y revisión del contenido |

## Condiciones de presentación

Datos reales, ejemplos sintéticos y estimaciones deben identificarse. Si la demo usa un corte histórico, no presentarlo como situación actual. No convertir los errores de un notebook exploratorio en métricas validadas ni atribuir a una simulación efectos en salud.

La información sanitaria oficial y la señal del modelo se muestran por separado. El prototipo no calcula la probabilidad individual de infección ni certifica un destino como seguro.
