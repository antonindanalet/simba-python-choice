import numpy as np
import pandas as pd
import statsmodels.api as sm

from simba.mobi.mzmv.config import path_to_mtmc_data
from simba.mobi.mzmv.pedestrian_speed.utils import get_and_filter_walk_etappen
from simba.mobi.mzmv.pedestrian_speed.utils import get_hours_as_text
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hh
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_trips_in_switzerland
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_zp


def linear_regression_person(year: int) -> None:
    # -- 1. Load walk etappen data and compute person speed --
    walk_etappen = get_and_filter_walk_etappen(
        year,
        selected_columns=[
            "f51300",  # transport mode
            "HHNR",
            "E_Ausland",  # Is abroad or not
            "rdist",  # distance
            "e_dauer",  # duration
            "WP",  # weights
            "WEGNR",
            "f51100",
            "f51400",
        ],
    )
    speed_person = get_speed(walk_etappen)
    # -- 2. Merge household and person data --
    speed_person = add_household_and_person_data(speed_person, year)

    # -- 3. Create binary columns --
    speed_person = create_binary_variables(speed_person)

    # -- 4. Model predictors and WLS regression --
    # Select predictor columns for the regression model.
    predictor_columns = speed_person[
        [
            "alter",
            "home_zurich_region",
            "home_urban",
            "couple_with_children",
            "work_full_time",
            "work_part_time",
            "studying",
            "work_mittelland_region",
            "GA",
            "HT",
            "VA",
            "work_german",
            "age_piece_65plus",
            "home_french",
        ]
    ]
    # Add constant for the intercept
    predictors_with_constant = sm.add_constant(predictor_columns)

    # Fit a weighted least squares model using WP as weights.
    weighted_model = sm.WLS(
        speed_person["speed"], predictors_with_constant, weights=speed_person["WP"]
    )
    weighted_result = weighted_model.fit()

    # Print model summary
    print(weighted_result.summary())


def linear_regression_trip(year: int) -> None:
    """
    Loads and merges trip data for the given year, computes person-specific speeds,
    creates binary columns for various trip and household characteristics, adds daytime
    dummy variables, and then fits a linear regression model using statsmodels, at the "trip" level.

    It prints the columns contained in the final merged DataFrame and outputs the regression summary.
    """

    # 1. Load and merge data
    etappen_cols = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
        "WEGNR",
        "f51100",
        "f51400",
    ]
    walk_etappen = get_and_filter_walk_etappen(year, etappen_cols)
    person_speed = get_speed(walk_etappen)
    walk_etappen = pd.merge(
        walk_etappen, person_speed[["HHNR", "speed"]], on="HHNR", how="left"
    )

    # Merge trips data
    df_trips = get_trips_in_switzerland(
        year,
        path_to_mtmc_data,
        selected_columns=[
            "HHNR",
            "WEGNR",
            "wmittel1",  # main transport mode (hierarchical)
            "wmittel1a",  # aggregated main transport mode
            "w_etappen",  # number of trip segments ("Etappen")
            "wzweck1",
        ],
    )
    walk_etappen = pd.merge(walk_etappen, df_trips, on=["HHNR", "WEGNR"], how="left")

    # Merge person and household data
    walk_etappen = add_household_and_person_data(walk_etappen, year)

    # 2. Create binary columns based on conditions
    walk_etappen = create_binary_variables(walk_etappen)
    # Extra mapping for trips
    # Mapping: new_column -> condition series
    binary_conditions = {
        "trips NOT by public transport": walk_etappen["wmittel1a"] != 3,
        "trips by train": walk_etappen["wmittel1"] == 2,
        "shopping": walk_etappen["wzweck1"] == 4,
        "leisure": walk_etappen["wzweck1"] == 8,
    }
    for col_name, condition in binary_conditions.items():
        walk_etappen[col_name] = np.where(condition, 1, 0)

    # 3. Add daytime dummy variables for two-hour intervals.
    # Starting at 1 minute until the end of the day, with intervals of 120 minutes.
    for lower_bound in range(1, 24 * 60, 2 * 60):
        upper_bound = lower_bound + 2 * 60
        # get_hours_as_text should return e.g. "0-2", "2-4", etc.
        hours_label = get_hours_as_text(lower_bound, upper_bound)
        walk_etappen[f"daytime{hours_label}"] = np.where(
            (walk_etappen["f51100"] >= lower_bound)
            & (walk_etappen["f51100"] < upper_bound),
            1,
            0,
        )

    # 4. Prepare predictors and fit the linear regression model using statsmodels.
    predictor_cols = [
        "trips NOT by public transport",
        "trips by train",
        "shopping",
        "leisure",
        "german",
        "alter",
        "home_zurich_region",
        "home_geneva_region",  # Uncomment additional predictors if needed:
        # "daytime0-2", "daytime2-4", "daytime4-6", "daytime6-8",
        # "daytime8-10", "daytime10-12", "daytime12-14", "daytime14-16",
        # "daytime16-18", "daytime18-20", "daytime20-22",
    ]
    predictors_with_constant = sm.add_constant(walk_etappen[predictor_cols])

    model = sm.OLS(walk_etappen["speed"], predictors_with_constant)
    result = model.fit()
    print(result.summary())

    # Optionally, you could fit a weighted regression:
    # weighted_model = sm.WLS(walk_etappen["speed"], predictors_with_constant, weights=walk_etappen["WP"])
    # weighted_result = weighted_model.fit()
    # print(weighted_result.summary())


