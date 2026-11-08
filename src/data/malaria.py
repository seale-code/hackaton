"""Consulta de los CSV históricos del equipo, preservando etiquetas y conteos.

No reinterpreta semana 53 ni fusiona definiciones entre los dos periodos de origen.
No usa los CSV derivados como si fueran una nueva descarga de la fuente oficial.
"""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from .calendar import weeks_in_year
from .pilot import ROOT

DIRECTORY = ROOT / "Programas/Adquisición de datos/vigilancia_malaria"
PERIODS = {"2000–2008": (2000, 2008), "2009–2025": (2009, 2025)}
DEFINITIONS = {"2000–2008": "Suma histórica de falciparum y vivax",
               "2009–2025": "Conteo histórico de notificaciones individuales"}
# Display-only aliases. Original values and identifiers remain untouched in exports.
DISPLAY_ALIASES = {"CA�ETE": "Cañete", "DATEM DEL MARA�ON": "Datem del Marañón",
                   "FERRE�AFE": "Ferreñafe", "MARA�ON": "Marañón"}


def display_name(value):
    return DISPLAY_ALIASES.get(value, value.title())


def catalog(directory=DIRECTORY):
    files = sorted(Path(directory).glob("malaria_2000-2025_*.csv"))
    if not files:
        raise ValueError("No se encontraron archivos departamentales de malaria")
    return {p.stem.removeprefix("malaria_2000-2025_").upper(): p for p in files}


def prepare(frame, department):
    required = ["ano", "semana", "provincia", "malaria_total"]
    if set(required) - set(frame):
        raise ValueError("Faltan columnas de año, semana, provincia o malaria_total")
    data = frame[required].copy()
    if data.empty or data.isna().any().any():
        raise ValueError("Archivo vacío o con valores ausentes")
    if not data.provincia.map(lambda value: isinstance(value, str) and bool(value.strip())).all():
        raise ValueError("Provincia inválida")
    numbers = ["ano", "semana", "malaria_total"]
    data[numbers] = data[numbers].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(data[numbers]).all().all() or data[numbers].mod(1).ne(0).any().any():
        raise ValueError("Años, semanas y conteos deben ser enteros finitos")
    if not data.ano.between(2000, 2025).all() or not data.semana.between(1, 53).all():
        raise ValueError("Año o semana fuera del contrato del archivo histórico")
    if data.malaria_total.lt(0).any():
        raise ValueError("Conteos negativos")
    if data.duplicated(["provincia", "ano", "semana"]).any():
        raise ValueError("Provincia, año y semana duplicados")
    data[numbers] = data[numbers].astype("int64")
    data.insert(0, "departamento", department)
    data["periodo_fuente"] = np.where(data.ano.le(2008), "2000–2008", "2009–2025")
    data["definicion_conteo"] = data.periodo_fuente.map(DEFINITIONS)
    data["etiqueta_semana"] = data.ano.astype(str) + "-SE" + data.semana.astype(str).str.zfill(2)
    # Flag for review, NOT a reason to delete or reassign records.
    data["calendario_revision"] = data.semana.gt(data.ano.map(weeks_in_year))
    data["cero_heredado_no_verificado"] = data.malaria_total.eq(0)
    data["nombre_con_caracter_danado"] = data.provincia.str.contains("�", regex=False)
    return data.sort_values(["provincia", "ano", "semana"]).reset_index(drop=True)


def load_department(department, directory=DIRECTORY):
    files = catalog(directory)
    if department not in files:
        raise ValueError("Departamento fuera del catálogo de malaria")
    data = prepare(pd.read_csv(files[department], encoding="utf-8"), department)
    data["archivo_fuente"] = files[department].name
    return data


def select_year(data, province, period, year):
    if period not in PERIODS:
        raise ValueError("Periodo de origen desconocido")
    lo, hi = PERIODS[period]
    if not lo <= year <= hi:
        raise ValueError("El año debe pertenecer al periodo seleccionado")
    if province not in data.provincia.values:
        raise ValueError("Provincia fuera del departamento seleccionado")
    return data.loc[data.provincia.eq(province) & data.periodo_fuente.eq(period) & data.ano.eq(year)].copy()


def audit_department(department, directory=DIRECTORY):
    path = catalog(directory)[department]
    data = load_department(department, directory)
    review = data.loc[data.calendario_revision]
    return {"departamento": department, "archivo": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "filas": len(data), "provincias": data.provincia.nunique(),
            "periodos": {period: {"filas": int(len(part)), "suma_archivo": int(part.malaria_total.sum())}
                         for period, part in data.groupby("periodo_fuente")},
            "filas_calendario_revision": len(review),
            "filas_revision_con_valor": int(review.malaria_total.gt(0).sum()),
            "suma_revision": int(review.malaria_total.sum()),
            "filas_con_cero": int(data.cero_heredado_no_verificado.sum()),
            "nombres_con_caracter_danado": sorted(data.loc[data.nombre_con_caracter_danado, "provincia"].unique().tolist()),
            "procedencia": "CSV derivado del equipo; no descarga oficial verificada",
            "calendario": "etiquetas originales; revisión según convención provisional del piloto"}
