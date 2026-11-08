# Evaluación ejecutada · 08/11/2026

Experimento retrospectivo sobre el snapshot en revisión. MAE en casos confirmados por semana: menor es mejor. Entrenamiento 2001–2021; validación 2022–2023; prueba 2024. No es una estimación de riesgo individual ni una validación operativa.

| Provincia | Horizonte | Persistencia | Estacional 52 | Ridge historia | Ridge + clima |
|---|---:|---:|---:|---:|---:|
| MORROPON | 1 semana(s) | 9.48 | 121.74 | 9.21 | 9.23 |
| MORROPON | 2 semana(s) | 13.47 | 123.61 | 13.09 | 13.11 |
| PAITA | 1 semana(s) | 19.66 | 154.88 | 20.33 | 20.18 |
| PAITA | 2 semana(s) | 31.69 | 157.65 | 34.43 | 34.18 |
| PIURA | 1 semana(s) | 56.28 | 687.68 | 48.38 | 48.18 |
| PIURA | 2 semana(s) | 92.96 | 700.37 | 77.50 | 74.57 |
| SULLANA | 1 semana(s) | 14.14 | 269.86 | 12.98 | 13.40 |
| SULLANA | 2 semana(s) | 19.04 | 274.55 | 16.21 | 15.48 |

Hay 50 objetivos de prueba a una semana y 49 a dos semanas por provincia, después de exigir que las semanas de origen y objetivo estén completas dentro de 2024. Validación: 103 y 102 respectivamente. Se evalúan todos los métodos sobre las mismas fechas.

El resultado es mixto: en Paita, persistencia supera ambos Ridge en prueba; en Morropón, añadir clima no mejora Ridge de historia. En Sullana, su aporte cambia con el horizonte. No se afirma una mejora general del clima ni se selecciona un modelo operativo con esta tabla.

Los 5.376 registros originales no se alteraron. Se excluyeron ejemplos de años marcados sin casos, pero los ceros restantes siguen pendientes de auditoría. No se reconstruyeron retrasos de publicación; el clima y los conteos se asumen conocidos al cierre de semana. Calendario y representatividad espacial siguen siendo provisionales.

Archivos: `metricas.csv` (64 grupos), `predicciones.csv` (cada predicción), `manifest.json` (hash, cortes, variables y límites). Reproducir en un directorio nuevo:

```bash
python -m src.models.evaluate --output reports/reproduccion_piloto
```

La aplicación muestra históricos y no carga estas predicciones. Ver [método completo](../../docs/EVALUACION.md).
