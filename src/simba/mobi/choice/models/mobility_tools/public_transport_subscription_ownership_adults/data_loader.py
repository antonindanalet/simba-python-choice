import os
from pathlib import Path

import numpy as np
import pandas as pd

from simba.mobi.choice.utils.mobi import add_mobi_variables
from simba.mobi.choice.utils.mtmc import add_urban_typology
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hh
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hhp
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_zp


def get_data(
    path_to_input: Path, path_to_mtmc_data: Path, path_to_mobi_zones: Path
) -> pd.DataFrame:
    if os.path.isdir(path_to_input) is False:
        path_to_input.mkdir(parents=True, exist_ok=True)
    if os.path.isfile(path_to_input / "zp_mtmc_2015_2021.csv"):
        df_zp = pd.read_csv(path_to_input / "zp_mtmc_2015_2021.csv")
    else:
        print('Creating input data from initial MTMC files...')
        df_zp = get_data_per_year(2015, path_to_mtmc_data) #rather than df_zp_2015 = get_data_per_year(2015, path_to_mtmc_data)
        # df_zp_2021 = get_data_per_year(2021, path_to_mtmc_data)
        # df_zp = pd.concat([df_zp_2015, df_zp_2021])
        # Rename variables
        # print(df_zp.columns)
        df_zp = df_zp.rename(
            columns={
                "alter": "age",
                # "f20400a": "driving_licence",
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

        # Remove children
        df_zp = df_zp[df_zp.age > 17]

        df_zp["has_driving_licence"].replace({2: 0}, inplace=True)  # 0: no, 1: yes
        # print(df_zp.columns)
        df_zp.fillna(0, inplace=True)
        df_zp.to_csv(path_to_input / "zp_mtmc_2015_2021.csv", index=False)
    return df_zp


def get_data_per_year(year: int, path_to_mtmc_data: Path) -> pd.DataFrame:
    # Load row data of the Mobility and Transpot Microcensus (MTMC)
    if year == 2015:
        selected_columns = [
            "HHNR",
            "alter",
            "sprache",
            "ERWERB",
            "nation",
            "f20400a",
            "f41610a",      # GA, variable 2015
            "f41610b",      # Halbtax
            "f41610c",      # Verbundabo
            'activity_1_if_not_working',      # AV: In Ausbildung
            'activity_2_if_not_working',
            'activity_3_if_not_working',
            'AU_X_CH1903', 
            'AU_Y_CH1903',
            'A_X_CH1903',
            'A_Y_CH1903', 
        ]  
    elif year == 2021:
        selected_columns = [
            "HHNR",
            "alter",
            "sprache",
            "ERWERB",
            "nation",
            "f20400a",
            "f41600_01a",   # GA, variable 2021
            "f41600_01b",   # Halbtax
            "f41600_01c",   # Verbundabo
            'f41001b',      # AV: In Ausbildung
            'f41001c',
            'AU_X_CH1903',
            'AU_Y_CH1903',
            'A_X_CH1903',
            'A_Y_CH1903', 
            'f30100'
        ]  
    else:
        raise ValueError("Year not well defined! It must be 2015 or 2021...")
    df_zp = get_zp(year, path_to_mtmc_data, selected_columns=selected_columns)
    df_zp = df_zp.rename(
        columns={
            "f41610a": "GA_ticket",
            "f41610c": "Verbund_Abo",
            "f41610b": "halbtax_ticket",
            #problem with column names
            "has_ga": "GA_ticket",
            "has_va": "Verbund_Abo",
            "has_hta": "halbtax_ticket",
            "f41600_01a": "GA_ticket",
            "f41600_01c": "Verbund_Abo",
            "f41600_01b": "halbtax_ticket",
        }
    )
    # print(df_zp.columns)
    df_zp["subscriptions"] = df_zp.apply(lambda row: label_subscriptions(row), axis=1)
    df_zp = df_zp[df_zp.subscriptions >= 0]

    if year == 2015:
        selected_columns = ["HHNR", "hhtyp", "W_X", "W_Y", 'W_X_CH1903', 'W_Y_CH1903', "hhgr", "f30100", "W_BFS"]
    elif year == 2021:
        selected_columns = [
            "HHNR",
            "hhtyp",
            "W_X",
            "W_Y",
            'W_X_CH1903',
            'W_Y_CH1903',
            "hhgr",
            "f30100",
            "W_stadt_land_2012",
        ]
    df_hh = get_hh(year, path_to_mtmc_data, selected_columns=selected_columns)
    if year == 2015:
        df_hh = add_urban_typology(df_hh)
        df_hh = df_hh.drop("W_BFS", axis=1)
    df_hh["year"] = year
    df_hhp = get_hhp(year, path_to_mtmc_data, selected_columns=["HHNR", "alter"])
    df_hhp = df_hhp.rename(columns={"alter": "age"})
    df_hhp["is_adult"] = np.where(df_hhp.age < 18, 0, 1)
    df_hhp = df_hhp.drop(columns=["age"])
    df_hhp_agg = df_hhp.groupby("HHNR").sum()
    df_hh = pd.merge(df_hh, df_hhp_agg, left_on="HHNR", right_index=True, how="left")
    df_hh = df_hh.rename(columns={"is_adult": "nb_adults"})
    df_zp = pd.merge(df_zp, df_hh, on="HHNR", how="left")

    #AV
    df_zp['In_Ausbildung'] = df_zp.apply(lambda x: 1 if (x['activity_1_if_not_working'] == 32) or (x['activity_2_if_not_working'] == 32) or (x['activity_3_if_not_working'] == 32) else 0, axis=1)
    # df_zp.drop(columns=['f41001a', 'f41001b', 'f41001c'], inplace=True)

    df_zp['dist_home_uni'] = np.sqrt((df_zp.W_X_CH1903 - df_zp.AU_X_CH1903)**2 + (df_zp.W_Y_CH1903 - df_zp.AU_Y_CH1903)**2) * df_zp['In_Ausbildung']
    # df_zp['dist_home_work'] = np.sqrt((df_zp.W_X_CH1903 - df_zp.A_X_CH1903)**2 + (df_zp.W_Y_CH1903 - df_zp.A_Y_CH1903)**2)
    return df_zp


def label_subscriptions(row) -> int:
    # 1: NONE, 2: GA, 3: HT, 4: V, 5: HT + V
    if row["GA_ticket"] == 1:  # GA
        if row["halbtax_ticket"] == 1:
            # Warning: Person with GA and HT are considered as "GA"
            return 2
        elif row["halbtax_ticket"] == 2:  # No HT
            return 2  # GA (no HT)
        else:
            return -98
    elif row["GA_ticket"] == 2:  # No GA
        if row["halbtax_ticket"] == 1:  # HT
            if row["Verbund_Abo"] == 1:
                return 5  # HT + Verbundabo (no GA)
            elif row["Verbund_Abo"] == 2:
                return 3  # HT (no GA, no Verbundabo)
            else:  # no info about Verbundabo
                return -98
        elif row["halbtax_ticket"] == 2:  # No HT
            if row["Verbund_Abo"] == 1:
                return 4  # Verbundabo (no GA, no HT)
            elif row["Verbund_Abo"] == 2:
                return 1  # no GA, no Verbundabo, no HT
            else:  # no info about Verbundabo
                return -98
        else:  # no info about HT
            return -98
    else:  # no information about GA
        return -98
