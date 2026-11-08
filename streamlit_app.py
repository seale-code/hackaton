"""Demo histórica del piloto de dengue. Ejecutar: streamlit run streamlit_app.py."""
from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st
from src.data.pilot import DATASET, PROVINCES, audit, load_pilot, select_period

st.set_page_config(page_title="Guía del viajero · Piura", page_icon="🧭", layout="wide")


@st.cache_data
def snapshot(version):
    return load_pilot()


st.caption("HACKATON FACI  /  PILOTO EN PERÚ")
st.title("Conoce el contexto de tu destino")
st.markdown("Explora el historial de **dengue y clima** en cuatro provincias de Piura.")
st.warning("Demo histórica en revisión. No muestra riesgo actual ni predice si una persona se enfermará.")
try:
    data = snapshot(DATASET.stat().st_mtime_ns)
except (OSError, ValueError) as exc:
    st.error(f"No se puede abrir el dataset del piloto: {exc}")
    st.stop()

with st.sidebar:
    st.header("Tu consulta")
    province = st.selectbox("Provincia", list(PROVINCES), format_func=PROVINCES.get, key="province")
    start = st.date_input("Desde", date(2024, 1, 1), min_value=date(2000, 1, 1), max_value=date(2035, 12, 31), key="start")
    end = st.date_input("Hasta", date(2024, 12, 31), min_value=date(2000, 1, 1), max_value=date(2035, 12, 31), key="end")
    st.caption("Puedes consultar fechas fuera de cobertura para comprobar si hay información disponible.")
    st.divider()
    st.markdown("**Cobertura del piloto**\n\nPiura · Sullana · Morropón · Paita")
    st.caption("Escala provincial · Frecuencia semanal · Datos locales, sin actualización automática")

try:
    selected = select_period(data, province, start, end)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

part = data.loc[data.provincia.eq(province)]
coverage_start = part.inicio_semana.min().date()
coverage_end = (part.inicio_semana.max() + pd.Timedelta(days=6)).date()
st.subheader(PROVINCES[province])
st.caption(f"Semanas disponibles: {coverage_start:%d/%m/%Y}–{coverage_end:%d/%m/%Y}. "
           "La última semana comienza el " + part.inicio_semana.max().strftime("%d/%m/%Y") +
           ". La fecha de extracción de la fuente original no está acreditada en este snapshot.")

if start < coverage_start or end > coverage_end:
    st.info("El periodo solicitado excede la cobertura. Los históricos disponibles no describen la situación actual ni completan las fechas faltantes.")

if selected.empty:
    st.info("No hay datos para estas fechas. Prueba un periodo histórico dentro de la cobertura indicada.")
else:
    st.caption("Se muestran semanas completas que se solapan con el periodo elegido; los casos no se prorratean por día.")
    a, b, c = st.columns(3)
    a.metric("Confirmados registrados", f"{int(selected.casos_confirmados.sum()):,}".replace(",", "."))
    b.metric("Probables registrados", f"{int(selected.casos_probables.sum()):,}".replace(",", "."))
    c.metric("Semanas en la consulta", len(selected))
    st.caption("Totales del archivo histórico en revisión. Los ceros pueden proceder de rellenos previos; no prueban ausencia de casos o riesgo.")
    if selected.anio_sin_casos_registrados.any():
        st.warning("La selección incluye años marcados sin casos registrados. Su cobertura debe verificarse con la fuente.")
    history, weather, records = st.tabs(["Casos por semana", "Clima histórico", "Datos de la consulta"])
    with history:
        timeline = selected.set_index("inicio_semana").reindex(pd.date_range(selected.inicio_semana.min(), selected.inicio_semana.max(), freq="7D"))
        timeline.index.name = "inicio_semana"
        chart = timeline.reset_index().rename(columns={"casos_confirmados": "Confirmados", "casos_probables": "Probables"})
        fig = px.line(chart, x="inicio_semana", y=["Confirmados", "Probables"],
                      color_discrete_sequence=["#087F8C", "#D17A22"], labels={"inicio_semana": "Inicio de semana", "value": "Registros", "variable": "Tipo"})
        fig.update_traces(connectgaps=False)
        fig.update_layout(legend_title_text="", margin=dict(l=0, r=0, t=20, b=0), height=350)
        st.plotly_chart(fig, width="stretch")
    with weather:
        st.caption("NASA POWER: puntos de referencia provinciales, no mediciones de toda la provincia. Datos históricos, no pronóstico meteorológico.")
        left, right = st.columns(2)
        with left:
            fig = px.line(timeline.reset_index(), x="inicio_semana", y=["tmax_promedio", "tmin_promedio"],
                          labels={"inicio_semana": "Inicio de semana", "value": "Temperatura (°C)", "variable": "Variable"},
                          color_discrete_sequence=["#D17A22", "#087F8C"])
            fig.update_traces(connectgaps=False)
            fig.update_layout(height=330, legend=dict(orientation="h"), margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, width="stretch")
        with right:
            fig = px.bar(selected, x="inicio_semana", y="lluvia_total", labels={"inicio_semana": "Inicio de semana", "lluvia_total": "Precipitación semanal (mm)"}, color_discrete_sequence=["#087F8C"])
            fig.update_layout(height=330, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, width="stretch")
        if province in ["PIURA", "SULLANA"]:
            st.info("El snapshot contiene valores climáticos idénticos para Piura y Sullana en sus semanas compartidas. La representatividad espacial está pendiente de revisión.")
    with records:
        st.dataframe(selected, hide_index=True, width="stretch")
        st.download_button("Descargar consulta en CSV", selected.to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"dengue_{province.lower()}_{start}_{end}_en_revision.csv", mime="text/csv")

st.divider()
left, right = st.columns(2)
with left:
    st.markdown("#### Fuentes para preparar tu viaje")
    st.markdown("[CDC Perú / MINSA: vigilancia de dengue](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue)\n\n"
                "[OPS: información oficial sobre dengue](https://www.paho.org/es/temas/dengue)\n\n"
                "[NASA POWER: datos meteorológicos](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)")
    st.caption("Son enlaces de consulta. Esta demo no descarga ni verifica avisos sanitarios vigentes.")
with right:
    st.markdown("#### Qué puedes hacer aquí")
    st.write("Consultar antecedentes semanales y conocer la cobertura de los datos antes de preparar un recorrido.")
    st.caption("Pendiente: itinerario de varias paradas, revisión de fuentes, pronóstico validado y pruebas con viajeros. Sudamérica es una ampliación futura.")
with st.expander("Calidad y procedencia del archivo"):
    st.write("Se conserva el dataset original sin corregir sus valores. La validación estructural no certifica la completitud epidemiológica.")
    st.write("Calendario provisional: semanas de domingo a sábado y primera semana que contiene el 4 de enero. Existe un registro de Sullana, semana 53 de 2009, separado en el reporte de revisión; no se incorpora ni reasigna automáticamente.")
    st.json(audit(data))
