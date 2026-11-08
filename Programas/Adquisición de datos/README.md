# Entradas de adquisición revisadas

Los scripts Python de esta carpeta ahora delegan a `src.data.cli` y no descargan al importarse. Desde la raíz, por ejemplo:

```bash
python "Programas/Adquisición de datos/procesamiento_malaria.py" --input /ruta/agregado.csv /ruta/individual.csv
python "Programas/Adquisición de datos/main.py" zoonosis --download
```

Los CSV en `vigilancia_malaria/` y `vigilancia_zoonosis/` se conservan como salidas del procesamiento previo, con sus límites: calendario de 53 semanas y ceros de relleno. Las ejecuciones v2 crean salidas separadas en `data/interim/`, preservan tipos de diagnóstico y guardan incompatibles en revisión. No regeneran ni reemplazan esos CSV automáticamente. Ver [contrato](../../docs/DATOS.md).
