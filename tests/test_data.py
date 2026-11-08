from datetime import date
import importlib.util
from pathlib import Path
import pandas as pd
import pytest
from src.data.calendar import epi_week, week_start, weeks_in_year
from src.data.ingestion import aggregate_notifications, aggregate_malaria, aggregate_weather
from src.data.pilot import load_pilot, select_period, validate


@pytest.mark.parametrize("day,expected", [(date(2024, 1, 1), (2024, 1)), (date(2009, 1, 1), (2008, 53)), (date(2010, 1, 3), (2010, 1)), (date(2024, 12, 29), (2025, 1))])
def test_calendar_boundaries(day, expected):
    assert epi_week(day) == expected
    y, w = expected
    assert 0 <= (day - week_start(y, w)).days <= 6


def test_calendar_no_fake_53():
    assert weeks_in_year(2009) == 52
    assert weeks_in_year(2008) == 53
    with pytest.raises(ValueError):
        week_start(2009, 53)


def notifications():
    return pd.DataFrame([dict(departamento="PIURA", provincia="SULLANA", ano=2009, semana=1, diagnostic="A27", tipo_dx=kind) for kind in ["C", "P", "S"]])


def test_types_stay_separate_without_fabricated_weeks():
    result, rejected = aggregate_notifications(notifications(), ["A27"])
    assert len(result) == 3
    assert set(result.tipo_dx) == {"C", "P", "S"}
    assert result.registros.tolist() == [1, 1, 1]
    assert rejected.empty


def test_invalid_week_and_unselected_diagnosis_preserved():
    frame = notifications()
    frame.loc[0, "semana"] = 53
    frame.loc[1, "diagnostic"] = "OTHER"
    result, rejected = aggregate_notifications(frame, ["A27"])
    assert len(result) == 1
    assert len(rejected) == 2
    assert 53 in rejected.semana.values


def test_unknown_case_type_not_silently_confirmed():
    frame = notifications()
    frame.loc[0, "tipo_dx"] = None
    result, rejected = aggregate_notifications(frame, ["A27"])
    assert len(rejected) == 1
    assert "C" not in result.tipo_dx.values


def test_malaria_missing_species_not_zero():
    frame = notifications().iloc[:2].copy()
    frame["falciparum"] = [2, None]
    frame["vivax"] = [3, 4]
    result, rejected = aggregate_malaria(frame, aggregated=True)
    assert len(result) == 1
    assert result.falciparum.iloc[0] == 2
    assert len(rejected) == 1


def test_daily_weather_partial_week_not_complete():
    frame = pd.DataFrame({"provincia": ["PIURA"] * 8, "time": pd.date_range("2024-01-07", periods=8),
                          "temperature_2m_mean": [28.] * 8, "precipitation_sum": [1.] * 8, "relative_humidity_2m_mean": [70.] * 8})
    result = aggregate_weather(frame)
    assert result.semana.tolist() == [2, 3]
    assert result.semana_completa.tolist() == [True, False]
    assert result.precipitation_sum.iloc[0] == 7
    assert pd.isna(result.precipitation_sum.iloc[1])
    with pytest.raises(ValueError, match="duplicado"):
        aggregate_weather(pd.concat([frame, frame.iloc[:1]]))


def test_snapshot_and_overlap():
    data = load_pilot()
    assert len(data) == 5376
    # Wednesday maps to the complete Sunday–Saturday week, not zero rows.
    selected = select_period(data, "PIURA", "2024-01-10", "2024-01-10")
    assert len(selected) == 1
    assert selected.inicio_semana.iloc[0] == pd.Timestamp("2024-01-07")
    assert select_period(data, "PIURA", "2030-01-01", "2030-02-01").empty
    with pytest.raises(ValueError):
        select_period(data, "PIURA", "2025-01-01", "2024-01-01")


@pytest.mark.parametrize("problem", ["duplicate", "negative", "wrong_date", "missing", "fractional", "infinity"])
def test_invalid_snapshot_rejected(problem):
    data = load_pilot().iloc[:3].copy()
    if problem == "duplicate": data = pd.concat([data, data.iloc[:1]])
    elif problem == "negative": data.loc[0, "casos_confirmados"] = -1
    elif problem == "wrong_date": data.loc[0, "inicio_semana"] += pd.Timedelta(days=1)
    elif problem == "missing": data.loc[0, "lluvia_total"] = float("nan")
    elif problem == "fractional": data["ano"] = data.ano + .5
    elif problem == "infinity": data.loc[0, "tmax_promedio"] = float("inf")
    with pytest.raises(ValueError): validate(data)


def test_importing_entrypoints_does_not_download_or_write(monkeypatch):
    import requests
    def forbidden(*args, **kwargs): raise AssertionError("Import must not download")
    monkeypatch.setattr(requests, "get", forbidden)
    directory = Path(__file__).resolve().parents[1] / "Programas/Adquisición de datos"
    for path in directory.glob("*.py"):
        spec = importlib.util.spec_from_file_location("review_" + path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
