"""Pantalla de consulta histórica de malaria por departamento, provincia y año."""
import pandas as pd
import plotly.express as px
import streamlit as st
from src.data.malaria import PERIODS, DEFINITIONS, audit_department, catalog, display_name, load_department, select_year


@st.cache_data
def department_snapshot(department, version):
    return load_department(department)


def render_malaria():
    st.caption("HACKATON FACI  /  GUÍA DEL VIAJERO EN PERÚ")
    st.title("Explora el historial de malaria")
    st.markdown("Consulta registros semanales por **departamento, provincia y año**.")
    st.info("Información histórica del archivo del equipo. No describe el riesgo actual de un viaje.")
    try:
        files = catalog()
    except (OSError, ValueError) as exc:
        st.error(f"No se puede abrir el catálogo de malaria: {exc}")
        return
    with st.sidebar:
        st.header("Tu consulta de malaria")
        departments = list(files)
        department = st.selectbox("Departamento", departments, index=departments.index("LORETO") if "LORETO" in departments else 0,
                                  format_func=display_name, key="malaria_department")
    try:
        data = department_snapshot(department, files[department].stat().st_mtime_ns)
    except (OSError, ValueError) as exc:
        st.error(f"No se puede abrir el archivo de malaria: {exc}")
        return
    with st.sidebar:
        period = st.selectbox("Periodo de la fuente", list(PERIODS), index=1, key="malaria_period")
        in_period = data.loc[data.periodo_fuente.eq(period)]
        provinces = sorted(in_period.provincia.unique())
        if not provinces:
            st.info("Este departamento no tiene registros para el periodo elegido.")
            return
        # A scoped key prevents a province from a different department/period persisting.
        province = st.selectbox("Provincia", provinces, format_func=display_name,
                                key=f"malaria_province_{department}_{period}")
        lo, hi = PERIODS[period]
        year = st.selectbox("Año", list(range(lo, hi + 1)), index=(2024 if hi == 2025 else hi) - lo,
                           key=f"malaria_year_{period}")
        st.caption(f"{len(departments)} departamentos con archivos disponibles. Escala provincial · Frecuencia semanal.")
    selected = select_year(data, province, period, year)
    st.subheader(f"{display_name(province)} · {display_name(department)}")
    st.caption(f"Fuente {period}: {DEFINITIONS[period]}. Los periodos se consultan por separado para conservar su definición.")
    years = in_period.loc[in_period.provincia.eq(province), "ano"]
    st.caption(f"Años presentes para esta provincia: {int(years.min())}–{int(years.max())}. Archivo: {files[department].name}")
    if selected.empty:
        st.info("No hay datos de esta provincia para el año seleccionado. La ausencia no se interpreta como cero casos.")
    else:
        left, middle, right = st.columns(3)
        left.metric("Total del archivo en el año", f"{int(selected.malaria_total.sum()):,}".replace(",", "."))
        middle.metric("Semanas registradas", len(selected))
        right.metric("Semanas con valor positivo", int(selected.malaria_total.gt(0).sum()))
        st.caption("Se conserva malaria_total del procesamiento histórico. El archivo no permite separar especies ni tipos de diagnóstico. Sus ceros pueden proceder de rellenos anteriores.")
        if selected.calendario_revision.any():
            st.warning("La selección contiene etiquetas semanales que requieren revisión del calendario. Sus valores se conservan en el gráfico, el total y la descarga.")
        if selected.nombre_con_caracter_danado.any():
            st.caption("El nombre se presenta con una corrección de lectura; el CSV descargado conserva el texto original del archivo.")
        history, records = st.tabs(["Registros por semana", "Datos de la consulta"])
        with history:
            chart = selected.assign(estado=selected.calendario_revision.map({False: "Etiqueta del archivo", True: "Calendario por revisar"}))
            fig = px.bar(chart, x="semana", y="malaria_total", color="estado",
                         color_discrete_map={"Etiqueta del archivo": "#087F8C", "Calendario por revisar": "#D17A22"},
                         labels={"semana": "Semana indicada por la fuente", "malaria_total": "Valor del archivo", "estado": ""},
                         hover_data=["etiqueta_semana"])
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0), legend=dict(orientation="h"))
            fig.update_xaxes(dtick=4)
            st.plotly_chart(fig, width="stretch")
            st.caption("Las etiquetas de semana se muestran tal como aparecen en el archivo; no se transforman en fechas diarias ni se rellenan semanas ausentes.")
        with records:
            st.dataframe(selected, hide_index=True, width="stretch")
            st.download_button("Descargar consulta de malaria", selected.to_csv(index=False).encode("utf-8-sig"),
                               file_name=f"malaria_{department.lower().replace(' ', '_')}_{year}.csv", mime="text/csv")
    st.divider()
    st.markdown("#### Fuentes de consulta")
    st.markdown("[CDC Perú / MINSA: vigilancia epidemiológica de malaria](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-malaria)")
    st.caption("El catálogo oficial identifica recursos para 2000–2008 y 2009–2025. Esta consulta utiliza los archivos derivados conservados en el repositorio, sin actualización automática.")
    with st.expander("Procedencia y calidad del archivo"):
        st.write("Se conservan los valores y las etiquetas originales, incluidas semanas 53. La comparación con el calendario provisional solo marca registros para revisión; no certifica su invalidez frente a MINSA.")
        st.write("La consulta usa los CSV históricos derivados del equipo. Las columnas originales ya agregadas no permiten recuperar especies ni distinguir confirmados, probables o sospechosos.")
        st.json(audit_department(department))
