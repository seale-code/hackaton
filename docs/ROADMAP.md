# Roadmap: guía del viajero

Las casillas representan entregables por completar, no funciones ya implementadas.

## 1. Verificar viabilidad de datos

- [ ] Inventariar por país y enfermedad cobertura, descarga, periodo y condiciones de uso.
- [ ] Seleccionar dos o tres países piloto solo si hay información comparable.
- [ ] Elegir una enfermedad, unidad territorial, objetivo y horizonte del primer modelo.
- [ ] Revisar correspondencia de semanas, definiciones de caso y fechas de publicación.
- [ ] Documentar qué orientación oficial se puede integrar y cómo revisar su vigencia.

**Salida:** ficha de viabilidad y decisiones registradas. Sin datos suficientes, reducir cobertura y mantener consulta descriptiva sin prometer un modelo.

## 2. Construir la base reproducible

- [ ] Implementar descargas y conservar snapshots con catálogo.
- [ ] Normalizar territorios, enfermedades y periodos con contratos de datos.
- [ ] Auditar duplicados, faltantes, revisiones y cambios de definición.
- [ ] Revisar problemas del piloto de Piura antes de reutilizar transformaciones.
- [ ] Preparar una muestra para desarrollar la interfaz sin inventar resultados reales.

**Salida:** tabla trazable y reporte de calidad.

## 3. Desarrollar la consulta de itinerario

- [ ] Validar paradas y fechas.
- [ ] Relacionar destinos con la escala disponible.
- [ ] Mostrar históricos, corte, fuentes y estados de cobertura.
- [ ] Incorporar enlaces y orientación oficial revisada.
- [ ] Resolver fechas lejanas y destinos sin datos.

**Salida:** recorrido consultable, aun cuando no exista pronóstico.

## 4. Evaluar el primer modelo

- [ ] Fijar particiones temporales y baseline.
- [ ] Entrenar un candidato y comparar resultados por grupo.
- [ ] Medir el aporte adicional del clima y, si aplica, de los índices de El Niño.
- [ ] Guardar métricas, predicciones de prueba y ficha del modelo.
- [ ] Integrar solo resultados identificados como experimentales y dentro de cobertura.

**Salida:** evaluación reproducible, incluyendo resultados sin mejora.

## 5. Validar el producto

- [ ] Probar con viajeros la comprensión de fuente, fecha, escala y estimación.
- [ ] Evaluar criterios de comparación con Ingeniería Industrial.
- [ ] Corregir mensajes que confundan faltantes con ausencia de riesgo.
- [ ] Fijar dependencias y documentar los comandos reales cuando existan.
- [ ] Ensayar la demo y preparar un respaldo identificado.

**Salida:** evidencia del uso y entrega coherente con lo implementado.

## Posibles ampliaciones

Más países, otras enfermedades, resolución subnacional, comparación de itinerarios y optimización con presupuesto/duración. Solo incorporar ampliaciones tras completar el flujo principal y verificar datos.
