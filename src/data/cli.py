"""Descarga optativa o CSV local; salidas nuevas y trazabilidad por ejecución."""
import argparse
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import hashlib
import json
import pandas as pd
import requests
from .ingestion import aggregate_malaria, aggregate_notifications, aggregate_weather
from .pilot import ROOT

SOURCES = {
    "dengue": ["https://www.datosabiertos.gob.pe/node/23482/download"],
    "zoonosis": ["https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_zoonosis_2000_2025_0.csv"],
    "malaria": ["https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_malaria_2000_2008.csv",
                "https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_malaria_2009_2025.csv"],
}

CLIMATE_POINTS = {"Piura": (-5.19, -80.63), "Sullana": (-4.90, -80.69),
                  "Talara": (-4.58, -81.27), "Paita": (-5.09, -81.11),
                  "Sechura": (-5.56, -80.82), "Ayabaca": (-4.64, -79.71),
                  "Huancabamba": (-5.24, -79.45), "Morropón": (-5.19, -79.97)}


def download_climate():
    frames, provenance, payloads = [], [], []
    url = "https://archive-api.open-meteo.com/v1/archive"
    for province, (latitude, longitude) in CLIMATE_POINTS.items():
        params = {"latitude": latitude, "longitude": longitude, "start_date": "2001-01-01",
                  "end_date": "2025-12-31", "timezone": "America/Lima",
                  "daily": "temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean"}
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        frame = pd.DataFrame(response.json()["daily"])
        frame["provincia"] = province
        frames.append(frame)
        payloads.append((response.content, "json"))
        provenance.append({"source": url, "params": params, "provincia": province,
                           "sha256": hashlib.sha256(response.content).hexdigest(),
                           "read_at_utc": datetime.now(timezone.utc).isoformat(), "rows": len(frame)})
    return [pd.concat(frames, ignore_index=True)], provenance, payloads


def main(kind=None):
    parser = argparse.ArgumentParser(description=__doc__)
    if kind is None:
        parser.add_argument("kind", choices=[*SOURCES, "clima"])
    parser.add_argument("--input", type=Path, nargs="+", help="CSV locales; malaria: agregado y luego individual")
    parser.add_argument("--download", action="store_true", help="Descargar las fuentes; requiere red")
    parser.add_argument("--output", type=Path, help="Directorio nuevo; no sobrescribir resultados anteriores")
    args = parser.parse_args()
    kind = kind or args.kind
    if bool(args.input) == args.download:
        parser.error("Usa --input o --download, exactamente uno")
    expected = 2 if kind == "malaria" else 1
    if args.input and len(args.input) != expected:
        parser.error(f"{kind} requiere {expected} archivo(s)")
    output = args.output or ROOT / "data/interim" / f"{kind}_v2_{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}"
    if output.exists():
        parser.error("El directorio de salida ya existe; elige uno nuevo")
    frames, provenance, payloads = [], [], []
    sources = args.input or SOURCES.get(kind, [])
    if kind == "clima" and args.download:
        frames, provenance, payloads = download_climate()
    for source in sources:
        if args.input:
            payload = source.read_bytes()
        else:
            response = requests.get(source, headers={"User-Agent": "HACKATON-data-review/1.0"}, timeout=60)
            response.raise_for_status()
            payload = response.content
        frames.append(pd.read_csv(BytesIO(payload), low_memory=False))
        payloads.append((payload, "csv"))
        provenance.append({"source": str(source), "sha256": hashlib.sha256(payload).hexdigest(),
                           "read_at_utc": datetime.now(timezone.utc).isoformat(), "rows": len(frames[-1])})
    results = []
    if kind == "malaria":
        for label, frame, aggregated in zip(["2000_2008", "2009_2025"], frames, [True, False]):
            ok, rejected = aggregate_malaria(frame, aggregated)
            results.append((label, ok, rejected))
    elif kind == "clima":
        results.append(("semanal", aggregate_weather(frames[0]), pd.DataFrame()))
    else:
        codes = ["A27", "X20", "X21"] if kind == "zoonosis" else ["A97.0", "A97.1", "A97.2"]
        frame = frames[0]
        if kind == "dengue":
            if "departamento" not in frame:
                raise ValueError("Falta departamento")
            frame = frame.loc[frame.departamento.eq("PIURA")]
        ok, rejected = aggregate_notifications(frame, codes)
        results.append(("notificaciones", ok, rejected))
    output.mkdir(parents=True, exist_ok=False)
    for i, (payload, extension) in enumerate(payloads, 1):
        (output / f"fuente_{i}.{extension}").write_bytes(payload)
    for label, ok, rejected in results:
        ok.to_csv(output / f"{label}.csv", index=False)
        rejected.to_csv(output / f"{label}_revision.csv", index=False)
    metadata = {"kind": kind, "sources": provenance,
                "calendar": "provisional_domingo_semana_del_4_de_enero",
                "missing_weeks": "sin fila; no se imputan ceros",
                "outputs": [{"name": label, "rows": len(ok), "review_rows": len(rejected)} for label, ok, rejected in results]}
    (output / "manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
