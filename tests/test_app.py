from datetime import date
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "streamlit_app.py"


def test_default_and_province_change():
    app = AppTest.from_file(str(APP), default_timeout=30).run()
    assert not app.exception
    assert len(app.metric) == 3
    assert app.metric[2].value == "53"
    app.selectbox(key="province").select("PAITA").run()
    assert not app.exception
    assert app.subheader[0].value == "Paita"


def test_future_dates_have_no_fake_metrics():
    app = AppTest.from_file(str(APP), default_timeout=30).run()
    app.date_input(key="start").set_value(date(2030, 1, 1))
    app.date_input(key="end").set_value(date(2030, 2, 1)).run()
    assert not app.exception
    assert len(app.metric) == 0
    assert any("No hay datos" in message.value for message in app.info)


def test_reversed_dates_stop_with_explanation():
    app = AppTest.from_file(str(APP), default_timeout=30).run()
    app.date_input(key="start").set_value(date(2025, 1, 1)).run()
    assert not app.exception
    assert len(app.error) == 1
    assert len(app.metric) == 0
