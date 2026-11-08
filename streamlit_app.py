"""Guía del viajero: consulta histórica de dengue y malaria en Perú."""
import streamlit as st
from app.dengue import render_dengue
from app.malaria import render_malaria

st.set_page_config(page_title="Guía del viajero · Perú", page_icon="🧭", layout="wide")
disease = st.sidebar.radio("Información sanitaria", ["Dengue", "Malaria"], key="disease")
if disease == "Malaria":
    render_malaria()
else:
    render_dengue()
