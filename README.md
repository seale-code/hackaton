<div align="center">

# Guía climática y sanitaria para viajeros en Sudamérica

### Datos epidemiológicos y clima para conocer mejor tu destino

**Información territorial · Visualización de datos · Análisis temporal**

Proyecto de la Hackatón FACI  
Ingeniería Informática + Ingeniería Industrial

</div>

---

## El proyecto

Preparar un viaje también implica conocer el contexto sanitario y ambiental del destino. Este proyecto reúne información epidemiológica y climática en una experiencia de consulta por lugar y periodo, con gráficos y fuentes que facilitan explorar los datos.

La propuesta tiene una visión sudamericana y reúne dos experiencias de consulta con datos de Perú: **dengue y clima en Piura, Sullana, Morropón y Paita**, y **malaria por departamento y provincia**, a partir de 22 archivos departamentales.

> **Nuestra pregunta:** ¿cómo acercar la información sanitaria y climática de un destino a las personas que preparan un viaje?

## Nuestra propuesta

Conectar datos, territorio y tiempo para hacer más accesible la consulta de antecedentes. La aplicación permite explorar cómo varían los casos registrados y las condiciones climáticas a lo largo de las semanas, manteniendo visible la procedencia de la información.

El proyecto combina dos perspectivas: el desarrollo de herramientas de análisis y visualización, y el estudio de cómo esas herramientas pueden apoyar la planificación de un recorrido.

## Explora la aplicación

| Funcionalidad | Experiencia de consulta |
| --- | --- |
| Selección de consulta | Elige dengue o malaria y explora los territorios disponibles |
| Consulta temporal | Selecciona fechas para dengue o periodo de origen y año para malaria |
| Evolución semanal | Visualiza confirmados y probables de dengue, o registros históricos de malaria |
| Contexto climático de Piura | Consulta temperaturas y precipitación histórica junto al dengue |
| Datos descargables | Exporta la selección en formato CSV |
| Fuentes y cobertura | Identifica la procedencia y el periodo de los datos |

**El recorrido es sencillo:** elige la información sanitaria, selecciona el destino y periodo, y explora sus registros semanales.

## La experiencia con datos de Perú

La consulta de dengue reúne **5.376 registros semanales** y variables meteorológicas de cuatro provincias de Piura. La consulta de malaria explora **181.578 filas históricas en 22 archivos departamentales**, organizadas por provincia, año y semana.

Las series abarcan etiquetas de año entre **2000 y 2025**. Para malaria, la aplicación presenta por separado los periodos de origen **2000–2008** y **2009–2025**, conservando sus respectivas definiciones de conteo.

| Componente | Fuente de referencia |
| --- | --- |
| Vigilancia epidemiológica de dengue y malaria | CDC Perú / Ministerio de Salud |
| Variables meteorológicas del piloto | NASA POWER |
| Información de consulta sobre dengue | Organización Panamericana de la Salud |

El análisis de dengue se complementa con un **experimento retrospectivo de predicción de conteos semanales a una y dos semanas**, que compara referencias estadísticas y regresión con y sin variables climáticas. Su metodología y resultados se presentan en la documentación técnica.

## Tecnología

**Python · pandas · NumPy · scikit-learn · Streamlit · Plotly**

Python sostiene el procesamiento y análisis; Streamlit y Plotly permiten explorar los resultados mediante una interfaz interactiva. Las pruebas automatizadas se ejecutan con pytest y GitHub Actions.

## Ejecutar la aplicación

Requiere **Python 3.12**. Desde la carpeta del repositorio:

```bash
python -m venv .venv
```

Activa el entorno según tu sistema:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala las dependencias e inicia la aplicación:

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Abre la dirección que muestra Streamlit, normalmente `http://localhost:8501`. La consulta utiliza el conjunto de datos incluido en el repositorio.

## Un proyecto interdisciplinario

**Ingeniería Informática** aporta el procesamiento de datos, el análisis temporal y el desarrollo de la aplicación. **Ingeniería Industrial** aporta la perspectiva de planificación del viaje, organización de la información y evaluación de utilidad.

El trabajo vincula el análisis del clima con el acceso a información sanitaria para la preparación de viajes.

## Conoce más

- [Alcance del proyecto](docs/ALCANCE.md)
- [Datos, fuentes y criterios de calidad](docs/DATOS.md)
- [Consulta y procesamiento de malaria](docs/MALARIA.md)
- [Metodología de evaluación de dengue](docs/EVALUACION.md)
- [Resultados del experimento](reports/evaluacion_piloto_2026-11-08/README.md)
- [Recorrido de la demo](docs/DEMO.md)
- [Equipo](docs/EQUIPO.md)
- [Guía para contribuir](CONTRIBUTING.md)
