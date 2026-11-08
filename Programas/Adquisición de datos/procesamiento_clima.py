import time
import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

carpeta = Path("clima_departamentos")                       # Crear la carpeta de exportación
carpeta.mkdir(parents=True, exist_ok=True)

def descargar_departamento(provincias):
  #provincias = {"Piura": (-5.19, -80.63), "Sullana": (-4.90, -80.69), "Talara": (-4.58, -81.27),
  #              "Paita": (-5.09, -81.11), "Sechura": (-5.56, -80.82), "Ayabaca": (-4.64, -79.71),
  #              "Huancabamba": (-5.24, -79.45), "Morropón": (-5.19, -79.97)}

  filas = []
  session = requests.Session()

  for provincia, (lat, lon) in provincias.items():
      params = {
          "latitude": lat,
          "longitude": lon,
          "start_date": "2000-01-01",
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

  return clima


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
    return [y, w]


def procesar_departamento(dep):
    df_coords = pd.read_csv("clima_departamentos/coordenadas.csv")  # Abrir el archivo de coordenadas por provincia de departamento
    df_select = df_coords[df_coords["ccdd"] == dep]  # Seleccionar un departamento

    provincias = dict(zip(  # Crear un diccionario que contenga las coordenadas de sus provincias
        df_select["nombprov"],
        zip(df_select["latitud"], df_select["longitud"])))

    clima = descargar_departamento(provincias)  # Descargar datos meteorológicos de cada punto

    provincias = df_select["nombprov"].unique()

    clima[["year", "week"]] = pd.DataFrame(  # Calcular año y semana una sola vez
        clima["time"].apply(semana_epidemiologica).tolist(),
        index=clima.index)

    indices = pd.MultiIndex.from_product(  # Preparar índice temporal
        [range(2000, 2026), range(1, 54)],
        names=["year", "week"])

    departamento = pd.DataFrame({  # Crear un dataset de departamento
        "year": [], "week": [], "temperature_2m_mean": [],
        "precipitation_sum": [], "relative_humidity_2m_mean": [], "provincia": []})

    for provincia in provincias:
        df = clima[clima["provincia"] == provincia]

        temporal = pd.DataFrame(  # Crear dataset temporal
            0.0,
            index=indices,
            columns=["temperature_2m_mean", "precipitation_sum",
                     "relative_humidity_2m_mean", "provincia"])

        semanal = df.groupby(["year", "week"]).agg({  # Agrupar datos por semana
            "temperature_2m_mean": lambda x: x.sum() / 7,
            "precipitation_sum": "sum",
            "relative_humidity_2m_mean": lambda x: x.sum() / 7})

        temporal.update(semanal)  # Incorporar valores al dataset vacío
        temporal["provincia"] = provincia
        temporal = temporal.reset_index()

        nombre = f"clima_{provincia.lower()}.csv"
        departamento = pd.concat([departamento, temporal])

    departamento.to_csv("clima_departamentos/clima_" + dep.lower() + ".csv", index=False)


df_coords = pd.read_csv("clima_departamentos/coordenadas.csv")            # Abrir el archivo de coordenadas por provincia de departamento
departamentos = df_coords["ccdd"].unique()
for element in departamentos:
  procesar_departamento(element)
  print("Procesado: "+element)
