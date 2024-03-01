"""Gets the different datasets of the Mobility and Transport Microcensus for given years as dataframes."""
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional

import numpy as np
import pandas as pd


def get_zp(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    """Get the data about the persons from the Mobility and Transport Microcensus ("zp": "Zielpersonen" in German)."""
    if year not in [2005, 2010, 2015, 2020, 2021]:
        raise ValueError(
            "Cannot get data for other years than 2005, 2010, 2015, 2020 and 2021! (zp)"
        )
    # Define file name by year
    if year == 2005:
        file_name = "zielpersonen.dat"
    else:
        file_name = "zielpersonen.csv"
    # Define delimiter by year
    if year == 2005:
        delimiter = "\t"
    elif year == 2015:
        delimiter = ","
    else:
        delimiter = ";"
    with open(
        path_to_mtmc_data.joinpath(str(year), file_name),
        "r",
        encoding="latin1",
    ) as zielpersonen_file:
        if selected_columns is None:
            df_zp = pd.read_csv(
                zielpersonen_file,
                delimiter=delimiter,
                dtype={
                    "HHNR": int,
                    "ZIELPNR": int,
                    "WP": np.longdouble,
                    "gesl": int,
                    "nation": int,
                },
            )
            if year == 2020:
                df_zp.columns.values[
                    0
                ] = "HHNR"  # Wrong coding of the first column in the raw data
        else:
            if year == 2020:
                df_zp = pd.read_csv(zielpersonen_file, delimiter=delimiter)
                df_zp.columns.values[
                    0
                ] = "HHNR"  # Wrong coding of the first column in the raw data
                df_zp = df_zp[selected_columns]
            else:
                df_zp = pd.read_csv(
                    zielpersonen_file,
                    delimiter=delimiter,
                    dtype={
                        "HHNR": int,
                        "ZIELPNR": int,
                        "WP": np.longdouble,
                        "gesl": int,
                        "nation": int,
                    },
                    usecols=selected_columns,
                )
    return df_zp


def get_hh(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    """Get the data about the households (hh) from the Mobility and Transport Microcensus."""
    if year == 2021:
        with open(
            path_to_mtmc_data.joinpath("2021", "haushalte.csv"),
            "r",
            encoding="latin1",
        ) as haushalte_file:
            df_hh = pd.read_csv(
                haushalte_file, sep=";", dtype={"HHNR": int}, usecols=selected_columns
            )
    elif year == 2020:
        with open(
            path_to_mtmc_data.joinpath("2021", "haushalte.csv"),
            "r",
            encoding="latin1",
        ) as haushalte_file:
            if selected_columns is None:
                df_hh = pd.read_csv(
                    haushalte_file, sep=";", dtype={"ZW2_HNR": str, "ZW3_HNR": str}
                )
                df_hh.columns.values[
                    0
                ] = "HHNR"  # Wrong coding of the first column in the raw data
            else:
                df_hh = pd.read_csv(
                    haushalte_file, sep=";", dtype={"ZW2_HNR": str, "ZW3_HNR": str}
                )
                df_hh.columns.values[
                    0
                ] = "HHNR"  # Wrong coding of the first column in the raw data
                df_hh = df_hh[selected_columns]
    elif year == 2015:
        with open(
            path_to_mtmc_data.joinpath("2015", "haushalte.csv"),
            "r",
            encoding="latin1",
        ) as haushalte_file:
            df_hh = pd.read_csv(
                haushalte_file, dtype={"HHNR": int}, usecols=selected_columns
            )
    elif year == 2010:
        with open(
            path_to_mtmc_data.joinpath("2010", "haushalte.csv"), "r", encoding="latin1"
        ) as haushalte_file:
            df_hh = pd.read_csv(
                haushalte_file, sep=";", dtype={"HHNR": int}, usecols=selected_columns
            )
    elif year == 2005:
        with open(
            path_to_mtmc_data.joinpath("2005", "Haushalte.dat"), "r", encoding="latin1"
        ) as haushalte_file:
            df_hh = pd.read_csv(
                haushalte_file, sep="\t", dtype={"HHNR": int}, usecols=selected_columns
            )
    else:
        raise ValueError(
            "Cannot get data for other years than 2005, 2010, 2015, 2020 and 2021! (hh)"
        )
    return df_hh


def get_hhp(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    """Get the data about the persons in the households from the Mobility and Transport Microcensus.

    "hhp" stands for the German word "haushaltpersonen".
    """
    if year == 2015:
        with open(
            path_to_mtmc_data.joinpath("2015", "haushaltspersonen.csv"),
            "r",
            encoding="latin1",
        ) as haushaltspersonen_file:
            df_hhp = pd.read_csv(
                haushaltspersonen_file, dtype={"HHNR": int}, usecols=selected_columns
            )
    elif year == 2021:
        with open(
            path_to_mtmc_data.joinpath("2021", "haushaltspersonen.csv"),
            "r",
            encoding="latin1",
        ) as haushaltspersonen_file:
            df_hhp = pd.read_csv(
                haushaltspersonen_file,
                sep=";",
                dtype={"HHNR": int},
                usecols=selected_columns,
            )
    else:
        raise ValueError(
            "Cannot get data for other years than 2015 and 2021! (hhp) "
            "Warning: These data do not exist for 2020!"
        )
    return df_hhp


def get_overnight_trips(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    """Get the data about the trips with overnight stays from the Mobility and Transport Microcensus."""
    if year == 2015:
        with open(
            path_to_mtmc_data.joinpath("2015", "reisenmueb.csv"),
            "r",
            encoding="latin1",
        ) as trips_with_overnight_file:
            df_trips_with_overnight = pd.read_csv(
                trips_with_overnight_file, delimiter=",", usecols=selected_columns
            )
    elif year == 2021:
        with open(
            path_to_mtmc_data.joinpath("2021", "reisenmueb.csv"),
            "r",
            encoding="latin1",
        ) as trips_with_overnight_file:
            df_trips_with_overnight = pd.read_csv(
                trips_with_overnight_file, delimiter=";", usecols=selected_columns
            )
    else:
        raise ValueError(
            "Cannot get data for other years than 2015 and 2021! (trips with overnight stays) "
        )
    return df_trips_with_overnight
