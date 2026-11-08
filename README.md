# Guía climática y sanitaria para viajeros

**Primera demo: dengue en Piura, Sullana, Morropón y Paita (Perú).**

Consulta antecedentes de dengue y clima por provincia y periodo. La visión es una guía de viajes para Sudamérica; la cobertura implementada se limita a este piloto. El nombre definitivo del producto está pendiente.

## Ejecutar la demo

Requiere **Python 3.12**. Desde la raíz del repositorio:

```bash
python -m venv .venv
# Linux / macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Abrir la dirección local que imprime Streamlit (normalmente `http://localhost:8501`). La demo utiliza el CSV incluido; no descarga datos ni entrena modelos al abrirse. Las dependencias directas están fijadas en `requirements.txt`.

## Qué funciona

- Selección de provincia y fechas; incluye las semanas completas que se solapan con la consulta.
- Casos confirmados y probables separados, gráficos semanales de casos, temperaturas y lluvia.
- Descarga de la consulta en CSV, cobertura visible y mensajes para periodos sin datos o parcialmente cubiertos.
- Enlaces de consulta a MINSA, OPS y NASA POWER; no se presentan como avisos vigentes integrados.
- Comprobaciones de claves, calendario, conteos, fechas y valores faltantes del snapshot.
- Procesamiento revisado de dengue, malaria, zoonosis y clima: sin descargas al importar, sin generar 53 semanas para todos los años ni rellenar ausencias con ceros. Diagnósticos separados, registros dudosos conservados y manifiestos de procedencia.
- Experimento retrospectivo con persistencia, referencia estacional y regresión Ridge con/sin clima, evaluado por provincia y horizonte.

## Qué todavía falta

- Contrastar calendario, ceros históricos y definición de casos con los recursos originales de MINSA.
- Actualizar datos y reconstruir fechas de publicación antes de emitir pronósticos operativos.
- Itinerarios de varias paradas, integración de avisos vigentes y pruebas con viajeros.
- Validación de utilidad y de predicción operativa. No se ha demostrado reducción de contagios ni riesgo individual.
- Otros países y enfermedades en la interfaz. Malaria y zoonosis permanecen como trabajo exploratorio fuera del piloto.

## Datos y límites

La demo lee `data/processed/dengueshield_dataset_integrado_REVISION.csv`: **5.376 filas**, etiquetas de año 2000–2025, cuatro provincias. Se conserva sin alterar el snapshot histórico del equipo. La fecha de extracción original no está acreditada; la última semana comienza el 28/12/2025 y su ventana llega al 03/01/2026, sin implicar datos actuales.

- Los ceros existentes pueden proceder de rellenos anteriores. Una tabla sin celdas vacías no acredita cobertura completa.
- Calendario **provisional**: domingo a sábado; semana 1 contiene el 4 de enero. Su equivalencia con MINSA está pendiente. El registro de Sullana, semana 53 de 2009, permanece en el reporte de revisión; no se reasigna.
- Piura y Sullana tienen clima idéntico en las 1.357 semanas compartidas. Falta verificar representatividad espacial.
- Los puntos NASA POWER no representan mediciones uniformes de toda la provincia.
- No se calcula probabilidad personal de enfermar, ni se certifican destinos seguros.

[Contrato y procedencia](docs/DATOS.md) · [Alcance](docs/ALCANCE.md) · [Estado y antecedentes](docs/ANTECEDENTES.md)

## Comprobar y evaluar

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/audit_pilot.py
# Elegir una carpeta nueva en cada ejecución:
python -m src.models.evaluate --output reports/mi_evaluacion
```

El experimento entrena en 2001–2021, reporta validación 2022–2023 y prueba 2024. Predice conteos confirmados a 1 y 2 semanas; compara todos los métodos sobre las mismas fechas. Usa el snapshot revisado retrospectivamente, sin reconstruir los retrasos de publicación. **No alimenta pronósticos en la interfaz.**

[Resultados ejecutados y limitaciones](reports/evaluacion_piloto_2026-11-08/README.md) · [Método](docs/EVALUACION.md)

## Procesar archivos del equipo

Desde la raíz, consultar `python -m src.data.cli --help`. Ejemplos:

```bash
python -m src.data.cli dengue --input /ruta/dengue.csv
python -m src.data.cli zoonosis --input /ruta/zoonosis.csv
python -m src.data.cli malaria --input /ruta/malaria_2000_2008.csv /ruta/malaria_2009_2025.csv
python -m src.data.cli clima --input /ruta/clima_diario.csv
# Descarga voluntaria de los recursos configurados; requiere conexión:
python -m src.data.cli dengue --download
```

`--download` también admite malaria, zoonosis y clima (Open-Meteo 2001–2025). Una descarga fallida detiene el proceso. Estas descargas no se ejecutaron para esta entrega; se verificó la transformación con datos locales de prueba. Cada ejecución guarda copias de entrada, SHA-256, consulta y salidas en un directorio nuevo bajo `data/interim/`; nunca sobrescribe los CSV anteriores. Los adaptadores conservan la granularidad de registros y no certifican la calidad epidemiológica de la fuente.

Las rutas antiguas de `Programas/Adquisición de datos/` y `scripts/test/` delegan al nuevo módulo y requieren `--input` o `--download`. Las salidas v2 tienen un esquema distinto; los notebooks antiguos se conservan como antecedentes y no se conectan automáticamente a ellas.

## Organización

| Ruta | Contenido actual |
|---|---|
| `streamlit_app.py` | Aplicación ejecutable |
| `src/data/` | Calendario, validación, consulta y transformación |
| `src/models/evaluate.py` | Evaluación retrospectiva por fechas |
| `tests/` | Pruebas de datos, particiones y flujos de interfaz |
| `reports/evaluacion_piloto_2026-11-08/` | Métricas, predicciones y manifiesto de la ejecución |
| `notebooks/` | Exploraciones anteriores, sin modificación de resultados históricos |
| `Programas/Adquisición de datos/` | Entradas compatibles y CSV exploratorios previos |
| `docs/` | Alcance, fuentes, método y próximos pasos |

Ingeniería Informática: datos, modelos e interfaz. Ingeniería Industrial: proceso de planificación y evaluación de utilidad. Asignación individual pendiente. [Equipo](docs/EQUIPO.md) · [Contribuir](CONTRIBUTING.md) · [Demo](docs/DEMO.md) · [Roadmap](docs/ROADMAP.md)
