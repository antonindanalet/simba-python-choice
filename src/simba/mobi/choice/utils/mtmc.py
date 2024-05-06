"""Utils package dealing with data of the Mobility and Transport Microcensus (MTMC)."""
from pathlib import Path

import pandas as pd


def add_urban_typology(df: pd.DataFrame) -> pd.DataFrame:
    """Add an urban typology from the Federal Statistical Office (FSO) to the dataframe.
    This typology is called "Stadt/Land-Typologie" in German.
    More info: https://www.bfs.admin.ch/asset/de/2544676
    The typology defines three levels (urban, rural and "intermediate")."""
    input_directory = Path(
        r"../../Zones/Raumgliederungen.xlsx"
    )
    urban_rural_typology = pd.read_excel(
        input_directory,
        sheet_name="Daten",
        skiprows=[0, 2],
    )
    urban_rural_typology = urban_rural_typology.drop(
        [
            "Gemeindename",
            "Kantons-nummer",
            "Kanton",
            "Bezirks-nummer",
            "Bezirksname",
            "Gemeindetypologie 2012 (9 Typen)",
            "Gemeindetypologie 2012 (25 Typen)",
        ],
        axis=1,
    )
    urban_rural_typology = urban_rural_typology.rename(
        columns={"Städtische / Ländliche Gebiete": "W_stadt_land_2012"}
    )
    df = df.merge(
        urban_rural_typology, how="left", left_on="W_BFS", right_on="BFS Gde-nummer"
    )
    return df
