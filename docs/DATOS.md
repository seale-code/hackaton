# Contratos y calidad de datos

Los contratos siguientes son propuestas para la guía regional. Las plantillas tienen solo encabezados; no representan una integración ya realizada. Los CSV de Piura conservan su formato anterior y no cumplen automáticamente estos contratos.

## 1. Catálogo de fuentes

Archivo de referencia: [catalogo_fuentes.csv](../data/sample/catalogo_fuentes.csv).

| Campo | Significado |
| --- | --- |
| `source_id` | Identificador estable usado en las demás tablas |
| `label` | Nombre del organismo/producto |
| `url` | Página o documentación exacta del recurso |
| `kind` | Epidemiología, clima, índice climático u orientación |
| `access_status` | Fuente identificada, descarga por validar o exploración local previa; no asumir integración regional |
| `license_status` | Condiciones de uso verificadas o pendientes |

Cada descarga real debe ampliar el catálogo con URL del archivo o consulta y parámetros, fecha de consulta, versión/snapshot, periodo, unidades, nivel geográfico, definiciones y condiciones de redistribución. Un enlace al portal no sustituye esa ficha del recurso.

## 2. Observaciones epidemiológicas

Plantilla: [observaciones_epidemiologicas_plantilla.csv](../data/sample/observaciones_epidemiologicas_plantilla.csv).

| Campo | Convención propuesta |
| --- | --- |
| `country_iso3` | País en ISO 3166-1 alfa-3 |
| `area_id` | Identificador territorial estable; no un nombre libre como clave |
| `spatial_level` | `country` o nivel subnacional documentado |
| `disease` | Identificador normalizado de dengue, Zika o chikungunya |
| `case_definition` | Confirmado, probable, sospechoso u otra definición de la fuente; no mezclarlos sin justificación |
| `week_start` | Fecha ISO `YYYY-MM-DD`; conversión desde el calendario de la fuente documentada |
| `cases` | Conteo observado; vacío si falta, nunca rellenado automáticamente con cero |
| `notification_status` | `reported`, `missing`, `partial` o `revised` |
| `population` | Denominador compatible si se dispone de él; vacío si no |
| `population_reference` | Fuente/año y ámbito del denominador |
| `source_id` | Referencia al catálogo |
| `available_at` | Fecha de publicación/disponibilidad comprobada; vacío si se desconoce |
| `retrieved_at` | Fecha-hora ISO de consulta del snapshot |
| `dataset_version` | Identificador del snapshot usado |

Clave dentro de un snapshot seleccionado: país, área, enfermedad, definición, semana y fuente. Resolver revisiones de la misma clave de forma explícita. La tabla de entrenamiento final selecciona una serie compatible y evita sumar el registro nacional de OPS con el mismo dato de la autoridad nacional.

Casos acumulados requieren una transformación revisada antes de tratarlos como incidentes semanales. Diferencias negativas pueden reflejar correcciones y no deben convertirse silenciosamente en cero.

## 3. Clima e índices de El Niño

Para cada variable registrar: fuente, punto/celda/estación o agregado de área, fecha o periodo, unidad, valor, cobertura válida, fecha de disponibilidad y versión.

- Agregar temperatura y precipitación con reglas y unidades explícitas.
- Conservar cantidades válidas: una suma de días faltantes no equivale a precipitación cero.
- Un punto o celda meteorológica no representa automáticamente toda una provincia o país. Justificar la asignación o agregación espacial.
- Respetar el calendario y zona horaria de cada fuente al construir semanas.
- Índices mensuales o estacionales no son observaciones semanales nuevas. Documentar su alineación y el momento de publicación.
- Diferenciar Niño 1+2, Niño 3.4, ONI y otros índices; no tratarlos como series intercambiables.
- Usar solo variables conocidas al corte. Una serie retrospectiva revisada puede requerir declarar limitaciones sobre su disponibilidad histórica.

## 4. Estimaciones

Plantilla: [pronosticos_plantilla.csv](../data/sample/pronosticos_plantilla.csv).

| Campo | Significado |
| --- | --- |
| `country_iso3`, `area_id`, `spatial_level`, `disease` | Cobertura exacta del modelo |
| `case_definition` | Definición de la variable objetivo |
| `cutoff_date` | Momento hasta el que puede usarse información |
| `target_week_start` | Semana concreta para la que se emite la estimación |
| `horizon_weeks` | Desplazamiento definido respecto al último periodo observado utilizable |
| `target_name` | Conteo o evento de incremento elegido, con definición en la ficha del modelo |
| `prediction_value` | Estimación del objetivo, no probabilidad personal de enfermedad |
| `prediction_lower`, `prediction_upper` | Opcionales; solo con intervalos evaluados |
| `model_version`, `dataset_version`, `evaluation_id` | Identificadores reproducibles |
| `generated_at` | Fecha-hora de generación |
| `status` | `experimental_validated` si fue evaluado o `unavailable`; la evaluación no implica eficacia clínica |
| `unavailable_reason` | Motivo cuando no se puede emitir; vacío si sí aplica |

Un resultado no disponible tiene estimación e intervalos vacíos. No se devuelve cero. El objetivo, las unidades y el evento de clasificación se guardan en la ficha correspondiente al modelo.

## 5. Itinerario

Plantilla: [itinerario_plantilla.csv](../data/sample/itinerario_plantilla.csv).

`trip_id`, `stop_id`, `destination_label`, `country_iso3`, `area_id`, `requested_spatial_level`, `arrival_date`, `departure_date`.

El destino solicitado y la escala de los datos pueden ser distintos; la interfaz debe explicarlo. El identificador de viaje puede ser temporal para el MVP. No se necesitan pasaporte, diagnóstico, embarazo u otros datos clínicos para implementar la consulta propuesta.

Validar fechas ISO, llegada anterior a salida, claves de paradas y destinos admitidos. Un itinerario de ejemplo no contiene afirmaciones sanitarias.

## 6. Orientación y avisos oficiales

Registrar organismo, URL, enfermedad, territorio, fecha de publicación/revisión cuando exista, fecha de consulta, texto revisado o enlace, y criterio de vigencia. Mantener el nivel y la redacción atribuida de cada autoridad. No asignar a una estimación del modelo el formato de una alerta oficial.

La ausencia de un aviso encontrado no demuestra ausencia de riesgo. La orientación individual sobre vacunas, medicación o condiciones personales se remite a la fuente competente y a consulta profesional.

## 7. Controles de integración

1. Unicidad de claves y preservación de identificadores territoriales como texto.
2. Semanas válidas según cada fuente; revisar cambios de año y calendarios diferentes.
3. Ceros, faltantes, datos parciales y revisiones diferenciados.
4. Cobertura común entre fuentes y series seleccionadas sin doble conteo.
5. Disponibilidad al corte y separación de variables futuras.
6. Coherencia de unidades, población y escala; no comparar totales brutos como riesgo personal.
7. Estados del producto documentados en [PRODUCTO.md](PRODUCTO.md).

## Almacenamiento

`data/raw/` conserva originales locales, `interim/` las transformaciones y `processed/` las tablas listas para el pipeline. `sample/` puede versionar contratos y muestras pequeñas cuya redistribución esté permitida. No publicar datos personales ni datos de terceros sin verificar condiciones de uso.
