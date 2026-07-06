import pandas as pd
import geopandas as gpd

def read_csv(csv_path, lat_col, lon_col, lasttime_col, cutoff):
    """Read CSV, filter by date, and clean coordinates."""
    df = pd.read_csv(csv_path)
    df[lasttime_col] = pd.to_datetime(df[lasttime_col], errors="coerce")
    df[lasttime_col] = df[lasttime_col].dt.tz_localize(None)
    df = df[df[lasttime_col] >= pd.to_datetime(cutoff)].copy()
    df[lat_col] = pd.to_numeric(df[lat_col], errors="coerce")
    df[lon_col] = pd.to_numeric(df[lon_col], errors="coerce")
    df = df.dropna(subset=[lat_col, lon_col])
    return df


def to_geodataframe(df, lat_col, lon_col, crs="EPSG:4326"):
    """Convert DataFrame to GeoDataFrame."""
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]), crs=crs)
    return gdf


def load_shapefile(path):
    """Load shapefile or GeoJSON."""
    return gpd.read_file(path)


def save_csv(df, path):
    """Save DataFrame to CSV."""
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"CSV salvo em: {path}")


def count_points_in_polygons(points_gdf, polygons_gdf, polygon_id_col):
    """
    Count how many points fall inside each polygon.

    Automatically reprojects polygons to match points CRS if needed.
    """
    if points_gdf.crs != polygons_gdf.crs:
        polygons_gdf = polygons_gdf.to_crs(points_gdf.crs)
        
    joined = gpd.sjoin(points_gdf, polygons_gdf, how="left", predicate="within")
    counts = joined.groupby(polygon_id_col).size().reset_index(name="points_count")
    result = polygons_gdf.merge(counts, on=polygon_id_col, how="left").fillna(0)
    return result
