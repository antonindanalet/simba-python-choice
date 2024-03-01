import os

import numpy as np
import pandas as pd

from simba.mobi.choice.utils.mobi import add_mobi_variables
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hh
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hhp


def get_data(path_to_input, path_to_mobi, path_to_mtmc) -> pd.DataFrame:
    if os.path.isdir(path_to_input) is False:
        path_to_input.mkdir(parents=True, exist_ok=True)
    path_to_input = path_to_input / "hh_mtmc.csv"
    if os.path.isfile(path_to_input):
        df_hh_21 = pd.read_csv(path_to_input)
    else:
        df_hh_21 = get_data_per_year(2021, path_to_mtmc)
        df_hh_21.loc[df_hh_21["nb_cars"] > 3, "nb_cars"] = 3  # 3+ cars

        df_hh_21 = add_mobi_variables(
            df_hh_21,
            path_to_mobi,
            mobi_variables=[
                "accsib_pt",
                "accsib_car",
                "accsib_mul",
                "density",
                "pc_car",
            ],
        )
        df_hh_21 = df_hh_21[df_hh_21.nb_cars >= 0]  # -98: no answer, -97: don't know.
        df_hh_21.fillna(0, inplace=True)
        df_hh_21.to_csv(path_to_input, index=False)
    return df_hh_21


def get_data_per_year(year, path_to_mtmc) -> pd.DataFrame:
    # Load row data of the Mobility and Transport Microcensus (MTMC)
    if year == 2021:
        selected_columns = [
            "HHNR",
            "sprache",
            "hhtyp",
            "hhgr",
            "f30100",
            "W_X",
            "W_Y",
            "W_stadt_land_2012",
        ]
    else:
        raise Exception("Year not well defined")
    df_hh = get_hh(
        year, path_to_mtmc_data=path_to_mtmc, selected_columns=selected_columns
    )
    df_hh = df_hh.rename(
        columns={"hhgr": "hh_size", "f30100": "nb_cars", "sprache": "language"}
    )
    df_hh["year"] = year
    df_hhp = get_hhp(
        year,
        path_to_mtmc_data=path_to_mtmc,
        selected_columns=["HHNR", "alter", "f20400a"],
    )
    df_hhp = df_hhp.rename(columns={"alter": "age", "f20400a": "driving_licence"})
    df_hhp.loc[
        (df_hhp["driving_licence"] == -99) & (df_hhp["age"] >= 0), "driving_licence"
    ] = 0  # age known, less than 18, no driving licence
    df_hhp.loc[
        df_hhp["driving_licence"] == 2, "driving_licence"
    ] = 0  # no driving licence -> 0
    df_hhp["is_child"] = np.where(df_hhp.age < 18, 1, 0)
    df_hhp["is_adult"] = np.where(df_hhp.age < 18, 0, 1)
    df_hhp_agg = df_hhp.groupby("HHNR")[
        ["driving_licence", "is_child", "is_adult"]
    ].sum()
    df_hh = pd.merge(df_hh, df_hhp_agg, left_on="HHNR", right_index=True, how="left")
    df_hh = df_hh.rename(
        columns={
            "driving_licence": "nb_driving_licences",  # Negative = NA
            "is_child": "nb_children",
            "is_adult": "nb_adults",
        }
    )
    return df_hh
