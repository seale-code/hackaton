# Antecedentes y estado comprobable

## Cambio de producto

El proyecto comenzó con un piloto de dengue y clima en Piura. La dirección actual es una guía climática y sanitaria para viajeros por Sudamérica según destino y fecha.

Se conservan los datos, scripts y notebooks aportados por el equipo. La actualización de documentación no cambia sus valores ni los adapta automáticamente al nuevo producto. Piura puede servir como caso de exploración, pero dejó de ser el único ámbito del proyecto.

## Material existente

| Material | Evidencia en el repositorio | Límite de uso |
| --- | --- | --- |
| [Casos de dengue por provincia](../src/data/casos_dengue_piura/) | Ocho CSV del procesamiento previo | Son provincias de Piura, no distritos ni cobertura regional de Sudamérica |
| [Scripts y salidas exploratorias](../scripts/test/) | Descargas de epidemiología y meteorología; CSV por provincia | Rutas y calendarios anteriores por revisar |
| [Notebook epidemiológico](../notebooks/procesamiento_vigilancia_epidemiológica.ipynb) | Descarga, selección de Piura y agregación por provincia | No es un adaptador regional y su relleno de semanas requiere auditoría |
| [Notebook meteorológico](../notebooks/datos_meteorológicos_puntuales.ipynb) | Consulta y agregación meteorológica para puntos de Piura | Representación espacial y calendario deben verificarse |
| [Notebook NASA](../notebooks/datosNASA.ipynb) | Exploración de descarga, integración y calidad para cuatro provincias | Incluye una convención epidemiológica provisional y revisión de casos pendientes |
| [Dataset integrado en revisión](../data/processed/dengueshield_dataset_integrado_REVISION.csv) | 5 376 filas; Piura, Sullana, Morropón y Paita | No es una base regional validada ni el contrato definitivo de la guía |
| [Reporte de calidad](../reports/dengueshield_reporte_calidad.csv) | Resumen por provincia y año | Corresponde al piloto anterior |
| [Casos pendientes](../reports/dengueshield_casos_pendientes_revision.csv) | Filas para revisar la regla de calendario | No eliminarlos ni reinterpretarlos como ausencia de casos |
| [Exploración de regresión](../notebooks/jugando_con_regresion_lineal.ipynb) | Ensayo de regresión con división aleatoria de filas | No demuestra capacidad de anticipación temporal ni un modelo válido para viajeros |
| [Exploración ENSO](../notebooks/procesamiento_indices_enso.ipynb) | Lectura de índices y transformación temporal | Revisar disponibilidad, faltantes y correspondencia de semanas antes de reutilizar |
| [Script ENSO](../scripts/test/obtener_indices_enso.py) | Archivo vacío en la revisión de base | No presentar la descarga ENSO como módulo implementado |

El inventario se basa en lectura de archivos, cabeceras y conteo local. No se volvieron a ejecutar las descargas ni se contrastaron todos los registros con las fuentes originales en esta actualización.

## Revisión técnica necesaria antes de reutilizar

1. El procesamiento epidemiológico llama a `sort_values()` sin asignar su salida y obtiene límites de años desde el orden de los registros. Revisar límites con operaciones explícitas y auditar semanas sin registros frente a ceros observados.
2. Los procesamientos usan distintas convenciones semanales; el meteorológico incluye una numeración desplazada y el notebook NASA declara su convención provisional. Validar calendario, semanas finales y cambios de año con las fuentes, sin suponer 53 semanas en todos los años.
3. El notebook de regresión concatena casos y clima por posición y divide filas al azar. Revisar la unión por claves y rehacer la evaluación temporal antes de interpretar métricas.
4. En ese ensayo, las variables llamadas seno y coseno usan la misma función. Revisar la representación cíclica cuando se reconstruyan las variables.
5. La transformación ENSO incluye rellenos y ponderaciones temporales que necesitan revisar faltantes, periodos parciales y fecha de disponibilidad.
6. Los puntos meteorológicos son aproximaciones espaciales; no acreditan clima homogéneo de toda una unidad territorial.

Estos puntos se documentan sin alterar el trabajo del equipo en esta actualización de producto.

## Qué existe y qué sigue como propuesta

**Existe:** estructura Git, documentación, scripts y notebooks exploratorios, CSV locales del piloto y reportes de calidad previos.

**Está definido como dirección:** guía para viajeros, ámbito sudamericano, consulta por destinos y fechas e interés en dengue, Zika y chikungunya.

**Está pendiente:** selección de países piloto, auditoría regional, contratos implementados, entorno reproducible, modelo temporal evaluado, integración de orientación y aplicación ejecutable.

No se ha demostrado precisión regional, utilidad con viajeros, reducción de contagios ni mejora de las decisiones de viaje.
