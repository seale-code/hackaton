> **Estado del piloto (08/11/2026):** el alcance implementado está en [ALCANCE.md](ALCANCE.md). Las propuestas regionales de este documento son ampliaciones futuras, no cobertura disponible. La implementación y las fuentes consumidas se detallan en [README](../README.md) y [DATOS.md](DATOS.md).

# Fuentes y referencias del producto

## Catálogo inicial

Se identificaron las páginas siguientes. Esta revisión no acredita una descarga regional completa, cobertura subnacional uniforme, permisos de reutilización universales ni una integración funcionando.

| Fuente | Uso posible | Qué se comprobó | Qué falta verificar |
| --- | --- | --- | --- |
| [OPS: ARBO Portal](https://www.paho.org/es/arbo-portal) | Dengue, Zika y chikungunya en las Américas | El portal reúne información proporcionada por autoridades sanitarias; los datos pueden revisarse | Recursos descargables, histórico por país/enfermedad, granularidad, calendario y condiciones de uso |
| [OPS: datos abiertos](https://opendata.paho.org/es) | Localizar recursos y análisis por enfermedad | El portal ofrece entradas para estas enfermedades | Acceso automatizable, formato, cobertura y licencias de cada recurso |
| [OPS: boletín anual 2024](https://ais.paho.org/ha_viz/Arbo/Arbo_Bulletin_2024.asp?env=pri) | Referencia de definiciones y límites de notificación | Presenta datos regionales y advierte sobre revisiones y notificación incompleta | Utilidad del recurso específico para construir series; no usar el boletín como sustituto de una tabla auditada |
| Ministerios e institutos nacionales de salud | Ampliar resolución y contrastar series | No se seleccionó un catálogo regional definitivo | Países, URLs exactas, definiciones, oportunidad y condiciones de descarga |
| [NASA POWER: API diaria](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) | Series meteorológicas históricas | Documentación de series y formatos; hay exploración local previa | Variables, unidades, representación territorial, faltantes y latencia para el piloto |
| [NASA POWER: metodología](https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/) | Entender las fuentes y revisiones meteorológicas | Describe datos meteorológicos procesados y fuentes de reanálisis | Evaluar resolución y asignación espacial; no tratarlos como estaciones locales |
| [NOAA PSL: índices mensuales](https://psl.noaa.gov/data/timeseries/month/) | Indicadores relacionados con El Niño | Catálogo de índices y documentación; existe un notebook previo | Serie exacta, versión, disponibilidad, frecuencia y pertinencia por territorio |
| [CDC: Travel Health Notices](https://wwwnc.cdc.gov/travel/notices) | Avisos oficiales y enlaces preventivos | Clasificación y descripción de avisos para viajeros | Extracción, condiciones de uso, vigencia y revisión de contenido integrado |
| [CDC Yellow Book: Perú](https://www.cdc.gov/yellow-book/hcp/americas-caribbean/peru.html) | Ejemplo de guía sanitaria de un destino | Referencia existente para viajeros | No generalizar sus recomendaciones a otros países ni convertirla en una predicción propia |

El catálogo CSV inicial está en [data/sample/catalogo_fuentes.csv](../data/sample/catalogo_fuentes.csv). Sus estados describen identificación o exploración, no validación regional.

## Antecedentes y diferenciación por comprobar

| Referencia | Qué describe su información pública | Relación con esta propuesta |
| --- | --- | --- |
| OPS ARBO Portal | Datos y análisis de arbovirus | Fuente y referencia de visualización epidemiológica |
| CDC Travelers’ Health | Orientación por destino y avisos para viajeros | Referencia que ya cubre preparación sanitaria |
| [Sitata](https://www.sitata.com/en/travel-insurance-for-your-trip/) | Alertas sobre brotes y otros eventos de viaje | Servicio existente; revisar su cobertura funcional antes de afirmar originalidad |
| [Sivapre, descripción de Cayetano](https://investigacion.cayetano.edu.pe/noticias/estudiante-de-enfermeria-de-cayetano-integra-equipo-que-desarrolla-sistema-inteligente-para-prevenir-brotes-de-dengue-en-el-peru/) | Vigilancia de dengue, reportes ciudadanos y orientación de intervenciones | Antecedente de la discusión; nuestra dirección actual tiene al viajero y su itinerario como usuario y entrada principales |

Posible aporte a contrastar: reunir itinerario, fechas, tendencias evaluadas y orientación oficial con cobertura e incertidumbre visibles. No se afirma una innovación mundial ni una funcionalidad ausente en todos los productos existentes. Esta tabla se basa en descripciones públicas y no acredita el comportamiento técnico de esos servicios.

## Información que debe acompañar cada fuente real

- Organismo y recurso exacto, URL y parámetros de consulta.
- Fecha de consulta y versión de archivo o snapshot.
- Países, territorios, enfermedad, periodo y calendario.
- Definición de casos, unidad y estado de notificación.
- Frecuencia de publicación, retrasos y política de revisiones.
- Condiciones de uso y redistribución.
- Procedimiento para reproducir la obtención y transformación.

## Selección de países y enfermedad

Elegir por intersección útil de cobertura y calidad, no solo por el total de filas. Revisar historia suficiente para probar después del entrenamiento, eventos observables, definiciones compatibles y escala útil para el producto. Los países y la enfermedad del primer modelo siguen pendientes.

## Vigencia de orientación

Los avisos pueden cambiar. La guía deberá mostrar fuente y fecha de consulta, diferenciar un corte histórico de la situación actual y evitar recomendaciones clínicas inventadas. No reutilizar cifras de conversaciones anteriores como datos vigentes.

## Malaria en Perú

CDC Perú / Ministerio de Salud. *Vigilancia epidemiológica de Malaria*. Plataforma Nacional de Datos Abiertos. [Catálogo oficial](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-malaria). Recursos identificados: `datos_abiertos_vigilancia_malaria_2000_2008.csv` y `datos_abiertos_vigilancia_malaria_2009_2025.csv`. Catálogo consultado el 8 de noviembre de 2026.

La aplicación consulta los CSV derivados del equipo; la solicitud directa del recurso oficial quedó bloqueada. [Procedencia, definiciones y contrato](MALARIA.md).
