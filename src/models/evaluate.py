"""Experimento retrospectivo reproducible; no produce pronósticos operativos.

Entrena por provincia y horizonte. Variables en origen (al cierre de semana),
etiqueta h semanas después; todos los cruces son por fecha, nunca por posición.
Los retrasos reales de publicación no están disponibles en el snapshot.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import importlib.metadata
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.data.pilot import DATASET, load_pilot

BASE = ["casos_origen", "lag_1", "lag_2", "lag_3", "semana_sin", "semana_cos"]
CLIMATE = ["tmax_promedio", "tmin_promedio", "lluvia_total"]


def make_examples(part, horizon):
    if horizon not in (1, 2):
        raise ValueError("Horizonte admitido: 1 o 2 semanas")
    indexed = part.set_index("inicio_semana").sort_index()
    dates = pd.date_range(indexed.index.min(), indexed.index.max(), freq="7D")
    indexed = indexed.reindex(dates)
    # No llenar huecos ni años señalados sin casos registrados.
    cases = indexed.casos_confirmados.mask(indexed.anio_sin_casos_registrados.astype("boolean").fillna(True))
    examples = pd.DataFrame(index=dates)
    examples["origen"] = dates
    examples["corte"] = dates + pd.Timedelta(days=6)
    examples["objetivo_fecha"] = dates + pd.Timedelta(weeks=horizon)
    examples["objetivo_fin"] = examples.objetivo_fecha + pd.Timedelta(days=6)
    examples["casos_origen"] = cases
    for lag in [1, 2, 3]:
        examples[f"lag_{lag}"] = cases.shift(lag)
    # Calendario conocido; periodo anual aproximado, no codifica datos futuros.
    phase = 2 * np.pi * examples.index.dayofyear / 365.2425
    examples["semana_sin"], examples["semana_cos"] = np.sin(phase), np.cos(phase)
    examples[CLIMATE] = indexed[CLIMATE]
    examples["real"] = cases.shift(-horizon)
    examples["persistencia"] = cases
    examples["estacional_52"] = cases.shift(52 - horizon)
    return examples.dropna(subset=BASE + CLIMATE + ["real", "estacional_52"]).reset_index(drop=True)


def partition(examples, start, end):
    # Origen y objetivo deben pertenecer al bloque; purga el cruce de límites.
    return examples.loc[examples.origen.ge(pd.Timestamp(start)) & examples.objetivo_fin.le(pd.Timestamp(end))].copy()


def evaluate(data):
    records = []
    for province, part in data.groupby("provincia"):
        for horizon in (1, 2):
            examples = make_examples(part, horizon)
            train = partition(examples, "2001-01-01", "2021-12-31")
            validation = partition(examples, "2022-01-01", "2023-12-31")
            test = partition(examples, "2024-01-01", "2024-12-31")
            if len(train) < 104 or validation.empty or test.empty:
                raise ValueError(f"Historia insuficiente: {province}, horizonte {horizon}")
            models = {}
            for name, features in [("ridge_historia", BASE), ("ridge_clima", BASE + CLIMATE)]:
                # Alpha predefinido; no selección ni reajuste sobre prueba.
                model = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
                model.fit(train[features], train.real)
                models[name] = (model, features)
            for split, block in [("validacion", validation), ("prueba", test)]:
                predictions = {"persistencia": block.persistencia.to_numpy(), "estacional_52": block.estacional_52.to_numpy()}
                for name, (model, features) in models.items():
                    predictions[name] = np.maximum(0, model.predict(block[features]))
                for name, values in predictions.items():
                    result = block[["origen", "corte", "objetivo_fecha", "objetivo_fin", "real"]].copy()
                    result["prediccion"] = values
                    result["provincia"], result["horizonte"], result["particion"], result["modelo"] = province, horizon, split, name
                    result["n_entrenamiento"] = len(train)
                    records.append(result)
    predictions = pd.concat(records, ignore_index=True)
    predictions["error_absoluto"] = (predictions.real - predictions.prediccion).abs()
    metrics = predictions.groupby(["provincia", "horizonte", "particion", "modelo"], as_index=False).agg(
        n=("real", "size"), MAE=("error_absoluto", "mean"), n_entrenamiento=("n_entrenamiento", "first"))
    return predictions, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("reports/evaluacion_piloto"))
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Elige un directorio nuevo para conservar la evaluación anterior")
    data = load_pilot()
    predictions, metrics = evaluate(data)
    args.output.mkdir(parents=True)
    predictions.to_csv(args.output / "predicciones.csv", index=False)
    metrics.to_csv(args.output / "metricas.csv", index=False)
    metadata = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset": str(DATASET.relative_to(Path(__file__).resolve().parents[2])),
        "dataset_sha256": hashlib.sha256(DATASET.read_bytes()).hexdigest(),
        "evaluation_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "software": {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scikit-learn", "scipy"]},
        "objetivo": "conteo semanal confirmado de dengue", "horizontes_semanas": [1, 2],
        "train": "2001–2021", "validation": "2022–2023", "test": "2024",
        "features": {"historia": BASE, "clima": CLIMATE}, "alpha_ridge": 1.0,
        "negative_predictions": "recortadas a cero", "model_selection": "ninguna",
        "limitations": ["Snapshot en revisión; ceros previos no auditados con la fuente",
                        "Excluye años marcados sin casos; no certifica el resto de ceros",
                        "Calendario provisional y un caso de Sullana separado para revisión",
                        "No se reconstruyeron retrasos de publicación; variables asumidas conocidas al cierre de semana",
                        "Clima compartido Piura/Sullana pendiente de representatividad",
                        "No demuestra riesgo individual, utilidad con viajeros ni desempeño en tiempo real"]}
    (args.output / "manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
