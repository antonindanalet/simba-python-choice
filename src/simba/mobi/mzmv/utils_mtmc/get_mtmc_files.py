"""Gets the different datasets of the Mobility and Transport Microcensus for given years as dataframes."""
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from simba.mobi.mzmv.utils2015.codes import dict_mobi_names2mzmv_codes_hh_2015
from simba.mobi.mzmv.utils2015.codes import dict_mobi_names2mzmv_codes_zp_2015
from simba.mobi.mzmv.utils2021.codes import dict_mobi_names2mzmv_codes_hh_2021
from simba.mobi.mzmv.utils2021.codes import dict_mobi_names2mzmv_codes_zp_2021


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
            selected_columns = get_mzmv_codes(selected_columns, year, "zp")
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
            # If generic names have been used, transform column names back to generic names
            df_zp = get_generic_names(df_zp, year, "zp")
    return df_zp


def get_generic_names(df_zp: pd.DataFrame, year: int, mtmc_table: str) -> pd.DataFrame:
    list_of_column_names = df_zp.columns.tolist()
    if year == 2015:
        if mtmc_table == "zp":
            dict_mobi_names2mzmv_codes_2015 = dict_mobi_names2mzmv_codes_zp_2015
        elif mtmc_table == "hh":
            dict_mobi_names2mzmv_codes_2015 = dict_mobi_names2mzmv_codes_hh_2015
        dict_mzmv_codes2mobi_names = {
            v: k for k, v in dict_mobi_names2mzmv_codes_2015.items()
        }
    elif (year == 2020) | (year == 2021):
        if mtmc_table == "zp":
            dict_mobi_names2mzmv_codes_2021 = dict_mobi_names2mzmv_codes_zp_2021
        elif mtmc_table == "hh":
            dict_mobi_names2mzmv_codes_2021 = dict_mobi_names2mzmv_codes_hh_2021
        dict_mzmv_codes2mobi_names = {
            v: k for k, v in dict_mobi_names2mzmv_codes_2021.items()
        }
    else:
        raise ValueError("Year must be 2015, 2020 or 2021.")
    list_of_column_names = [
        dict_mzmv_codes2mobi_names.get(item, item) for item in list_of_column_names
    ]
    df_zp.columns = pd.Index(list_of_column_names)
    if (year == 2015) & (mtmc_table == "zp") & ("f40901_02" in list_of_column_names):
        df_zp = df_zp.rename(
            columns={
                "f40900": "full_part_time_job",
                "f40901_02": "percentage_first_part_time_job",  # only in 2015
                "f40903": "percentage_second_part_time_job",  # only in 2015
            }
        )
        df_zp["total_work_percentage"] = (
            (df_zp["full_part_time_job"] == 1) * 100
            + df_zp["percentage_first_part_time_job"]
            * (df_zp["percentage_first_part_time_job"] > 0)
            + df_zp["percentage_second_part_time_job"]
            * (df_zp["percentage_second_part_time_job"] > 0)
        )
        del df_zp["percentage_first_part_time_job"]
        del df_zp["percentage_second_part_time_job"]
        del df_zp["full_part_time_job"]
    return df_zp


def get_mzmv_codes(
    selected_columns: List[str], year: int, mtmc_table: str
) -> List[str]:
    """Translates generic codes (e.g. "has_ga") into the name of the variable in the MTMC, depending on the year.
    If the original name of the MTMV variable is used, it stays as it is.
    If a generic name is used, it is replaces by the name of the variable for this year."""
    if year == 2015:
        if mtmc_table == "zp":
            dict_mobi_names2mzmv_codes_2015 = dict_mobi_names2mzmv_codes_zp_2015
            if "total_work_percentage" in selected_columns:
                selected_columns.extend(["f40901_02", "f40903", "f40900"])
                selected_columns.remove("total_work_percentage")
        elif mtmc_table == "hh":
            dict_mobi_names2mzmv_codes_2015 = dict_mobi_names2mzmv_codes_hh_2015
        selected_columns = [
            dict_mobi_names2mzmv_codes_2015.get(item, item) for item in selected_columns
        ]
    elif year == 2021:
        if mtmc_table == "zp":
            dict_mobi_names2mzmv_codes_2021 = dict_mobi_names2mzmv_codes_zp_2021
        elif mtmc_table == "hh":
            dict_mobi_names2mzmv_codes_2021 = dict_mobi_names2mzmv_codes_hh_2021
        selected_columns = [
            dict_mobi_names2mzmv_codes_2021.get(item, item) for item in selected_columns
        ]
    return selected_columns


