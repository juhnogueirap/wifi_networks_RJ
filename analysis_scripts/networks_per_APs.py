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

APS_SHP = "Cidade_RJ_APs/Limite_Áreas_de_Planejamento_(AP).shp"
AP_CODE_COL = "codap" 
 
CUTOFF_DATE = "2023-01-01"
OUTPUT_CSV = "results/networks_per_AP.csv"

AP_MAPPING = {
    "1": "AP1 - Centro",
    "2": "AP2 - Zona Sul",
    "3": "AP3 - Zona Norte",
    "4": "AP4 - Barra e Jacarepaguá",
    "5": "AP5 - Zona Oeste"
}

df = read_csv(WIFI_CSV, LAT_COL, LON_COL, LASTTIME_COL, CUTOFF_DATE)

gdf = to_geodataframe(df, LAT_COL, LON_COL)

gdf_aps = load_shapefile(APS_SHP)

counts_gdf = count_points_in_polygons(gdf, gdf_aps, AP_CODE_COL)
counts_gdf = counts_gdf.rename(columns={"points_count": "network_count"})
counts_gdf["nome_ap"] = counts_gdf[AP_CODE_COL].map(AP_MAPPING)

save_csv(counts_gdf[[AP_CODE_COL, "network_count", "nome_ap"]], OUTPUT_CSV)
