"""Transformaciones puras: registros presentes, diagnósticos separados y cuarentena."""
import pandas as pd
import numpy as np
from .calendar import epi_week, week_start

KEYS = ["departamento", "provincia", "ano", "semana"]


def separate_invalid(frame: pd.DataFrame, required: list[str]):
    missing = set(required) - set(frame.columns)
    if missing:
        raise ValueError(f"Columnas ausentes: {sorted(missing)}")
    data = frame.copy()
    reasons = pd.Series("", index=data.index, dtype="object")
    for field in required:
        absent = data[field].isna() | data[field].astype(str).str.strip().eq("")
        reasons.loc[absent] += f"{field} ausente; "
    for field in ["ano", "semana"]:
        values = pd.to_numeric(data[field], errors="coerce")
        invalid = ~np.isfinite(values) | values.mod(1).ne(0)
        reasons.loc[invalid] += f"{field} no entero; "
        data[field] = values
    dates = []
    for i, row in data.iterrows():
        try:
            if reasons.loc[i]:
                raise ValueError("Campos inválidos")
            dates.append(week_start(int(row.ano), int(row.semana)))
        except (ValueError, OverflowError):
            dates.append(pd.NaT)
            reasons.loc[i] += "calendario pendiente; "
    data["inicio_semana"] = pd.to_datetime(dates)
    rejected = frame.loc[reasons.ne("")].copy()
    rejected["motivo_revision"] = reasons.loc[reasons.ne("")]
    valid = data.loc[reasons.eq("")].copy()
    valid[["ano", "semana"]] = valid[["ano", "semana"]].astype(int)
    return valid, rejected


def aggregate_notifications(frame: pd.DataFrame, codes: list[str]):
    valid, rejected = separate_invalid(frame.reset_index(drop=True), KEYS + ["diagnostic", "tipo_dx"])
    # Conservar diagnósticos ajenos a esta selección en el reporte, sin perderlos.
    outside = ~valid.diagnostic.isin(codes)
    other = valid.loc[outside].copy()
    other["motivo_revision"] = "diagnóstico fuera de la selección"
    rejected = pd.concat([rejected, other], ignore_index=True)
    groups = KEYS + ["inicio_semana", "diagnostic", "tipo_dx"]
    result = valid.loc[~outside].groupby(groups, dropna=False).size().reset_index(name="registros")
    # Ausencia de fila no se convierte en cero; registros no equivale a casos confirmados.
    return result.sort_values(groups).reset_index(drop=True), rejected


def aggregate_malaria(frame: pd.DataFrame, aggregated: bool):
    extra = ["falciparum", "vivax"] if aggregated else []
    valid, rejected = separate_invalid(frame.reset_index(drop=True), KEYS + extra)
    groups = KEYS + ["inicio_semana"]
    if aggregated:
        numeric = valid[extra].apply(pd.to_numeric, errors="coerce")
        bad = (~np.isfinite(numeric)).any(axis=1) | (numeric < 0).any(axis=1) | numeric.mod(1).ne(0).any(axis=1)
        rejected_counts = valid.loc[bad].copy()
        rejected_counts["motivo_revision"] = "conteo ausente, negativo o no entero"
        rejected = pd.concat([rejected, rejected_counts], ignore_index=True)
        valid = valid.loc[~bad].copy()
        valid[extra] = numeric.loc[~bad].astype(int)
        result = valid.groupby(groups)[extra].sum(min_count=1).reset_index()
        result["tipo_registro"] = "conteos_agregados_falciparum_vivax"
    else:
        # No asumir que todas las filas son confirmadas ni unirlas al total agregado.
        if "tipo_dx" not in valid:
            valid["tipo_dx"] = "NO_INFORMADO"
        valid["tipo_dx"] = valid.tipo_dx.fillna("NO_INFORMADO").replace("", "NO_INFORMADO")
        result = valid.groupby(groups + ["tipo_dx"]).size().reset_index(name="registros")
        result["tipo_registro"] = "notificaciones_individuales"
    return result, rejected


def aggregate_weather(frame: pd.DataFrame):
    variables = ["temperature_2m_mean", "precipitation_sum", "relative_humidity_2m_mean"]
    required = ["provincia", "time"] + variables
    if set(required) - set(frame.columns):
        raise ValueError("Faltan columnas de clima diario")
    data = frame[required].copy()
    data["time"] = pd.to_datetime(data.time, errors="raise").dt.normalize()
    if data[["provincia", "time"]].isna().any().any():
        raise ValueError("Provincia o fecha ausente")
    if data.duplicated(["provincia", "time"]).any():
        raise ValueError("Clima diario duplicado por provincia y fecha")
    data[variables] = data[variables].apply(pd.to_numeric, errors="raise")
    if np.isinf(data[variables].to_numpy()).any():
        raise ValueError("Clima contiene valores infinitos")
    if (data.precipitation_sum < 0).any() or (~data.relative_humidity_2m_mean.dropna().between(0, 100)).any():
        raise ValueError("Precipitación o humedad inválida")
    data[["ano", "semana"]] = pd.DataFrame([epi_week(d.date()) for d in data.time], index=data.index)
    rows = []
    for (province, year, week), part in data.groupby(["provincia", "ano", "semana"]):
        row = {"provincia": province, "ano": year, "semana": week,
               "inicio_semana": week_start(year, week), "dias_presentes": len(part)}
        complete = len(part) == 7 and part[variables].notna().all().all()
        row["semana_completa"] = complete
        for var in variables:
            row[var] = (part[var].sum() if var == "precipitation_sum" else part[var].mean()) if complete else float("nan")
        rows.append(row)
    return pd.DataFrame(rows, columns=["provincia", "ano", "semana", "inicio_semana", "dias_presentes", "semana_completa"] + variables)