def get_hh(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    """Get the data about the households (hh) from the Mobility and Transport Microcensus."""
    if year not in [2005, 2010, 2015, 2020, 2021]:
        raise ValueError(
            "Cannot get data for other years than 2005, 2010, 2015, 2020 and 2021! (zp)"
        )
    # Define file name by year
    if year == 2005:
        file_name = "Haushalte.dat"
    else:
        file_name = "haushalte.csv"
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
    ) as haushalte_file:
        if selected_columns is None:
            df_hh = pd.read_csv(
                haushalte_file,
                delimiter=delimiter,
                dtype={"ZW2_HNR": str, "ZW3_HNR": str},
            )
            if year == 2020:
                df_hh.columns.values[
                    0
                ] = "HHNR"  # Wrong coding of the first column in the raw data
        else:
            selected_columns = get_mzmv_codes(selected_columns, year, "hh")
            if year == 2020:
                df_hh = pd.read_csv(
                    haushalte_file,
                    delimiter=delimiter,
                    dtype={"ZW2_HNR": str, "ZW3_HNR": str},
                )
                df_hh.columns.values[
                    0
                ] = "HHNR"  # Wrong coding of the first column in the raw data
                df_hh = df_hh[selected_columns]
            else:
                df_hh = pd.read_csv(
                    haushalte_file,
                    delimiter=delimiter,
                    dtype={"HHNR": int},
                    usecols=selected_columns,
                )
            # If generic names have been used, transform column names back to generic names
            df_hh = get_generic_names(df_hh, year, "hh")
    return df_hh


def get_hhp(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    """Get the data about the persons in the households from the Mobility and Transport Microcensus.

    "hhp" stands for the German word "haushaltpersonen".
    """
    if year not in [2015, 2020, 2021]:
        raise ValueError(
            "Cannot get data for other years than 2015, 2020 and 2021! (hhp)"
        )
    if year == 2015:
        delimiter = ","
    else:
        delimiter = ";"
    if (year == 2015) | (year == 2021) | (year == 2020):
        with open(
            path_to_mtmc_data.joinpath(str(year), "haushaltspersonen.csv"),
            "r",
            encoding="latin1",
        ) as haushaltspersonen_file:
            df_hhp = pd.read_csv(
                haushaltspersonen_file,
                delimiter=delimiter,
                dtype={"HHNR": int},
                usecols=selected_columns,
            )
    else:
        raise ValueError(
            "Cannot get data for other years than 2015, 2020 and 2021! (hhp)"
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


def get_trips_in_switzerland(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    if year == 2015:
        with open(
            path_to_mtmc_data.joinpath("2015", "wegeinland.csv"),
            "r",
            encoding="latin1",
        ) as trips_in_switzerland_file:
            df_trips_in_switzerland = pd.read_csv(
                trips_in_switzerland_file, delimiter=",", usecols=selected_columns
            )
    elif year == 2021:
        with open(
            path_to_mtmc_data.joinpath("2021", "wegeinland.csv"),
            "r",
            encoding="latin1",
        ) as trips_in_switzerland_file:
            df_trips_in_switzerland = pd.read_csv(
                trips_in_switzerland_file, delimiter=";", usecols=selected_columns
            )
    else:
        raise ValueError("Year not well defined")
    return df_trips_in_switzerland


def get_tours(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    if year == 2015:
        with open(
            path_to_mtmc_data.joinpath("2015", "ausgaenge.csv"),
            "r",
            encoding="latin1",
        ) as tours_file:
            df_tours = pd.read_csv(tours_file, delimiter=",", usecols=selected_columns)
    elif year == 2021:
        with open(
            path_to_mtmc_data.joinpath("2021", "ausgaenge.csv"),
            "r",
            encoding="latin1",
        ) as tours_file:
            df_tours = pd.read_csv(tours_file, delimiter=";", usecols=selected_columns)
    else:
        raise ValueError("Year not well defined")
    return df_tours


def get_etappen(
    year: int, path_to_mtmc_data: Path, selected_columns: Optional[List[Any]] = None
) -> pd.DataFrame:
    if year == 2021:
        with open(
            path_to_mtmc_data.joinpath("2021", "etappen.csv"), "r", encoding="latin1"
        ) as etappen_file:
            df_etappen = pd.read_csv(
                etappen_file,
                sep=";",
                dtype={"HHNR": int, "W_AGGLO_GROESSE2012": int},
                usecols=selected_columns,
            )
    elif year == 2015:
        with open(
            path_to_mtmc_data.joinpath("2015", "etappen.csv"), "r", encoding="latin1"
        ) as etappen_file:
            df_etappen = pd.read_csv(
                etappen_file,
                dtype={"HHNR": int, "W_AGGLO_GROESSE2012": int},
                usecols=selected_columns,
            )
    elif year == 2010:
        with open(
            path_to_mtmc_data.joinpath("2010", "/etappen.csv"), "r", encoding="latin1"
        ) as etappen_file:
            df_etappen = pd.read_csv(
                etappen_file, sep=";", dtype={"HHNR": int}, usecols=selected_columns
            )
    elif year == 2005:
        with open(
            path_to_mtmc_data.joinpath("2005", "etappen.dat"), "r", encoding="latin1"
        ) as etappen_file:
            df_etappen = pd.read_csv(
                etappen_file,
                sep="\t",
                na_values=" ",
                dtype={
                    "HHNR": int,
                    "ZIELPNR": int,
                    "E_AUSLAND": int,
                    "PSEUDO": int,
                    "F510": int,
                    "rdist": float,
                },
                usecols=selected_columns,
            )
    else:
        raise ValueError(
            "Cannot get data for other years than 2005, 2010, 2015 & 2021! (etappen)"
        )
    return df_etappen
