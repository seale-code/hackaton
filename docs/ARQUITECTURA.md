# Arquitectura propuesta

## Flujo de datos y consulta

Fuentes epidemiológicas y climáticas se ingieren como snapshots versionados. Tras normalizar territorios, fechas y definiciones se producen series y variables. El entrenamiento y la evaluación se ejecutan fuera de la interfaz. La consulta relaciona esas salidas con las fechas del itinerario y con orientación oficial revisada.

El diagrama general está en el [README](../README.md#cómo-funcionaría).

## Componentes previstos

| Ruta | Responsabilidad | Estado |
| --- | --- | --- |
| `src/data/` | Adaptadores de fuentes, catálogo, normalización territorial y auditorías | Documentación; adaptadores regionales pendientes |
| `src/features/` | Rezagos, ventanas, estacionalidad y variables climáticas disponibles al corte | Documentación; implementación pendiente |
| `src/models/` | Baselines, entrenamiento, evaluación temporal e inferencia | Documentación; sin modelo regional validado |
| `src/itineraries/` | Validación de paradas y cruce de fechas con cobertura | Documentación; implementación pendiente |
| `src/guidance/` | Catálogo revisado de avisos y orientación oficial | Documentación; implementación pendiente |
| `src/prioritization/` | Comparación opcional de alternativas con criterios explícitos | Documentación; implementación pendiente |
| `app/` | Interfaz de recorrido y consulta de resultados versionados | Documentación; sin aplicación ejecutable |

Los notebooks y scripts de Piura son antecedentes de exploración. No constituyen estos módulos implementados.

## Tecnología sugerida

Un proyecto Python con pandas, scikit-learn, Streamlit y Plotly. Usar archivos versionados para la primera integración y decidir posteriormente si hace falta una base de datos. No crear una API independiente o servicios adicionales sin una necesidad concreta.

Todavía no se fijaron versiones de dependencias. El README no incluye un comando de arranque que no exista.

## Separación de ejecución

- **Ingesta:** descargar con condiciones de uso respetadas y registrar fuente, consulta y disponibilidad.
- **Entrenamiento:** usar snapshots, particiones y parámetros guardados; generar métricas y una ficha del modelo.
- **Consulta:** leer datos y resultados ya preparados; no entrenar ni descargar todo por cada interacción del usuario.
- **Orientación:** mantener el enlace y el contenido de la autoridad separados del resultado del modelo.

## Integración de una parada

1. Resolver destino y escala geográfica sin inventar detalle subnacional.
2. Buscar datos observados compatibles con la enfermedad y la fecha de corte.
3. Verificar antigüedad y completitud.
4. Comprobar si el horizonte del modelo cubre las semanas del viaje.
5. Construir la ficha con históricos, estimaciones aplicables y avisos, conservando su procedencia.

Las estancias que atraviesen varias semanas mostrarán cada periodo disponible. No se suman riesgos semanales para obtener una probabilidad individual de contagio.

## Contratos y trazabilidad

Ver [DATOS.md](DATOS.md). Cada resultado debe poder relacionarse con territorio, enfermedad, fuente, fecha de corte, versión del dataset y, si aplica, modelo y evaluación. Los archivos con sufijo `REVISION` del piloto anterior no se cargan por defecto como fuente regional.