def get_speed(walk_etappen: pd.DataFrame) -> pd.DataFrame:
    # Compute speed per person (km/h)
    person_speed = (
        walk_etappen.groupby("HHNR")
        .agg({"rdist": "sum", "e_dauer": "sum", "WP": "first"})
        .reset_index()
    )
    person_speed["speed"] = person_speed["rdist"] / person_speed["e_dauer"] * 60
    return person_speed


def add_household_and_person_data(
    speed_person: pd.DataFrame, year: int
) -> pd.DataFrame:
    hh_columns = [
        "HHNR",
        "sprache",
        "W_REGION",
        "W_stadt_land_2012",
        "hhtyp",
        "W_SPRACHE",
        "nb_of_cars",
    ]
    households = get_hh(year, path_to_mtmc_data, selected_columns=hh_columns)
    speed_person = pd.merge(speed_person, households, on="HHNR", how="left")

    zp_columns = [
        "HHNR",
        "alter",
        "ERWERB",
        "A_stadt_land_2012",
        "AU_stadt_land_2012",
        "A_REGION",
        "AU_REGION",
        "A_SPRACHE",
        "AU_SPRACHE",
        "has_ga",
        "has_hta",
        "has_va",
        "nation",
        "has_driving_licence",
    ]
    df_persons = get_zp(year, path_to_mtmc_data, selected_columns=zp_columns)
    speed_person = pd.merge(speed_person, df_persons, on="HHNR", how="left")

    # Piecewise, linear specification for age
    age_breakpoint = 65
    # Create a new predictor: additional effect of age above the breakpoint
    speed_person["age_piece_65plus"] = np.maximum(
        speed_person["alter"] - age_breakpoint, 0
    )

    age_breakpoint75 = 75
    speed_person["age_piece_75plus"] = np.maximum(
        speed_person["alter"] - age_breakpoint75, 0
    )

    return speed_person


