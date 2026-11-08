import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from src.data.malaria import audit_department, catalog, load_department, prepare, select_year
from src.data.ingestion import aggregate_malaria

ROOT = Path(__file__).resolve().parents[1]


def sample():
    return pd.DataFrame({"ano": [2008, 2009, 2009], "semana": [53, 1, 53],
                         "provincia": ["A"] * 3, "malaria_total": [5, 10, 7]})


def test_original_values_and_calendar_review_preserved():
    data = prepare(sample(), "TEST")
    assert data.malaria_total.sum() == 22
    assert data.calendario_revision.tolist() == [False, False, True]
    assert data.etiqueta_semana.tolist() == ["2008-SE53", "2009-SE01", "2009-SE53"]
    assert select_year(data, "A", "2000–2008", 2008).malaria_total.sum() == 5
    assert select_year(data, "A", "2009–2025", 2009).malaria_total.sum() == 17


def test_absent_year_is_empty_not_zero():
    data = prepare(sample(), "TEST")
    assert select_year(data, "A", "2009–2025", 2024).empty
    with pytest.raises(ValueError, match="periodo"):
        select_year(data, "A", "2000–2008", 2009)


@pytest.mark.parametrize("column,value", [("semana", 54), ("semana", 0), ("ano", 2026),
                                         ("malaria_total", -1), ("malaria_total", 1.5),
                                         ("malaria_total", np.inf), ("provincia", " "), ("provincia", None)])
def test_invalid_file_rejected(column, value):
    data = sample().astype({"malaria_total": float})
    data.loc[0, column] = value
    with pytest.raises(ValueError):
        prepare(data, "TEST")


def test_duplicate_and_missing_column_rejected():
    with pytest.raises(ValueError, match="duplicados"):
        prepare(pd.concat([sample(), sample()]), "TEST")
    with pytest.raises(ValueError, match="columnas"):
        prepare(sample().drop(columns="malaria_total"), "TEST")


def test_all_repository_files_and_published_manifest():
    manifest = json.loads((ROOT / "reports/malaria/auditoria_archivos.json").read_text())
    assert len(catalog()) == manifest["departamentos"] == 22
    reports = [audit_department(name) for name in catalog()]
    assert reports == manifest["archivos"]
    assert sum(item["filas"] for item in reports) == 181578
    assert sum(item["suma_revision"] for item in reports) == 167


def test_department_coverage_does_not_cross_geography():
    data = load_department("LORETO")
    assert set(data.departamento) == {"LORETO"}
    with pytest.raises(ValueError, match="catálogo"):
        load_department("../../otra_ruta")
    with pytest.raises(ValueError, match="Provincia"):
        select_year(data, "LIMA", "2009–2025", 2024)


def test_raw_malaria_preserves_diagnostic_and_case_type():
    frame = pd.DataFrame([{"departamento": "LORETO", "provincia": "MAYNAS", "ano": 2024,
                           "semana": 1, "diagnostic": diagnosis, "tipo_dx": kind}
                          for diagnosis, kind in [("B50", "C"), ("B51", "C"), ("B51", "P")]])
    result, rejected = aggregate_malaria(frame, aggregated=False)
    assert rejected.empty
    assert len(result) == 3
    assert result.registros.sum() == 3
    result, _ = aggregate_malaria(frame.drop(columns=["diagnostic", "tipo_dx"]), aggregated=False)
    assert result.diagnostic.iloc[0] == "NO_INFORMADO"
    assert result.tipo_dx.iloc[0] == "NO_INFORMADO"
    assert result.registros.iloc[0] == 3


def malaria_app():
    app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=30).run()
    return app.radio(key="disease").set_value("Malaria").run()


def test_malaria_screen_and_department_change():
    app = malaria_app()
    assert not app.exception
    assert app.selectbox(key="malaria_department").value == "LORETO"
    assert len(app.metric) == 3
    app.selectbox(key="malaria_department").select("PIURA").run()
    assert not app.exception
    assert "Piura" in app.subheader[0].value
    data = load_department("PIURA")
    province = app.selectbox(key="malaria_province_PIURA_2009–2025").value
    expected = int(select_year(data, province, "2009–2025", 2024).malaria_total.sum())
    assert app.metric[0].value == f"{expected:,}".replace(",", ".")


def test_switch_source_period_and_back_to_dengue():
    app = malaria_app()
    app.selectbox(key="malaria_period").select("2000–2008").run()
    assert not app.exception
    assert app.selectbox(key="malaria_year_2000–2008").value == 2008
    assert any("falciparum" in item.value for item in app.caption)
    app.radio(key="disease").set_value("Dengue").run()
    assert not app.exception
    assert app.metric[0].label == "Confirmados registrados"
