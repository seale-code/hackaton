# Alcance implementado del piloto

La visión es una guía climática y sanitaria para viajeros en Sudamérica. La aplicación ofrece **dengue en Piura, Sullana, Morropón y Paita**, y **malaria por provincia en los 22 archivos departamentales disponibles de Perú**, a escala semanal. Dengue conserva el piloto de la ficha técnica; malaria amplía la consulta histórica con los archivos aportados por el equipo.

## Primera entrega

Para dengue: consulta de provincia y fechas, históricos de casos confirmados/probables y clima. Para malaria: departamento, provincia, periodo de origen y año, con los conteos históricos del archivo. Ambas pantallas incluyen fuente, cobertura y CSV descargable. Funcionan sin conexión después de instalar dependencias. No hay cuentas ni datos clínicos del viajero.

La demo conserva los archivos existentes, sin regenerar ni corregir sus conteos. En dengue, las semanas que se solapan con el periodo se muestran completas, sin repartir casos por día. En malaria, se mantienen las etiquetas de año y semana originales, incluidas las que requieren revisión. Consultas sin datos no producen una estimación. Los enlaces oficiales son referencias, no una integración de alertas vigentes.

Existe un experimento separado de dengue confirmado a 1 y 2 semanas, evaluado retrospectivamente por fechas. No se aplica a malaria ni habilita pronósticos operativos en la demo.

## Pendientes antes de ampliar

1. Confirmar calendario y diferenciar ceros observados de faltantes desde las fuentes originales.
2. Verificar fechas de disponibilidad de casos y clima; revisar los puntos Piura/Sullana.
3. Evaluar con series corregidas y periodos adicionales.
4. Implementar hasta cuatro paradas de itinerario y probar comprensión con viajeros.
5. Seleccionar nuevos territorios y enfermedades según cobertura comparable.

Malaria incorpora consulta histórica por departamento, provincia y año, con los periodos de origen separados; ver [MALARIA.md](MALARIA.md). Zoonosis conserva un adaptador exploratorio y no se muestra en la aplicación. Zika, chikungunya, otros países y optimización de rutas son ampliaciones futuras.

## Fuera de alcance

Diagnóstico, probabilidad individual de infección, prescripción, certificación de viaje seguro, alertas oficiales propias, cobertura continental y promesas de reducción de contagios.
