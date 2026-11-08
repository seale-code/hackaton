import geopandas as gpd
from pathlib import Path


carpeta = Path("clima_departamentos")                       # Crear la carpeta de exportación
carpeta.mkdir(parents=True, exist_ok=True)

gdf = gpd.read_file("limites_provincia.json")

# Proyectar a coordenadas métricas
gdf = gdf.to_crs("EPSG:6933")

# Obtener un punto dentro de cada provincia
puntos = gdf.geometry.representative_point()

# Regresar a coordenadas geográficas
puntos = gpd.GeoSeries(puntos, crs="EPSG:6933").to_crs("EPSG:4326")

gdf["latitud"] = puntos.y
gdf["longitud"] = puntos.x

departamentos = ['AMAZONAS', 'ANCASH', 'APURIMAC', 'AREQUIPA', 'AYACUCHO',
                 'CAJAMARCA', 'CALLAO', 'CUSCO', 'HUANCAVELICA', 'HUANUCO',
                 'ICA', 'JUNIN', 'LA LIBERTAD', 'LAMBAYEQUE', 'LIMA',
                 'LORETO', 'MADRE DE DIOS', 'MOQUEGUA', 'PASCO', 'PIURA',
                 'PUNO', 'SAN MARTIN', 'TACNA', 'TUMBES', 'UCAYALI']


# Crear correspondencia: 01 = Amazonas, 02 = Ancash...
codigos = {f"{i+1:02d}": nombre for i, nombre in enumerate(departamentos)}

# Reemplazar CCDD
gdf["ccdd"] = gdf["ccdd"].astype(str).str.zfill(2).map(codigos)

# Guardar dataset de coordenadas
gdf[["ccdd", "nombprov", "latitud", "longitud"]].to_csv("clima_departamentos/coordenadas.csv", index=False)

# Límites de provincias obtenido en: https://geoespacial.inei.gob.pe/geoserver/Interoperabilidad/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Interoperabilidad%3Aig_provincia&maxFeatures=196&outputFormat=application%2Fjson
