import time
import requests
import pandas as pd
from datetime import date, timedelta

provincias = {"Piura": (-5.19, -80.63), "Sullana": (-4.90, -80.69), "Talara": (-4.58, -81.27),
              "Paita": (-5.09, -81.11), "Sechura": (-5.56, -80.82), "Ayabaca": (-4.64, -79.71),
              "Huancabamba": (-5.24, -79.45), "Morropón": (-5.19, -79.97)}

filas = []
session = requests.Session()

for provincia, (lat, lon) in provincias.items():
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2001-01-01",
        "end_date": "2025-12-31",
        "daily": "temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean",
        "timezone": "America/Lima"}

    for intento in range(4):
        r = session.get(
            "https://archive-api.open-meteo.com/v1/archive",
            params=params,
            timeout=60)

        if r.status_code == 429:
            espera = int(r.headers.get("Retry-After", 30 * (intento + 1)))
            print(f"Límite alcanzado. Esperando {espera} segundos...")
            time.sleep(espera)
            continue

        r.raise_for_status()
        df_clima = pd.DataFrame(r.json()["daily"])
        df_clima["provincia"] = provincia
        filas.append(df_clima)
        print(f"Descargado: {provincia}")
        break
    else:
        print(f"No se pudo descargar: {provincia}")
        continue

    time.sleep(5)

if filas:
    clima = pd.concat(filas, ignore_index=True)


# ['Piura', 'Sullana', 'Talara', 'Paita', 'Sechura', 'Ayabaca', 'Huancabamba', 'Morropón']
def inicio_semana_1(y):
    cuatro_enero = date(y, 1, 4)                                            # La primera semana tiene al menos 4 días del año actual
    return cuatro_enero - timedelta(days=(cuatro_enero.weekday() + 1) % 7)  # Restarle días transcurridos desde el domingo de la semana

def semana_epidemiologica(fecha_texto):
    fecha = date.fromisoformat(fecha_texto)           # Descomponer la fecha
    y = fecha.year
    if fecha < inicio_semana_1(y):                    # Si el día va antes del 4 de enero, éste corresponde al año pasado
        y -= 1
    elif fecha >= inicio_semana_1(y + 1):             # A ver si pertenece a la semana del año siguiente
        y += 1
    w = (fecha - inicio_semana_1(y)).days // 7 + 1    # Semanas transcurridos desde el primer día asignado
    return [y, w - 1]


provincias = ['Piura', 'Sullana', 'Talara', 'Paita', 'Sechura', 'Ayabaca', 'Huancabamba', 'Morropón']

for provincia in provincias:  # Recorrer todas las provincias de Piura
  df_seleccionado = clima[clima["provincia"] == provincia]
  year, week, empty = [], [], []

  for y in range(2001, 2026): # Crear casillas vacías dónde rellenar los datos obtenidos
    for w in range(1, 54):    # Siempre 53 semanas, aunque el último a veces esté vacío
      year.append(y)          # Cada casilla tiene un año
      week.append(w)          # y su respectiva semana
      empty.append(0.0)       # Para crear columnas a las que añadir números

  # Crear un dataset vacío, solo con año y semana como "keys"
  temporal = pd.DataFrame({"year": year, "week": week, "temperature_2m_mean": empty,
                          "precipitation_sum": empty, "relative_humidity_2m_mean": empty})

  for i in range(len(df_seleccionado)):
    y, w = semana_epidemiologica(df_seleccionado["time"].iloc[i]) # De la fecha obtener semana epidemiológica
    val = [df_seleccionado["temperature_2m_mean"].iloc[i],        # Valores relevantes
          df_seleccionado["precipitation_sum"].iloc[i],
          df_seleccionado["relative_humidity_2m_mean"].iloc[i]]
    temporal.loc[(temporal["year"] == y) & (temporal["week"] == w), "temperature_2m_mean"] += (val[0] / 7)        # Promediar la suma
    temporal.loc[(temporal["year"] == y) & (temporal["week"] == w), "precipitation_sum"] += val[1]                # Solo sumar
    temporal.loc[(temporal["year"] == y) & (temporal["week"] == w), "relative_humidity_2m_mean"] += (val[2] / 7)  # Promediar la suma

  name = "clima_"+provincia.lower()+".csv"
  temporal.to_csv(name, index=False)
  print(name + " Procesado.")
