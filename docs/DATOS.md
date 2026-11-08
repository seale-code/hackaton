# Datos, procedencia y contratos

## Snapshot que consume la demo

Archivo: `data/processed/dengueshield_dataset_integrado_REVISION.csv`.
SHA-256: `6bf93f88c3e29593c59f27f7bdc9bc9319422dfd3c097498e4785be4366f2733`.

Clave única: `provincia + ano + semana`; `inicio_semana` debe concordar con el calendario provisional. Provincias: PIURA, SULLANA, MORROPON, PAITA. Conteos confirmados y probables enteros no negativos. Temperaturas en °C y lluvia semanal en mm según la integración NASA previa. `anio_sin_casos_registrados` conserva la advertencia del procesamiento anterior.

El cargador rechaza duplicados, fechas discordantes, nulos, infinitos, conteos negativos/no enteros, temperaturas invertidas y provincias fuera del piloto. No rellena datos. Es una validación estructural, no certificación de cobertura.

## Fuentes utilizadas en la exploración

- MINSA / CDC Perú: [catálogo de dengue](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue). URL configurada en el script: `https://www.datosabiertos.gob.pe/node/23482/download`. Falta acreditar el hash y la fecha de descarga de la fuente que originó el snapshot integrado.
- NASA POWER: `https://power.larc.nasa.gov/api/temporal/daily/point`; parámetros T2M_MAX, T2M_MIN y PRECTOTCORR, comunidad AG. Integración conservada en `notebooks/datosNASA.ipynb`. Puntos: Piura (-5.1945,-80.6328), Sullana (-4.9039,-80.6853), Morropón (-5.1822,-79.9690), Paita (-5.0852,-81.1137).
- Open-Meteo histórico: `https://archive-api.open-meteo.com/v1/archive`. Corresponde a otra exploración y a la entrada de clima v2; no sustituye NASA dentro del snapshot de la demo.
- NOAA ENSO: exploración anterior conservada; no entra en este experimento ni en la interfaz.

Los enlaces OPS de la interfaz son referencias de consulta, no datos descargados por la aplicación.

## Calendario y ausencias

Convención técnica provisional: semanas domingo–sábado, semana 1 contiene el 4 de enero. Tiene 52 o 53 semanas según el año. No se afirma equivalencia completa con el calendario epidemiológico de MINSA. Las filas incompatibles se guardan en archivos `*_revision.csv` junto a su motivo; no se renumeran automáticamente.

El snapshot original conserva rellenos previos: 2.835 filas con cero confirmados y 573 filas marcadas con año sin casos. Son conteos del archivo, no cifras oficiales de ausencia de dengue. Los 1.357 registros climáticos semanales compartidos entre Piura y Sullana son idénticos; representatividad por revisar. Se conserva el registro pendiente de Sullana 2009/53 en `reports/dengueshield_casos_pendientes_revision.csv`.

## Salidas de los adaptadores v2

- Dengue/zoonosis: `departamento, provincia, ano, semana, inicio_semana, diagnostic, tipo_dx, registros`. Una fila cuenta notificaciones presentes de un tipo; las semanas y diagnósticos sin registros no se inventan con cero. Diagnósticos fuera de selección y campos inválidos van al reporte de revisión. Dengue selecciona Piura.
- Malaria 2000–2008: columnas falciparum/vivax separadas, sumadas por provincia y semana; conteos inválidos van a revisión.
- Malaria 2009–2025: número de notificaciones por tipo de diagnóstico; si la fuente no tiene tipo se marca `NO_INFORMADO`. Los dos periodos se exportan separados porque su equivalencia requiere revisar diccionarios y definiciones.
- Clima: media semanal de temperatura/humedad y suma de lluvia solo con siete días y tres variables completas. Una semana parcial conserva metadatos de cobertura y valores vacíos. Días duplicados o valores físicamente inválidos disparan un error.

La selección exacta de códigos de zoonosis se conserva del aporte del equipo (A27, X20, X21); no se presenta ese conjunto como una sola enfermedad. Las fuentes completas permanecen en cada ejecución para poder revisar la selección.

## Trazabilidad y compatibilidad

`python -m src.data.cli ...` crea un directorio nuevo con entradas originales, resultados, revisión y `manifest.json` (origen, consulta, SHA-256, lectura UTC, filas). No sobrescribe CSV históricos. Los notebooks antiguos esperan otro esquema; deben migrarse explícitamente antes de consumir las salidas v2. Los manifiestos de nuevas descargas no reparan retroactivamente la procedencia incompleta del snapshot de la demo.
