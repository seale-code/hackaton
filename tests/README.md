# Comprobaciones ejecutables

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/audit_pilot.py
```

Pruebas: límites de calendario; semanas inválidas conservadas; ausencia de ceros fabricados; separación de diagnósticos; clima parcial/duplicado; snapshot inválido; consulta por solapamiento; cortes de entrenamiento y objetivos; variables sin información futura; misma muestra para modelos; arranque y cambios de provincia/fechas en Streamlit mediante AppTest. No necesitan red ni descargas oficiales.

GitHub Actions ejecuta la suite con Python 3.12. Se comprobó el arranque y las interacciones con AppTest. La revisión visual en navegador quedó pendiente: el navegador de esta sesión no pudo acceder al servidor local. No se han realizado pruebas con viajeros.
