import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
from src.data import cli

ROOT = Path(__file__).resolve().parents[1]


def test_local_zoonosis_cli_preserves_inputs_and_types(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text("departamento,provincia,ano,semana,diagnostic,tipo_dx\nPIURA,SULLANA,2009,1,A27,C\nPIURA,SULLANA,2009,1,A27,P\nPIURA,SULLANA,2009,53,A27,C\n")
    output = tmp_path / "run"
    command = [sys.executable, "-m", "src.data.cli", "zoonosis", "--input", str(source), "--output", str(output)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (output / "fuente_1.csv").read_bytes() == source.read_bytes()
    table = pd.read_csv(output / "notificaciones.csv")
    assert set(table.tipo_dx) == {"C", "P"}
    assert len(table) == 2
    assert len(pd.read_csv(output / "notificaciones_revision.csv")) == 1
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["sources"][0]["rows"] == 3
    repeat = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert repeat.returncode != 0
    assert "ya existe" in repeat.stderr


def test_climate_download_is_explicit_and_records_query(tmp_path, monkeypatch):
    class Response:
        content = b'{"daily": {}}'

        def raise_for_status(self):
            pass

        def json(self):
            return {"daily": {"time": ["2024-01-07"], "temperature_2m_mean": [28.0],
                              "precipitation_sum": [2.0], "relative_humidity_2m_mean": [70.0]}}

    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return Response()

    monkeypatch.setattr(cli.requests, "get", fake_get)
    monkeypatch.setattr(cli, "CLIMATE_POINTS", {"Piura": (-5.19, -80.63)})
    output = tmp_path / "climate"
    monkeypatch.setattr(sys, "argv", ["cli", "clima", "--download", "--output", str(output)])
    cli.main()
    assert len(calls) == 1
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["sources"][0]["params"]["latitude"] == -5.19
    assert (output / "fuente_1.json").exists()
    assert pd.read_csv(output / "semanal.csv").temperature_2m_mean.isna().all()


def test_no_implicit_download():
    result = subprocess.run([sys.executable, "-m", "src.data.cli", "dengue"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert "exactamente uno" in result.stderr
