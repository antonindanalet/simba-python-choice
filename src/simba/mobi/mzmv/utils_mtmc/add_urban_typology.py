"""Utils package dealing with data of the Mobility and Transport Microcensus (MTMC)."""
from pathlib import Path

import pandas as pd


def add_urban_typology(
    df: pd.DataFrame, year: int, field_bfs: str = "W_BFS"
) -> pd.DataFrame:
    """Add an urban typology from the Federal Statistical Office (FSO) to the dataframe.
    This typology is called "Stadt/Land-Typologie" in German.
    More info: https://www.bfs.admin.ch/asset/de/2544676
    The typology defines three levels (urban, rural and "intermediate").
    Can be used e.g. with df_zp (with variable "W_BFS" or "A_BFS") or df_hh (with variable "W_BFS" for 2015)."""
    if (year != 2015) & (year != 2020) & (year != 2021):
        raise ValueError("Spatial typology is only available for 2015, 2020 and 2021!")
    path_to_typology = Path(r"path_to_typology")
    path_to_typology = path_to_typology / str(year) / "name_of_typology_file.xlsx"
    urban_rural_typology = pd.read_excel(
        path_to_typology,
        sheet_name="Daten",
        skiprows=[
            0,
            2,
        ],  # Removes the 1st row, with information, and the 3rd, with links
        usecols="A,G",  # Selects only the BFS commune number and the column with the typology
    )

    urban_rural_typology = urban_rural_typology.rename(
        columns={"Städtische / Ländliche Gebiete": "urban_typology"}
    )
    df = pd.merge(
        df,
        urban_rural_typology,
        how="left",
        left_on=field_bfs,
        right_on="BFS Gde-nummer",
    )
    df.drop("BFS Gde-nummer", axis=1, inplace=True)
    return df
