# Producto y experiencia del viajero

## Problema que se quiere validar

Una persona que prepara varias paradas necesita relacionar destinos y fechas con información sanitaria procedente de diferentes fuentes. La propuesta busca hacer esa consulta comprensible y trazable. No hay todavía entrevistas ni pruebas con viajeros documentadas en este repositorio.

Pregunta central: **¿qué situación sanitaria debería conocer para los lugares y las fechas de mi recorrido y dónde consulto orientación oficial?**

## Recorrido propuesto

1. Introducir destinos y fechas de llegada/salida.
2. Revisar la escala territorial y cobertura de cada parada.
3. Consultar históricos, situación reciente y estacionalidad.
4. Ver estimaciones aplicables al periodo, cuando existan y hayan sido evaluadas.
5. Acceder a orientación oficial y obtener un resumen del itinerario.

## Historias de usuario propuestas

Son especificaciones para implementar, no funcionalidades terminadas.

| ID | Historia | Aceptación principal |
| --- | --- | --- |
| HU-01 | Como viajero, quiero registrar varias paradas y fechas para consultar mi recorrido. | Validar llegada anterior a salida y permitir editar el orden; avisar sobre solapamientos sin modificar fechas silenciosamente. |
| HU-02 | Quiero consultar la situación epidemiológica de cada destino. | Mostrar enfermedad, escala, periodo observado, definición del conteo y fuente. |
| HU-03 | Quiero saber si una tendencia estimada cubre mis fechas. | Mostrar predicción solo si área, enfermedad y semanas están dentro de la cobertura del modelo. |
| HU-04 | Quiero acceder a orientación de autoridades sanitarias. | Cada contenido conserva URL, organismo, fecha de revisión y territorio de aplicación. |
| HU-05 | Quiero reconocer información insuficiente o antigua. | Faltantes y desactualización aparecen como estados propios, sin convertirlos en riesgo bajo. |
| HU-06 | Quiero consultar un viaje lejano sin recibir falsa precisión. | Fuera del horizonte se muestran históricos/estacionalidad y avisos, sin extrapolar estimaciones. |
| HU-07 | Quiero entender por qué aparece una señal. | Distinguir incremento observado, estimación experimental y aviso de una autoridad; no mezclar sus niveles. |
| HU-08 | Quiero comparar fechas o recorridos alternativos. | Ampliación: mantener las mismas escalas, enfermedades y fechas de corte, mostrando límites de comparación. |

## Pantallas previstas

| Pantalla | Contenido |
| --- | --- |
| Mi recorrido | Formulario de paradas y calendario |
| Panorama por destino | Mapa/listado, cobertura y situación epidemiológica |
| Detalle de una parada | Serie, periodo, estimaciones disponibles, incertidumbre y fuentes |
| Preparación del viaje | Orientación y enlaces oficiales relevantes |
| Resumen | Fichas por parada y recordatorio de la fecha de consulta |

No se muestra una probabilidad personal de contagio. No se usarán expresiones como «viaje libre de enfermedades» o «destino seguro» derivadas de un puntaje del prototipo.

## Estados que la interfaz debe representar

- `observed_only`: solo hay información observada utilizable.
- `forecast_available`: existe una estimación evaluada para el destino y periodo.
- `outside_horizon`: el viaje excede el horizonte validado.
- `insufficient_data`: no se puede producir el resultado solicitado.
- `stale_data`: la antigüedad supera el criterio documentado para la fuente.

La existencia y vigencia de avisos oficiales se muestra por separado. «Sin avisos encontrados» no equivale a «sin riesgo».

## Validación de utilidad

Probar si una persona identifica fuente, fecha, escala y límites del resultado; si consigue reunir orientación para sus paradas y si distingue un aviso oficial de un pronóstico experimental. Registrar participantes, tareas y resultados sin atribuir al producto reducciones de enfermedad no medidas.
