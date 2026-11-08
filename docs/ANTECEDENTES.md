# Estado comprobable y antecedentes

## Estado actual

El piloto ejecutable es dengue en cuatro provincias de Piura. La visión regional permanece como ampliación. Consulte [README](../README.md) y [alcance](ALCANCE.md) para los comandos y la cobertura actuales.

| Material | Estado |
|---|---|
| Interfaz `streamlit_app.py` | Consulta histórica, clima, exportación, fuentes y cobertura |
| `src/data/` | Validación estructural, calendario provisional y adaptadores revisados |
| `src/models/evaluate.py` | Experimento retrospectivo de 1–2 semanas, con referencias y cortes por fecha |
| `tests/` | Pruebas automatizadas de datos, límites temporales y aplicación |
| CSV integrado | Original conservado, 5.376 filas; calidad epidemiológica pendiente |
| CSV malaria y zoonosis | Aporte del equipo conservado; las nuevas salidas v2 no los sobrescriben |
| Notebooks anteriores | Evidencia exploratoria conservada; sus métricas no se actualizan retroactivamente |

## Problemas del trabajo anterior y tratamiento actual

- Los antiguos scripts generaban 53 semanas para cada año y ceros para ausencias. Los nuevos adaptadores usan un calendario compartido provisional, mantienen solo registros presentes y separan incompatibles para revisión.
- El cálculo meteorológico anterior desplazaba semanas (`w - 1`) y dividía por siete incluso periodos incompletos. El nuevo agregador usa semanas desde 1, comprueba siete días y deja vacías las agregaciones parciales.
- Zoonosis agrupaba sin `tipo_dx`; el nuevo conteo conserva esa columna.
- Malaria sumaba conteos de un periodo y filas de otro bajo un mismo total. Ahora los periodos y sus definiciones se exportan separados.
- Los módulos descargaban al importarse. Ahora requieren ejecución explícita con `--input` o `--download`.
- El notebook de regresión une por posición, divide filas al azar y duplica el seno bajo el nombre coseno. Se conserva como antecedente; el nuevo experimento crea series por fecha, usa seno/coseno distintos y reserva años posteriores.

## Límites todavía abiertos

Calendario oficial, ceros del snapshot, trazabilidad de la descarga original, datos disponibles al corte y representatividad espacial. Las correcciones de código no certifican ni modifican los CSV antiguos. No se volvieron a descargar fuentes sanitarias para esta entrega.

La evaluación nueva es retrospectiva sobre datos en revisión; no equivale a un modelo operativo validado. No se han probado itinerarios con viajeros ni demostrado mejoras de decisiones o reducción de infecciones.