def create_binary_variables(speed_person: pd.DataFrame) -> pd.DataFrame:
    # Languages: german (1), french (2), italian (3)
    lang_mapping = {"german": 1, "french": 2, "italian": 3}
    for col, value in lang_mapping.items():
        speed_person[col] = np.where(speed_person["sprache"] == value, 1, 0)

    # Home regions keys (W_REGION)
    home_regions = {
        "home_geneva_region": 1,
        "home_mittelland_region": 2,
        "home_northwest_region": 3,
        "home_zurich_region": 4,
        "home_east_region": 5,
        "home_central_region": 6,
        "home_tessin_region": 7,
    }
    for col, region_val in home_regions.items():
        speed_person[col] = np.where(speed_person["W_REGION"] == region_val, 1, 0)

    # Urban home indicator based on W_stadt_land_2012 (1 = urban)
    speed_person["home_urban"] = np.where(speed_person["W_stadt_land_2012"] == 1, 1, 0)

    # Household type indicators from hhtyp
    hh_type_mapping = {
        "one_person_hh": 10,
        "couple_without_children": 210,
        "couple_with_children": 220,
        "one_parent_with_children": 230,
    }
    for col, hh_val in hh_type_mapping.items():
        speed_person[col] = np.where(speed_person["hhtyp"] == hh_val, 1, 0)

    # Employment status from ERWERB: full time (1), part time (2), studying (3)
    employment_mapping = {
        "work_full_time": 1,
        "work_part_time": 2,
        "studying": 3,
    }
    for col, status in employment_mapping.items():
        speed_person[col] = np.where(speed_person["ERWERB"] == status, 1, 0)

    # Work location type (A_stadt_land_2012): urban (1), intermediary (2), rural (3)
    work_location_mapping = {
        "urban_work": 1,
        "intermediary_work": 2,
        "rural_work": 3,
    }
    for col, loc in work_location_mapping.items():
        speed_person[col] = np.where(speed_person["A_stadt_land_2012"] == loc, 1, 0)

    # Education location type (AU_stadt_land_2012): urban (1), intermediary (2), rural (3)
    edu_location_mapping = {
        "urban_education": 1,
        "intermediary_education": 2,
        "rural_education": 3,
    }
    for col, loc in edu_location_mapping.items():
        speed_person[col] = np.where(speed_person["AU_stadt_land_2012"] == loc, 1, 0)

    # Work (A_REGION) and Education (AU_REGION) regions:
    work_regions = {
        "work_geneva_region": 1,
        "work_mittelland_region": 2,
        "work_northwest_region": 3,
        "work_zurich_region": 4,
        "work_east_region": 5,
        "work_central_region": 6,
        "work_tessin_region": 7,
    }
    for col, region_val in work_regions.items():
        speed_person[col] = np.where(speed_person["A_REGION"] == region_val, 1, 0)

    edu_regions = {
        "education_geneva_region": 1,
        "education_mittelland_region": 2,
        "education_northwest_region": 3,
        "education_zurich_region": 4,
        "education_east_region": 5,
        "education_central_region": 6,
        "education_tessin_region": 7,
    }
    for col, region_val in edu_regions.items():
        speed_person[col] = np.where(speed_person["AU_REGION"] == region_val, 1, 0)

    # Creating an aggregated binary
    speed_person["education_northwest_zurich_east_region"] = np.where(
        (speed_person["AU_REGION"] == 3)
        | (speed_person["AU_REGION"] == 4)
        | (speed_person["AU_REGION"] == 5),
        1,
        0,
    )

    # GA indicator from has_ga
    speed_person["GA"] = np.where(speed_person["has_ga"] == 1, 1, 0)
    speed_person["HT"] = np.where(speed_person["has_hta"] == 1, 1, 0)
    speed_person["VA"] = np.where(speed_person["has_va"] == 1, 1, 0)

    # Language place of work: german (1), french (2), italian (3)
    lang_mapping = {"work_german": 1, "work_french": 2, "work_italian": 3}
    for col, value in lang_mapping.items():
        speed_person[col] = np.where(speed_person["A_SPRACHE"] == value, 1, 0)

    # Language place of education: german (1), french (2), italian (3)
    lang_mapping = {
        "education_german": 1,
        "education_french": 2,
        "education_italian": 3,
    }
    for col, value in lang_mapping.items():
        speed_person[col] = np.where(speed_person["AU_SPRACHE"] == value, 1, 0)

    lang_mapping = {"home_german": 1, "home_french": 2, "home_italian": 3}
    for col, value in lang_mapping.items():
        speed_person[col] = np.where(speed_person["W_SPRACHE"] == value, 1, 0)

    speed_person["is_swiss"] = np.where(speed_person["nation"] == 8100, 1, 0)

    speed_person["has_dl"] = np.where(speed_person["has_driving_licence"] == 1, 1, 0)

    speed_person["has_car"] = np.where(speed_person["nb_of_cars"] > 0, 1, 0)

    return speed_person


if __name__ == "__main__":
    linear_regression_person()
