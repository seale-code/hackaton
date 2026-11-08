import numpy as np
import pandas as pd
from src.data.pilot import load_pilot
from src.models.evaluate import make_examples, partition, evaluate


def test_horizons_use_dates_and_no_future_features():
    part = load_pilot().query("provincia == 'PIURA'")
    first = make_examples(part, 2)
    assert ((first.objetivo_fecha - first.origen).dt.days == 14).all()
    origin = pd.Timestamp("2020-06-07")
    changed = part.copy()
    changed.loc[changed.inicio_semana > origin, "casos_confirmados"] += 1000
    second = make_examples(changed, 2)
    cols = ["casos_origen", "lag_1", "lag_2", "lag_3", "estacional_52", "tmax_promedio"]
    np.testing.assert_allclose(first.loc[first.origen.eq(origin), cols], second.loc[second.origen.eq(origin), cols])
    assert first.loc[first.origen.eq(origin), "real"].iloc[0] != second.loc[second.origen.eq(origin), "real"].iloc[0]


def test_split_purges_targets_crossing_year():
    examples = make_examples(load_pilot().query("provincia == 'PIURA'"), 2)
    train = partition(examples, "2001-01-01", "2021-12-31")
    test = partition(examples, "2024-01-01", "2024-12-31")
    assert train.objetivo_fecha.max() < pd.Timestamp("2022-01-01")
    assert train.objetivo_fin.max() < pd.Timestamp("2022-01-01")
    assert test.origen.min() >= pd.Timestamp("2024-01-01")
    assert test.objetivo_fecha.max() <= pd.Timestamp("2024-12-31")
    assert test.objetivo_fin.max() <= pd.Timestamp("2024-12-31")


def test_partial_target_week_excluded_at_split_boundary():
    # La semana del 26/12 termina el 01/01: su etiqueta no puede entrenarse en 2021.
    examples = pd.DataFrame({"origen": pd.to_datetime(["2021-12-19"]),
                             "objetivo_fecha": pd.to_datetime(["2021-12-26"]),
                             "objetivo_fin": pd.to_datetime(["2022-01-01"])})
    assert partition(examples, "2001-01-01", "2021-12-31").empty


def test_gap_not_treated_as_next_week():
    part = load_pilot().query("provincia == 'PIURA'")
    part = part.loc[part.inicio_semana.ne(pd.Timestamp("2020-06-14"))]
    examples = make_examples(part, 1)
    assert pd.Timestamp("2020-06-07") not in examples.origen.tolist()


def test_evaluation_all_models_share_targets():
    predictions, metrics = evaluate(load_pilot())
    assert len(metrics) == 4 * 2 * 2 * 4
    assert np.isfinite(metrics.MAE).all()
    assert (predictions.prediccion >= 0).all()
    counts = metrics.groupby(["provincia", "horizonte", "particion"]).n.nunique()
    assert counts.eq(1).all()
