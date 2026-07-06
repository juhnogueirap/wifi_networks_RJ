from utils.utils import read_csv, to_geodataframe, load_shapefile
import geopandas as gpd
import pandas as pd

WIFI_CSV = "wigle_data/wigle_results.csv"
LAT_COL = "trilat" 
LON_COL = "trilong"
LASTTIME_COL = "lasttime"

CITIES_SHP = "RJ_Municipios_2023/RJ_Municipios_2023.shp"
CITY_COL = "NM_MUN" 

CUTOFF_DATE = "2023-01-01"
OUTPUT_CSV = "results/networks_per_city_per_features.csv"


df = read_csv(WIFI_CSV, LAT_COL, LON_COL, LASTTIME_COL, CUTOFF_DATE)
gdf = to_geodataframe(df, LAT_COL, LON_COL)
gdf_cities = load_shapefile(CITIES_SHP)

if gdf.crs != gdf_cities.crs:
    gdf = gdf.to_crs(gdf_cities.crs)


gdf_joined = gpd.sjoin(gdf, gdf_cities, how="inner", predicate="within")

#Looks for specific encryption, frequency, infra, security protocol
gdf_joined['encryption'] = gdf_joined['encryption'].fillna('').astype(str).str.lower()
gdf_joined['frequency'] = pd.to_numeric(gdf_joined['frequency'], errors='coerce')

gdf_joined['infra_count'] = (gdf_joined['type'] == 'infra').astype(int)
gdf_joined['adhoc_count'] = (gdf_joined['type'] == 'adhoc').astype(int)

gdf_joined['wpa2_count'] = gdf_joined['encryption'].str.contains(r'wpa2|wpa3', regex=True).astype(int)
gdf_joined['wpa_count'] = gdf_joined['encryption'].str.contains(r'wpa(?![23])', regex=True).astype(int)
gdf_joined['wep_count'] = gdf_joined['encryption'].str.contains('wep').astype(int)
gdf_joined['open_count'] = (
    (gdf_joined['encryption'] == '') | 
    (gdf_joined['encryption'].str.contains(r'^\[ess\]$|^\[ibss\]$', regex=True))
).astype(int)


gdf_joined['freq_24ghz_count'] = ((gdf_joined['frequency'] >= 2400) & (gdf_joined['frequency'] < 2500)).astype(int)
gdf_joined['freq_5ghz_count'] = ((gdf_joined['frequency'] >= 4900) & (gdf_joined['frequency'] < 6000)).astype(int)
gdf_joined['freq_6ghz_count'] = ((gdf_joined['frequency'] >= 5925) & (gdf_joined['frequency'] <= 7125)).astype(int)

results = gdf_joined.groupby(CITY_COL).agg(
    network_count=('type', 'size'),          
    infra_count=('infra_count', 'sum'),      
    adhoc_count=('adhoc_count', 'sum'),      
    wep_count=('wep_count', 'sum'),          
    wpa_count=('wpa_count', 'sum'),          
    wpa2_count=('wpa2_count', 'sum'),        
    open_count=('open_count', 'sum'),        
    freq_24ghz_count=('freq_24ghz_count', 'sum'), 
    freq_5ghz_count=('freq_5ghz_count', 'sum'),   
    freq_6ghz_count=('freq_6ghz_count', 'sum')   

).reset_index()

results = results.sort_values("network_count", ascending=False)

results.to_csv(OUTPUT_CSV, index=False)
print(f"Análise finalizada! Frequências incluídas com sucesso em: {OUTPUT_CSV}")