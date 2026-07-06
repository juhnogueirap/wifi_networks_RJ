from utils.utils import read_csv, to_geodataframe, load_shapefile, save_csv, count_points_in_polygons
import geopandas as gpd

WIFI_CSV = "wigle_data/wigle_results.csv"
LAT_COL = "trilat" 
LON_COL = "trilong"
LASTTIME_COL = "lasttime"

CITIES_SHP = "RJ_Municipios_2023/RJ_Municipios_2023.shp"
CITY_COL = "NM_MUN" 

CUTOFF_DATE = "2023-01-01"
OUTPUT_CSV = "results/networks_per_city.csv"

df = read_csv(WIFI_CSV, LAT_COL, LON_COL, LASTTIME_COL, CUTOFF_DATE)
gdf = to_geodataframe(df, LAT_COL, LON_COL)
gdf_cities = load_shapefile(CITIES_SHP)
counts_gdf = count_points_in_polygons(gdf, gdf_cities, CITY_COL)
counts_gdf = counts_gdf.rename(columns={"points_count": "network_count"})
counts_gdf = counts_gdf.sort_values("network_count", ascending=False)

save_csv(counts_gdf[[CITY_COL, "network_count"]], OUTPUT_CSV)

