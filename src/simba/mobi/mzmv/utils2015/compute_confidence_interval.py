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

# Constant
MAGIC_NUMBER = 1.14  # Defined by the Federal Statistical Office (FSO)


def get_weighted_avg_and_std(
    table: pd.DataFrame,
    weights: str,
    percentage: Optional[bool] = False,
    list_of_columns: Optional[List[Any]] = None,
) -> Tuple[Dict[str, List[float]], int, int]:
    """Calculates the weighted average and the standard error for specified columns.
    Only valid for the Mobility and Transport Microcensus 2015. Another approach has been used in 2021 (more complex).
    Inputs:
    - table: The Input DataFrame from the Mobility and Transport Microcensus.
    - weights: The column name in the DataFrame representing the weights for the weighted average and standard deviation
    calculation. Can be "WP" if averaging on persons or "WM" if averaging on households.
    - percentage: Defines if the outputs are percentages or an average absolute value.
    - list_of_columns: A list of column names in the DataFrame for which the weighted average and standard deviation
    should be calculated. If not provided, all columns in the DataFrame will be considered.
    Outputs:
    - dict_column_weighted_avg_and_std: A dictionary where the keys are the column names, and the values are lists
    containing the weighted average and standard deviation (or weighted percentage and variance if percentage is True)
    for each column.
    - nb_of_obs (int): The number of unique observations in the DataFrame. Statistical basis of the average.
    - total (int): The total weighted sum across all columns.
    Useful when computing something else than modal split in the segment."""

    # Constant
    z_score = 1.645  # Z-score for 90% confidence interval (adjustable)

    if "ZIELPNR" in table:
        series_unique_identifier = table["HHNR"] * 10 + table["ZIELPNR"]
        nb_of_obs = len(series_unique_identifier.unique())
    else:
        nb_of_obs = len(table["HHNR"].unique())
    dict_column_weighted_avg_and_std = {}
    if list_of_columns is None:
        # Filtering numeric columns only
        list_of_columns = table.select_dtypes(include=[np.number]).columns.tolist()
    total = 0
    if percentage:
        sum_all_columns = 0.0
        for column in list_of_columns:
            if column in table:
                total += sum(table[column] * table[weights])
                weighted_avg, weighted_std = weighted_avg_and_std(
                    table[column], table[weights]
                )
                sum_all_columns += weighted_avg
                dict_column_weighted_avg_and_std[column] = weighted_avg
        dict_column_weighted_avg_and_std = compute_percentage(
            list_of_columns,
            dict_column_weighted_avg_and_std,
            sum_all_columns,
            nb_of_obs,
            z_score,
        )
    else:
        for column in list_of_columns:
            if column in table:
                total += sum(table[column] * table[weights])
                weighted_avg, weighted_std = weighted_avg_and_std(
                    table[column], table[weights]
                )
                dict_column_weighted_avg_and_std[column] = [
                    weighted_avg,
                    np.divide(
                        z_score * MAGIC_NUMBER * weighted_std, np.sqrt(nb_of_obs)
                    ),
                ]
    return dict_column_weighted_avg_and_std, nb_of_obs, total


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


def get_moving_weighted_avg_and_std(
    table: pd.DataFrame,
    weights: str,
    percentage: Optional[bool] = False,
    list_of_columns: Optional[List[Any]] = None,
) -> Tuple[Dict[str, List[float]], int, int]:
    """Calculates the moving weighted average and the standard error for specified columns.
    Only available for percentage as True for now, and for a moving window -1/+1.
    If percentage as False is needed, the code below needs an update."""

    # Constant
    z_score = 1.645  # Z-score for 90% confidence interval (adjustable)

    if "ZIELPNR" in table:
        series_unique_identifier = table["HHNR"] * 10 + table["ZIELPNR"]
        nb_of_obs = len(series_unique_identifier.unique())
    else:
        nb_of_obs = len(table["HHNR"].unique())

    # Handle list_of_columns
    if list_of_columns is None:
        # Filtering numeric columns only
        list_of_columns = table.select_dtypes(include=[np.number]).columns.tolist()

    # Validate weights
    if weights not in table.columns:
        raise ValueError(f"Weight column '{weights}' not found in the table.")

    dict_column_weighted_avg_and_std = {}
    total = 0

    if percentage:
        sum_all_columns = 0.0
        for column in list_of_columns:
            if column in table:
                total += (table[column] * table[weights]).sum()
                observations, weights_for_avg = apply_moving_window(
                    column, list_of_columns, table, weights
                )
                weighted_avg, _ = weighted_avg_and_std(observations, weights_for_avg)
                sum_all_columns += weighted_avg
                dict_column_weighted_avg_and_std[column] = weighted_avg

        # Compute percentages
        dict_column_weighted_avg_and_std = compute_percentage(
            list_of_columns,
            dict_column_weighted_avg_and_std,
            sum_all_columns,
            nb_of_obs,
            z_score,
        )
    else:
        raise NotImplementedError("Non-percentage calculation is not yet implemented.")

    return dict_column_weighted_avg_and_std, nb_of_obs, total


def compute_percentage(
    list_of_columns: List[Any],
    dict_column_weighted_avg_and_std: Dict[str, List[float]],
    sum_all_columns: float,
    nb_of_obs: int,
    z_score: float,
) -> Dict[str, List[float]]:
    for column in list_of_columns:
        if column in dict_column_weighted_avg_and_std:
            weighted_percentage = float(
                np.divide(dict_column_weighted_avg_and_std[column], sum_all_columns)
            )
        else:
            weighted_percentage = 0.0

        variance = (
            z_score
            * MAGIC_NUMBER
            * np.sqrt(
                np.divide(
                    weighted_percentage * (1.0 - weighted_percentage),
                    float(nb_of_obs),
                )
            )
        )
        dict_column_weighted_avg_and_std[column] = [weighted_percentage, variance]

    return dict_column_weighted_avg_and_std


def apply_moving_window(
    column: str,
    list_of_columns: List[Any],
    table: pd.DataFrame,
    weights: str,
) -> Tuple[pd.Series, pd.Series]:
    column_index = list_of_columns.index(column)
    not_first_observation = column_index > 0
    not_last_observation = column_index < len(list_of_columns) - 1

    observations = [table[column]]  # Series as list
    weights_for_avg = [table[weights]]  # Series as list

    if not_first_observation and (list_of_columns[column_index - 1] in table.columns):
        previous_column = list_of_columns[column_index - 1]
        observations.append(table[previous_column])
        weights_for_avg.append(table[weights])
    if not_last_observation and list_of_columns[column_index + 1] in table.columns:
        next_column = list_of_columns[column_index + 1]
        observations.append(table[next_column])
        weights_for_avg.append(table[weights])

    return pd.concat(observations), pd.concat(weights_for_avg)
