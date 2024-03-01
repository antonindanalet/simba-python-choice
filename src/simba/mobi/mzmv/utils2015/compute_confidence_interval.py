"""This module computes the confidence intervals using the methodology of the Federal Statistical Office (FSO).

It uses the weights available in the raw data of the Mobility and Transport Microcensus.
The methodology is the one used in 2015. In 2021, the FSO made a methodological change.
It can be used for confidence intervals when computing an average value (e.g., distance),
or when computing percentages (e.g., modal split).
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd

# coding=latin-1


def get_weighted_avg_and_std(
    table: pd.DataFrame,
    weights: str,
    percentage: Optional[bool] = False,
    list_of_columns: Optional[List[Any]] = None,
) -> Tuple[Dict[str, List[float]], int]:
    """Computes the average and the standard error. Only valid for the Mobility and Transport Microcensus."""
    if "ZIELPNR" in table:
        table["unique_identifier"] = table["HHNR"] * 10 + table["ZIELPNR"]
        nb_of_obs = len(table["unique_identifier"].unique())
        del table["unique_identifier"]
    else:
        nb_of_obs = len(table["HHNR"].unique())
    dict_column_weighted_avg_and_std = {}
    if list_of_columns is None:
        list_of_columns = table.columns.tolist()
    magic_number = 1.14  # Defined by the Federal Statistical Office (FSO).
    if percentage:
        sum_all_columns = 0.0
        for column in list_of_columns:
            if column in table:
                weighted_avg, weighted_std = weighted_avg_and_std(
                    table[column], table[weights]
                )
                sum_all_columns += weighted_avg
                dict_column_weighted_avg_and_std[column] = weighted_avg
        for column in list_of_columns:
            if column in dict_column_weighted_avg_and_std:
                weighted_percentage = np.divide(
                    dict_column_weighted_avg_and_std[column], sum_all_columns
                )
            else:
                weighted_percentage = 0.0
            variance = (
                1.645
                * magic_number
                * np.sqrt(
                    np.divide(
                        weighted_percentage * (1.0 - weighted_percentage),
                        float(nb_of_obs),
                    )
                )
            )
            dict_column_weighted_avg_and_std[column] = [weighted_percentage, variance]
    else:
        for column in list_of_columns:
            if column in table:
                weighted_avg, weighted_std = weighted_avg_and_std(
                    table[column], table[weights]
                )
                dict_column_weighted_avg_and_std[column] = [
                    weighted_avg,
                    np.divide(1.645 * magic_number * weighted_std, np.sqrt(nb_of_obs)),
                ]
    return dict_column_weighted_avg_and_std, nb_of_obs


def weighted_avg_and_std(
    values: "pd.Series[float]", weights: "pd.Series[float]"
) -> Tuple[Any, Any]:
    """Return the standard deviation. Not specific to the Mobility and Transport Microcensus.

    Args:
        values, weights -- Numpy ndarrays with the same shape.

    Returns:
        weighted average and standard error.
    """
    weighted_avg = np.average(values, weights=weights)
    centered_values = values - weighted_avg.item()
    variance = np.divide((weights * (centered_values**2)).sum(), weights.sum() - 1)
    return weighted_avg, np.sqrt(variance)
