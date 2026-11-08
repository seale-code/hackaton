import requests
import pandas as pd
from io import BytesIO
from pathlib import Path

carpeta = Path("vigilancia_malaria")                       # Crear la carpeta de exportación
carpeta.mkdir(parents=True, exist_ok=True)

# URLs de los datasets
links = [
    "https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_malaria_2000_2008.csv",
    "https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_malaria_2009_2025.csv"]


# Descargar datasets
def get_dataset(link):
    respuesta = requests.get(
        link,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30)
    respuesta.raise_for_status()
    return pd.read_csv(BytesIO(respuesta.content), low_memory=False)


df_1, df_2 = [get_dataset(link) for link in links]


# Función para generar calendario completo
def crear_calendario(df, inicio, fin, columnas, modo, departamento):
    df = df.loc[df["departamento"].eq(departamento)].copy()             # Filtrar departamento
    provincias = df["provincia"].dropna().unique()                      # Seleccionar provincias

    if modo == "suma":                                                  # Agrupar los casos de malaria por falciparum y vivax
        casos = (
            df.assign(malaria_total=df["falciparum"] + df["vivax"])
            .groupby(columnas)["malaria_total"]
            .sum())

    elif modo == "conteo":                                              # Contar casos
        casos = df.groupby(columnas).size().rename("malaria_total")

    calendario = pd.MultiIndex.from_product(                            # Crear un calendario que siempre tenga 53 semanas
        [
            range(inicio, fin + 1),
            range(1, 54),
            provincias],
        names=columnas)

    resultado = (                                                       # Completar semanas sin registros con cero
        casos.reindex(calendario, fill_value=0)
        .reset_index())

    return resultado                                                    # Retornar el dataset procesado


def procesar_departamento(departamentos):
    for departamento in departamentos:
        columnas = ["ano", "semana", "provincia"]                       # Procesar ambos periodos
        parte1 = crear_calendario(
            df_1, 2000, 2008, columnas, "suma", departamento)
        parte2 = crear_calendario(
            df_2, 2009, 2025, columnas, "conteo", departamento)

        resultado = pd.concat(                                          # Unir los datasets
            [parte1, parte2],
            ignore_index=True)

        resultado = resultado.sort_values(                              # Ordenar
            ["ano", "semana", "provincia"]).reset_index(drop=True)

        resultado.to_csv(                                               # Exportar
            "vigilancia_malaria/malaria_2000-2025_"+departamento.lower()+".csv",
            index=False)

        total_casos = resultado["malaria_total"].sum()
        print("Casos totales de malaria 2000-2025 en "+departamento+": "+str(total_casos))


departamentos = df_2["departamento"].unique()
print(departamentos)
procesar_departamento(departamentos)
