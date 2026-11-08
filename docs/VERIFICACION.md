# Verificación de esta entrega

- Instalación desde `requirements-dev.txt` en un entorno Python 3.12 limpio: correcta.
- Suite de pytest y AppTest: 29 pruebas aprobadas.
- Auditoría estructural del snapshot: 5.376 filas, sin duplicados de clave ni huecos entre las fechas de cada provincia. Esto no acredita cobertura epidemiológica real: hay rellenos históricos.
- Evaluación ejecutada: métricas, predicciones y manifiesto en `reports/evaluacion_piloto_2026-11-08/`. Se purgan semanas objetivo cuyo sábado exceda el corte del bloque.
- CSV históricos y notebooks preservados; los cambios de ingesta producen nuevas salidas y no regeneran automáticamente las anteriores.
- Pruebas de adquisición: CSV sintéticos locales y respuesta meteorológica simulada. No se descargaron de nuevo los recursos oficiales ni se validó su esquema vigente.
- Interfaz: arranque, cambio de provincia, consulta futura y fechas invertidas comprobados con AppTest. La revisión visual en navegador quedó pendiente porque el navegador de la sesión no pudo acceder al servidor local.
- Sin pruebas con viajeros, alertas oficiales en vivo ni pronóstico operativo.

Los resultados de GitHub Actions deben consultarse en el pull request; no se confunden con las comprobaciones locales.

## Ampliación de malaria

- Suite completa: 45 pruebas aprobadas (incluye los 29 casos anteriores).
- Catálogo de malaria: 22 archivos, 181.578 filas. Los CSV originales no se modificaron.
- Auditoría reproducible de hashes y valores en `reports/malaria/`. Se conservan 2.744 filas con bandera de revisión, incluidas 18 con valores positivos (suma 167).
- Interfaz comprobada con AppTest: cambio de enfermedad, departamento, periodo, año y regreso a dengue. La revisión visual en navegador sigue siendo una comprobación independiente.
- La solicitud de descarga oficial devolvió HTTP 418; no se afirma una nueva validación de la fuente. Se usan los archivos históricos del equipo.
