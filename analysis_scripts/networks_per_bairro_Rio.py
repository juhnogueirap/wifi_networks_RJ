from utils.utils import (
    read_csv, 
    to_geodataframe, 
    load_shapefile, 
    save_csv, 
    count_points_in_polygons
)

WIFI_CSV = "wigle_data/wigle_results.csv"
LAT_COL = "trilat" 
LON_COL = "trilong"
LASTTIME_COL = "lasttime"


BAIRROS_SHP = "Bairros_Rio/Limite_de_Bairros.shp" 
AP_CODE_COL = "area_plane"     
BAIRRO_NAME_COL = "nome"       

CUTOFF_DATE = "2023-01-01"
OUTPUT_CSV = "results/networks_per_bairro_rio.csv"

AP_MAPPING = {
    "1": "AP1 - Centro",
    "2": "AP2 - Zona Sul",
    "3": "AP3 - Zona Norte",
    "4": "AP4 - Barra e Jacarepaguá",
    "5": "AP5 - Zona Oeste"
}

df = read_csv(WIFI_CSV, LAT_COL, LON_COL, LASTTIME_COL, CUTOFF_DATE)
gdf = to_geodataframe(df, LAT_COL, LON_COL)

gdf_bairros = load_shapefile(BAIRROS_SHP)

counts_gdf = count_points_in_polygons(gdf, gdf_bairros, BAIRRO_NAME_COL)
counts_gdf = counts_gdf.rename(columns={"points_count": "network_count"})

counts_gdf["nome_ap"] = counts_gdf[AP_CODE_COL].astype(str).map(AP_MAPPING)

colunas_finais = [AP_CODE_COL, "nome_ap", BAIRRO_NAME_COL, "network_count"]
save_csv(counts_gdf[colunas_finais], OUTPUT_CSV)