import pandas as pd
import requests
from io import BytesIO

# Descargar y abrir el dataset
respuesta = requests.get(
    "https://www.datosabiertos.gob.pe/node/23482/download",
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30)
respuesta.raise_for_status()
df = pd.read_csv(BytesIO(respuesta.content))

# Seleccionar variables relevantes
relevante = ["provincia", "distrito", "ano", "semana", "diagnostic", "tipo_dx"]

# Seleccionar únicamente Piura
df_piura = df[relevante].copy()[df["departamento"] == "PIURA"]

distritos = ['PIURA', 'SULLANA', 'TALARA', 'AYABACA', 'MORROPON', 'HUANCABAMBA', 'SECHURA', 'PAITA']

def procesar_distrito(provincia):
    provincia_sele = df_piura[df_piura["provincia"] == provincia]   # Seleccionar el distrito
    provincia_sele.sort_values(by="ano", ascending = True)          # Ordenar año en orden ascendente
    start_year = provincia_sele["ano"].unique()[0]                  # Obtener el primer año
    end_year = provincia_sele["ano"].unique()[-1]                   # Obtener el último año

    ano, semana, empty = [], [], []                                 # Crear variables de año, semana y uno vacío
    for y in range(start_year, end_year + 1):                       # Recorrer cada año
      for w in range(1, 54):                                        # Recorrer cada semana del año
        ano.append(y)                                               # Añadir año, semana y casilla vacía
        semana.append(w)
        empty.append(0)

    # Montarse un dataset vacío con estas variables creadas
    # A97.0: Dengue sin signos
    # A97.1: Dengue con signos de alarma
    # A97.2: Dengue grave
    # P: Caso probable
    # C: Caso confirmado
    temporal = pd.DataFrame({"ano": ano, "semana": semana, "A97.0P": empty, "A97.1P": empty,
                             "A97.2P": empty, "A97.0C": empty, "A97.1C": empty, "A97.2C": empty,})

    for i in range(len(provincia_sele)):                                       # Recorrer el distrito seleccionado
      temporal.loc[(temporal["ano"] == provincia_sele.iloc[i]["ano"]) &        # Apuntar por año y semana
                   (temporal["semana"] == provincia_sele.iloc[i]["semana"]),   # Aumentar caso correspondiente
                   provincia_sele.iloc[i]["diagnostic"] + provincia_sele.iloc[i]["tipo_dx"]] += 1

    name = "PIURA_" + provincia + ".csv"                         # Darle el nombre adecuado
    temporal.to_csv(name, index=False)                           # Guardar el archivo

for i in range(0, len(distritos)):                               # Procesar todos los distritos
    procesar_distrito(distritos[i])
    print(str(i) + " - Procesado el distrito " + distritos[i])
