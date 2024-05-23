import os
from pathlib import Path

import pandas as pd

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.data_loader import (
    get_data_per_year,
)
from simba.mobi.choice.utils.mobi import add_mobi_variables


def get_data(
    path_to_input: Path, path_to_mtmc_data: Path, path_to_mobi_zones: Path
) -> pd.DataFrame:
    if os.path.isdir(path_to_input) is False:
        path_to_input.mkdir(parents=True, exist_ok=True)
    if os.path.isfile(path_to_input):
        df_zp = pd.read_csv(path_to_input / "zp_mtmc_2015_2021.csv")
    else:
        df_zp_2015 = get_data_per_year(2015, path_to_mtmc_data)
        df_zp_2021 = get_data_per_year(2021, path_to_mtmc_data)
        df_zp = pd.concat([df_zp_2015, df_zp_2021])
        # Rename variables
        df_zp = df_zp.rename(
            columns={
                "alter": "age",
                "f20400a": "driving_licence",
                "sprache": "language",
                "hhgr": "hh_size",
                "f30100": "nb_cars",
            }
        )

        df_zp["full_time"] = (df_zp.ERWERB == 1).astype(int)
        df_zp["part_time"] = (df_zp.ERWERB == 2).astype(int)

        df_zp["is_swiss"] = (df_zp.nation == 8100).astype(int)

        df_zp = df_zp.drop(columns=["ERWERB", "nation"])

        df_zp = add_mobi_variables(
            df_zp,
            path_to_mobi_zones,
            mobi_variables=["accsib_mul", "accsib_pt", "accsib_car"],
        )

        # Remove adults
        df_zp = df_zp[df_zp.age <= 17]

        df_zp["has_driving_licence"].replace({2: 0}, inplace=True)  # 0: no, 1: yes

        # Remove the one person being 12 and having a half fare subscription
        df_zp = df_zp.loc[(df_zp["HHNR"] != 292694) | (df_zp["year"] != 2015), :]

        df_zp.fillna(0, inplace=True)
        df_zp.to_csv(path_to_input / "zp_mtmc_2015_2021.csv", index=False)
    return df_zp
