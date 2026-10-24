# Fuentes y contrato de datos

## Fuentes candidatas mencionadas en la planificación

| Fuente | Información buscada | Estado |
| --- | --- | --- |
| MINSA / CDC Perú | Casos de dengue, ubicación y semana epidemiológica | Acceso y cobertura por verificar |
| SENAMHI | Temperatura, precipitación y humedad | Series, permisos y faltantes por verificar |
| ENFEN / SENAMHI | Indicadores históricos relacionados con El Niño | Serie utilizable y frecuencia por verificar |
| INEI | Población y variables territoriales | Año y comparabilidad por verificar |

No se han descargado ni verificado datasets en este repositorio. Registrar para cada fuente: URL exacta, fecha de consulta, licencia o condiciones de uso, periodo, granularidad, unidades y procedimiento de obtención. No copiar cifras o supuestas coberturas de los chats como hechos verificados.

## Tabla analítica propuesta

Una fila por zona y semana, con clave territorial estable. Campos mínimos propuestos:

- `zona_id`: código territorial como texto, conservando ceros iniciales.
- `semana_inicio`: fecha; documentar la convención epidemiológica y los cambios de año.
- `casos`: conteo observado, distinguiendo cero de dato faltante.
- `temperatura`, `precipitacion`, `humedad`: unidades y agregaciones explícitas.
- `indicador_nino`: identificar la serie concreta, frecuencia y fecha de disponibilidad.
- `poblacion`: estimación y año de referencia, si se usa incidencia o priorización.

No todas las variables están garantizadas. Seleccionar solo las que puedan sostenerse con datos comparables.

## Reglas de integración

1. Validar unicidad de zona/semana y consistencia de códigos territoriales.
2. Documentar asignación de estaciones a zonas y agregación de clima.
3. Revisar faltantes, duplicados, revisiones de casos y cambios territoriales.
4. Conservar fecha de publicación cuando exista; una variable solo puede usarse si era conocida al emitir la predicción.
5. No repartir un total departamental entre distritos ni interpolar datos como si fueran observaciones reales.
6. Si los datos de Piura solo permiten una serie departamental, reducir el alcance y retirar el ranking interdistrital.

## Almacenamiento

`data/raw/` conserva originales locales; `interim/` las transformaciones; `processed/` tablas analíticas. Esas carpetas excluyen datos de Git por defecto. `sample/` puede contener ejemplos pequeños, explícitamente sintéticos o con permiso de redistribución.
