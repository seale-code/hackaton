# Cómo colaborar

El producto actual es la guía climática y sanitaria para viajeros en Sudamérica. Leer [alcance](docs/ALCANCE.md), [contratos de datos](docs/DATOS.md) y [estado comprobable](docs/ANTECEDENTES.md) antes de iniciar una tarea.

## Flujo de trabajo

1. Elegir una tarea pequeña con resultado y criterios de aceptación.
2. Crear una rama: `feat/descripcion`, `fix/descripcion` o `docs/descripcion`.
3. Implementar el cambio y actualizar los documentos relacionados.
4. Ejecutar las comprobaciones pertinentes al comportamiento modificado. No inventar un comando de pruebas que no exista.
5. Abrir un pull request con problema, resultado, evidencia y límites.
6. Revisar antes de integrar a `main` y conservar el historial del equipo.

## Datos y resultados

- Documentar recurso exacto, consulta, versión, periodo, escala y condiciones de uso.
- Distinguir observaciones, ejemplos sintéticos, avisos oficiales y resultados del modelo.
- No rellenar faltantes con cero sin justificación.
- No publicar secretos, itinerarios personales o datos clínicos de terceros.
- No cambiar notebooks y datasets de Piura como si fueran datos regionales: revisar primero los antecedentes y conservar procedencia.
- Evaluar modelos temporalmente, con baseline y variables disponibles en la fecha de corte.

## Criterio de terminado

Se cumplen los criterios de aceptación, hay evidencia relevante, la documentación refleja la implementación real y se conocen sus límites. Una carpeta con README no cuenta como módulo ejecutable; una fuente enlazada no cuenta como integración descargada.

## Convenciones

Nombres descriptivos, identificadores estables y commits pequeños. Una función para comparar alternativas se llama comparación; hablar de optimización solo cuando existan objetivo y restricciones explícitos. No añadir herramientas sin necesidad concreta.
