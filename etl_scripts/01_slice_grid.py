import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt

# This script is used to slice the state of Rio de Janeiro into quadrants.
# This will be useful for querying results in small areas that reside only inside the state of Rio de Janeiro.

rio_gdf = (gpd.read_file("RJ_Municipios_2023/RJ_Municipios_2023.shp")).to_crs(epsg=4326) 
rio_shape = rio_gdf.union_all() 
minx, miny, maxx, maxy = rio_shape.bounds
grid_size = 0.05 #quadrants size

quadrants = []
x = minx
while x < maxx:
    y = miny
    while y < maxy:
        quad = box(x, y, x + grid_size, y + grid_size)
        if quad.intersects(rio_shape):
            quadrants.append(quad)
        y += grid_size
    x += grid_size

gdf_quadrants = gpd.GeoDataFrame(geometry=quadrants, crs="EPSG:4326")
df_quadrants = gdf_quadrants.geometry.bounds #extracts limits (minx, miny, maxx, maxy)
df_quadrants = df_quadrants.rename(columns={
    "miny": "latrange1",
    "maxy": "latrange2",
    "minx": "longrange1",
    "maxx": "longrange2"
})
df_quadrants.to_csv("etl_scripts/quadrants_rj.csv", index=False)


fig1, ax1 = plt.subplots(figsize=(10, 10))

gpd.GeoSeries([rio_shape], crs="EPSG:4326").plot(
    ax=ax1, 
    facecolor="none", 
    edgecolor="black", 
    linewidth=0.8
)

gpd.GeoSeries([rio_shape.envelope], crs="EPSG:4326").plot(
    ax=ax1, 
    facecolor="none",  # Preenchimento transparente
    edgecolor="red",   # Linha que delimita vermelha
    linewidth=2
)

plt.title("Polígono sobre o estado do Rio de Janeiro")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig(
    "results/rj_poligono_sobre_estado.png", 
    dpi=300, 
    bbox_inches="tight"
)
plt.close(fig1)


fig2, ax2 = plt.subplots(figsize=(10, 10))
rio_gdf.plot(ax=ax2, facecolor="none", edgecolor="black")

gpd.GeoDataFrame(geometry=quadrants, crs="EPSG:4326").plot(
    ax=ax2, 
    facecolor="none", 
    edgecolor="red"
)

plt.title("Quadrantes sobre o RJ")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig(
    "results/rj_em_quadrantes.png", 
    dpi=300, 
    bbox_inches="tight"
)
plt.close(fig2)