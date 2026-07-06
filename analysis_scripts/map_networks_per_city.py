import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as mticker
import matplotlib.patheffects as path_effects  # <-- Adicionado para dar leitura ao texto preto
from matplotlib_scalebar.scalebar import ScaleBar

from utils.utils import (
    read_csv, 
    to_geodataframe, 
    load_shapefile, 
    count_points_in_polygons
)

WIFI_CSV = "wigle_data/wigle_results.csv"
LAT_COL = "trilat"
LON_COL = "trilong"
LASTTIME_COL = "lasttime"
CITIES_SHP = "RJ_Municipios_2023/RJ_Municipios_2023.shp"
CITY_NAME_COL = "NM_MUN"
CUTOFF_DATE = "2023-01-01"


df = read_csv(
    WIFI_CSV, 
    LAT_COL, 
    LON_COL,
    LASTTIME_COL, 
    CUTOFF_DATE
)

map_data = count_points_in_polygons(
    to_geodataframe(df, LAT_COL, LON_COL), 
    load_shapefile(CITIES_SHP), 
    CITY_NAME_COL
)


map_data['centroid_x'] = map_data['geometry'].centroid.x
map_data = map_data.sort_values(by='centroid_x').reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 10))

map_data.plot(
    column="points_count",
    cmap="YlOrRd",  
    norm=colors.LogNorm(
        vmin=max(map_data["points_count"].replace(0, 1).min(), 1),
        vmax=map_data["points_count"].max()
    ),
    legend=True,
    edgecolor="black",
    linewidth=0.3,
    legend_kwds={
        "shrink": 0.7  
    },
    ax=ax
)

for idx, row in map_data.iterrows():
    municipio_id = idx + 1
    nome_municipio = row[CITY_NAME_COL]
    print(f"{municipio_id}: {nome_municipio}")  
    centroide = row['geometry'].centroid
    txt = ax.text(
        centroide.x, 
        centroide.y, 
        str(municipio_id), 
        fontsize=6, 
        ha='center', 
        va='center', 
        color='black',       
        weight='bold'
    )
    txt.set_path_effects([
        path_effects.withStroke(linewidth=1.5, foreground='white')
    ])
print("----------------------------------------------------------")

escala = ScaleBar(
    dx=111000,              
    units="m", 
    dimension="si-length", 
    location="lower right", 
    frameon=False
)
ax.add_artist(escala)


ax.set_title("Redes Wi-Fi por Município do RJ", fontsize=14)
ax.axis("off")

cbar = ax.get_figure().get_axes()[-1]
cbar.set_ylabel("Contagem de redes (escala logarítmica)", rotation=90)
cbar.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{int(y):,}".replace(",", ".")))

plt.savefig("results/wifi_por_municipio.png", dpi=300, bbox_inches="tight")
print("Feito.")