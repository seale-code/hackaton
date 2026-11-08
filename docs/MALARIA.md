# Malaria: consulta y procesamiento

## Aplicación

Ejecutar `python -m streamlit run streamlit_app.py` y elegir **Malaria** en el selector lateral. Seleccionar departamento, periodo de origen, provincia y año. La pantalla muestra total del archivo, semanas registradas, semanas con valores positivos, gráfico semanal y CSV descargable con procedencia y banderas de calidad.

Hay 22 archivos departamentales: corresponden a los territorios presentes en el repositorio, no a una garantía de cobertura completa de Perú o Sudamérica. La ausencia de un departamento, provincia o año no significa ausencia de malaria. La información es histórica y no estima el riesgo individual de un viaje.

## Archivos utilizados

Se leen directamente los CSV de `Programas/Adquisición de datos/vigilancia_malaria/`. Contienen `ano, semana, provincia, malaria_total`. Se preservan sin cambios; la pantalla los carga por departamento y añade metadatos en memoria.

Son 181.578 filas derivadas del procesamiento anterior. La extracción original no tiene manifiesto recuperable: sus SHA-256 actuales se registran en [la auditoría](../reports/malaria/auditoria_archivos.json), lo cual identifica estos archivos, no certifica su concordancia con una versión oficial.

Se comprobó la existencia del catálogo oficial de [Vigilancia epidemiológica de Malaria, CDC Perú / MINSA](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-malaria), con recursos para 2000–2008 y 2009–2025. En esta sesión, la solicitud directa del CSV oficial devolvió HTTP 418 con una página de bloqueo; no se reintentó mediante rutas alternativas. La implementación usa los CSV del equipo, sin afirmar que se volvieron a descargar o validar contra el recurso original.

## Definiciones separadas

- **2000–2008:** el script original sumó las columnas falciparum y vivax.
- **2009–2025:** el script original contó filas de notificaciones individuales.

No se fusionan ambos periodos en una tendencia ni en un único total de la interfaz. Los archivos derivados solo conservan `malaria_total`: no permiten recuperar especies ni clasificar sus filas como confirmadas, probables o sospechosas. El CSV de la consulta conserva `periodo_fuente` y `definicion_conteo`.

El adaptador de fuentes originales (`aggregate_malaria`) sí conserva falciparum/vivax separados para el primer periodo y `diagnostic` más `tipo_dx` para notificaciones individuales. Si una columna de diagnóstico está ausente, vacía o nula, queda como `NO_INFORMADO`; no se deduce un diagnóstico.

## Calendario, ceros y nombres

La consulta utiliza **año y número de semana originales**, no fechas diarias reconstruidas. El procesamiento previo creó hasta 53 semanas todos los años. Frente a la convención provisional del piloto, 2.744 filas requieren revisión; 18 contienen valores positivos que suman 167. Se conservan en los totales, el gráfico, la tabla y la descarga, con `calendario_revision=True`. Esta bandera no demuestra que la etiqueta de MINSA sea incorrecta.

Los ceros heredados se etiquetan como `cero_heredado_no_verificado`; no se reinterpretan como ausencia comprobada de enfermedad. La consulta no genera nuevas filas ni ceros y un año sin filas devuelve un estado sin datos.

Cuatro nombres contienen un carácter de sustitución en los CSV: CA�ETE, DATEM DEL MARA�ON, FERRE�AFE y MARA�ON. La interfaz presenta los alias de lectura Cañete, Datem del Marañón, Ferreñafe y Marañón. Los identificadores, filtros internos y exportaciones preservan el valor original; no se reparan los CSV silenciosamente.

## Reproducir la auditoría y procesar fuentes

```bash
python scripts/audit_malaria.py
python -m pytest -q
# Para guardar una nueva auditoría, elegir un archivo que no exista:
python scripts/audit_malaria.py --output reports/malaria/nueva_auditoria.json
# Fuentes originales: primero archivo agregado y luego individual:
python -m src.data.cli malaria --input /ruta/malaria_2000_2008.csv /ruta/malaria_2009_2025.csv
```

El CLI crea nuevas salidas y manifiestos en `data/interim/`. Su esquema v2 no reemplaza automáticamente los CSV derivados que consume esta pantalla. No se entrena un modelo de malaria sobre los ceros heredados ni se aplica el modelo de dengue a esta enfermedad.

## Verificación

Se prueban los 22 archivos, integridad de los hashes, claves únicas, valores finitos/no negativos, separación de periodos, conservación de semanas en revisión, ausencia de datos y cambios de filtros en Streamlit. El flujo de dengue mantiene sus pruebas anteriores. La revisión visual en navegador y la verificación de las fuentes originales son comprobaciones independientes de estas pruebas automatizadas.
