from pathlib import Path
from typing import List

import geopandas
import pandas as pd


def add_mobi_variables(
    df: pd.DataFrame, path_to_mobi_zones: Path, mobi_variables: List[str]
) -> pd.DataFrame:
    # Add MOBi variables
    df = geopandas.GeoDataFrame(
        df, geometry=geopandas.points_from_xy(df.W_X, df.W_Y), crs="epsg:4326"
    )
    df.to_crs(epsg=21781, inplace=True)
    # Read the shape file with MOBi variables
    df_mobi = geopandas.read_file(path_to_mobi_zones, ignore_fields="area_land")
    df_mobi.to_crs(epsg=21781, inplace=True)  # Define the projection (CH1903_LV03)
    list_of_variables = mobi_variables + ["geometry"]
    df = geopandas.sjoin(
        df, df_mobi[list_of_variables], how="left", predicate="intersects"
    )
    # From geodataframe to dataframe
    df = pd.DataFrame(df.drop(columns=["geometry", "W_X", "W_Y", "index_right"]))
    return df
