"""Carga y consulta del snapshot histórico, sin imputaciones ni pronósticos."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from .calendar import week_start

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data/processed/dengueshield_dataset_integrado_REVISION.csv"
PROVINCES = {"PIURA": "Piura", "SULLANA": "Sullana", "MORROPON": "Morropón", "PAITA": "Paita"}
VALUES = ["casos_confirmados", "casos_probables", "tmax_promedio", "tmin_promedio", "lluvia_total"]


def validate(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"provincia", "ano", "semana", "inicio_semana", "anio_sin_casos_registrados", *VALUES}
    if required - set(frame):
        raise ValueError(f"Columnas ausentes: {sorted(required - set(frame))}")
    data = frame.copy()
    if data.empty or data[list(required)].isna().any().any():
        raise ValueError("Snapshot vacío o con valores faltantes: requiere revisión")
    if not set(data.provincia).issubset(PROVINCES):
        raise ValueError("Provincia fuera del piloto")
    if data.duplicated(["provincia", "ano", "semana"]).any():
        raise ValueError("Claves de provincia, año y semana duplicadas")
    data[VALUES + ["ano", "semana"]] = data[VALUES + ["ano", "semana"]].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(data[VALUES + ["ano", "semana"]].to_numpy()).all():
        raise ValueError("Valores no finitos")
    counts = ["casos_confirmados", "casos_probables"]
    if (data[counts + ["lluvia_total"]] < 0).any().any() or data[counts + ["ano", "semana"]].mod(1).ne(0).any().any():
        raise ValueError("Conteos negativos o claves/conteos no enteros")
    if (data.tmin_promedio > data.tmax_promedio).any():
        raise ValueError("Temperatura mínima mayor que la máxima")
    flags = data.anio_sin_casos_registrados.astype(str).str.lower()
    if not flags.isin(["true", "false"]).all():
        raise ValueError("Bandera de calidad inválida")
    data["anio_sin_casos_registrados"] = flags.eq("true")
    data["inicio_semana"] = pd.to_datetime(data.inicio_semana, errors="raise")
    expected = pd.to_datetime([week_start(int(y), int(w)) for y, w in zip(data.ano, data.semana)])
    if not (data.inicio_semana.to_numpy() == expected.to_numpy()).all():
        raise ValueError("Fecha y semana no coinciden con el calendario provisional")
    return data.sort_values(["provincia", "inicio_semana"]).reset_index(drop=True)


def load_pilot(path=DATASET):
    return validate(pd.read_csv(path))


def select_period(data, province, start, end):
    if province not in PROVINCES:
        raise ValueError("Provincia fuera del piloto")
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    if start > end:
        raise ValueError("La fecha inicial debe ser anterior o igual a la final")
    # Una semana se incluye si se solapa con el periodo. No prorratear casos.
    selected = data.loc[data.provincia.eq(province) & data.inicio_semana.le(end)
                        & (data.inicio_semana + pd.Timedelta(days=6)).ge(start)].copy()
    return selected


def audit(data, path=DATASET):
    gaps = {}
    for province, part in data.groupby("provincia"):
        expected = pd.date_range(part.inicio_semana.min(), part.inicio_semana.max(), freq="7D")
        gaps[province] = len(expected.difference(part.inicio_semana))
    climate = ["tmax_promedio", "tmin_promedio", "lluvia_total"]
    a = data.loc[data.provincia.eq("PIURA")].set_index("inicio_semana")[climate]
    b = data.loc[data.provincia.eq("SULLANA")].set_index("inicio_semana")[climate]
    shared = a.index.intersection(b.index)
    return {"sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            "filas": len(data), "semanas_ausentes_por_provincia": gaps,
            "filas_con_cero_confirmados": int(data.casos_confirmados.eq(0).sum()),
            "filas_anio_sin_casos": int(data.anio_sin_casos_registrados.sum()),
            "semanas_clima_identico_piura_sullana": int(a.loc[shared].eq(b.loc[shared]).all(axis=1).sum()),
            "calendario": "provisional_domingo_semana_del_4_de_enero",
            "validacion_con_fuente_original": False}
