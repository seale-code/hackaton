import requests
import pandas as pd
from io import BytesIO
from pathlib import Path

# Descargar el dataset
respuesta = requests.get(
    "https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_zoonosis_2000_2025_0.csv",
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=60)
respuesta.raise_for_status()
df = pd.read_csv(BytesIO(respuesta.content), low_memory=False)

relevante = ["departamento", "provincia", "ano", "semana", "diagnostic", "tipo_dx"]
CODIGOS = ["A27", "X20", "X21"]
df = df[relevante].copy()                                   # Seleccioanr columnas relevantes

df["ano"] = pd.to_numeric(df["ano"], errors="coerce")       # Preparar variables de tiempo
df["semana"] = pd.to_numeric(df["semana"], errors="coerce")

df = df.dropna(subset=["departamento", "provincia", "ano", "semana"])

df["ano"] = df["ano"].astype(int)
df["semana"] = df["semana"].astype(int)

carpeta = Path("vigilancia_zoonosis")                       # Crear la carpeta de exportación
carpeta.mkdir(parents=True, exist_ok=True)


def procesar_distrito(provincia, df_selec):

    datos = df_selec.loc[df_selec["provincia"].eq(provincia)].copy()

    if datos.empty:
        return pd.DataFrame(columns=["ano", "semana", "provincia"] + CODIGOS)

    calendario = pd.MultiIndex.from_product([       # Generar el calendario
            range(datos["ano"].min(), datos["ano"].max() + 1),
            range(1, 54)],
        names=["ano", "semana"])

    casos = datos.loc[                                      # Seleccionar diagnósticos de interés
        datos["diagnostic"].isin(CODIGOS)
        & datos["semana"].between(1, 53)]

    conteo = (                                              # Conteo por año, semana y diagnóstico
        casos.groupby(["ano", "semana", "diagnostic"])
        .size()
        .unstack("diagnostic"))

    resultado = (                                           # Completar semanas y diagnósticos sin registros
        conteo.reindex(index=calendario, columns=CODIGOS, fill_value=0)
        .fillna(0).astype(int).reset_index())

    resultado.insert(2, "provincia", provincia)             # Agregar provincia

    return resultado


def procesar_departamento(departamento):
    df_dep = df.loc[df["departamento"].eq(departamento)].copy()
    provincias = sorted(df_dep["provincia"].dropna().unique())


    resultados = [                                          # Procesar todas las provincias
        procesar_distrito(provincia, df_dep)
        for provincia in provincias]

    resultado = pd.concat(resultados, ignore_index=True)    # Unir resultados

    resultado = resultado.sort_values(                      # Ordenar por tiempo y alfabéticamente
        ["ano", "semana", "provincia"]).reset_index(drop=True)

    total_casos = int(resultado[CODIGOS].to_numpy().sum())  # Calcular total de casos

    archivo = carpeta / (f"zoonosis_2000-2025_{departamento.lower()}.csv")

    resultado.to_csv(archivo, index=False)

    return total_casos


departamentos = sorted(df["departamento"].dropna().unique())    # Procesar todos los departamentos

totales = {}

for departamento in departamentos:
    total = procesar_departamento(departamento)
    totales[departamento] = total

print("\nRESUMEN GENERAL DE ZOONOSIS 2000-2025\n")              # Dar un resumen general
for departamento, total in totales.items():
    print(f"{departamento:<20} {total:>12,}")
print("-" * 35)
print(
    f"{'TOTAL GENERAL':<20} "
    f"{sum(totales.values()):>12,}"
)
print("\nArchivos exportados en:", carpeta.resolve())
