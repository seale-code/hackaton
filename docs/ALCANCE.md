# Alcance implementado del piloto

La visión es una guía climática y sanitaria para viajeros en Sudamérica. El piloto ejecutable se limita a **dengue en Piura, Sullana, Morropón y Paita**, a escala provincial y semanal. Esta decisión sustituye la propuesta anterior de iniciar con dos o tres países y alinea el código con la ficha técnica delimitada.

## Primera entrega

Consulta de una provincia y un intervalo de fechas, históricos de casos confirmados/probables y clima, fuente, cobertura, CSV descargable y avisos de limitaciones. Funciona sin conexión después de instalar dependencias. No hay cuentas ni datos clínicos del viajero.

La demo usa el snapshot existente en revisión, sin regenerar ni corregir sus conteos. Las semanas que se solapan con el periodo se muestran completas, sin repartir casos por día. Fechas fuera de cobertura no producen una estimación. Los enlaces oficiales son referencias, no una integración de alertas vigentes.

Existe un experimento separado de conteo confirmado a 1 y 2 semanas, evaluado retrospectivamente por fechas. No habilita pronósticos operativos en la demo.

## Pendientes antes de ampliar

1. Confirmar calendario y diferenciar ceros observados de faltantes desde las fuentes originales.
2. Verificar fechas de disponibilidad de casos y clima; revisar los puntos Piura/Sullana.
3. Evaluar con series corregidas y periodos adicionales.
4. Implementar hasta cuatro paradas de itinerario y probar comprensión con viajeros.
5. Seleccionar nuevos territorios y enfermedades según cobertura comparable.

Malaria y zoonosis tienen adaptadores exploratorios revisados, pero no amplían la cobertura de esta aplicación. Zika, chikungunya, otros países y optimización de rutas son ampliaciones futuras.

## Fuera de alcance

Diagnóstico, probabilidad individual de infección, prescripción, certificación de viaje seguro, alertas oficiales propias, cobertura continental y promesas de reducción de contagios.
