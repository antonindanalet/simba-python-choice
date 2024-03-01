from pathlib import Path

import pandas as pd

from simba.mobi.choice.utils.mobi import add_mobi_variables
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hh
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_zp


def get_data(
    input_directoy: Path, path_to_mtmc_data: Path, path_to_mobi_zones: Path
) -> pd.DataFrame:
    path_to_input = input_directoy / "input15_20_21.csv"
    """Loads the pre-generated datafile (to save time) or generates it directly from the raw MTMV data."""
    if path_to_input.exists() and path_to_input.is_file():
        df_zp = pd.read_csv(path_to_input)
    else:
        df_zp_2015 = get_data_per_year(2015, path_to_mtmc_data=path_to_mtmc_data)
        df_zp_2020 = get_data_per_year(2020, path_to_mtmc_data=path_to_mtmc_data)
        df_zp_2021 = get_data_per_year(2021, path_to_mtmc_data=path_to_mtmc_data)
        df_zp = pd.concat([df_zp_2015, df_zp_2020, df_zp_2021])
        # Rename variables
        df_zp = df_zp.rename(
            columns={
                "alter": "age",
                "f20400a": "driving_licence",
                "sprache": "language",
            }
        )

        df_zp["full_time"] = (df_zp.ERWERB == 1).astype(int)
        df_zp["part_time"] = (df_zp.ERWERB == 2).astype(int)

        df_zp["is_swiss"] = (df_zp.nation == 8100).astype(int)
        df_zp = df_zp.drop(columns=["ERWERB", "nation"])

        df_zp = add_mobi_variables(
            df_zp,
            path_to_mobi_zones=path_to_mobi_zones,
            mobi_variables=["accsib_mul", "accsib_pt", "pc_car"],
        )

        # Remove children
        df_zp = df_zp[df_zp.age > 17]

        df_zp.driving_licence.replace({2: 0}, inplace=True)  # 0: no, 1: yes
        df_zp = df_zp[df_zp.driving_licence >= 0]  # Removes 'no answer' / 'don't know

        df_zp.fillna(0, inplace=True)
        df_zp.to_csv(path_to_input, index=False)
    return df_zp


def get_data_per_year(year: int, path_to_mtmc_data: Path) -> pd.DataFrame:
    # Load row data of the Mobility and Transpot Microcensus (MTMC)
    df_zp = get_zp(
        year=year,
        path_to_mtmc_data=path_to_mtmc_data,
        selected_columns=["HHNR", "alter", "sprache", "ERWERB", "nation", "f20400a"],
    )
    df_hh = get_hh(
        year=year,
        path_to_mtmc_data=path_to_mtmc_data,
        selected_columns=["HHNR", "hhtyp", "W_X", "W_Y"],
    )
    df_zp = pd.merge(df_zp, df_hh, on="HHNR", how="left")
    df_zp["year"] = year
    return df_zp
