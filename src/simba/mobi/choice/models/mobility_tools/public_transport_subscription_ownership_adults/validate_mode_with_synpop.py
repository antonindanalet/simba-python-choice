import pickle
import sys
from math import isnan
from pathlib import Path

import biogeme.exceptions as excep
import biogeme.results as res
import numpy as np
import pandas as pd

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.descriptive_stats import (
    compute_shares_of_subscriptions,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.model_simulation import (
    run_simulation,
)
from simba.mobi.choice.utils.mobi import add_mobi_variables


def validate_model_with_syn_pop_2022(
    input_directory: Path, output_directory: Path, path_to_mobi_zones: Path
) -> None:
    input_data_for_simulation = input_directory / "validation_with_SynPop"
    input_data_for_simulation.mkdir(parents=True, exist_ok=True)
    year = 2022
    dict_observed_shares_of_subscriptions = compute_shares_of_subscriptions()
    print(
        "Proportion of subscriptions (register data):",
        dict_observed_shares_of_subscriptions,
    )
    """ External validation using a synthetic population """
    # Prepare the data for PandasBiogeme
    generate_data_file_for_simulation(
        input_data_for_simulation, year, path_to_mobi_zones
    )
    dict_results = apply_model_to_synthetic_population(
        input_data_for_simulation, output_directory, year
    )
    # Compare rate of home office in the MTMC and in the synthetic population
    print("Proportion of subscriptions (synpop):", dict_results)
    with open(output_directory / "dict_results_validation.pickle", "wb") as pickle_file:
        pickle.dump(dict_results, pickle_file)


def apply_model_to_synthetic_population(
    input_data_for_simulation: Path, output_directory: Path, year: int
):
    output_directory_for_simulation = output_directory / "validation_with_SynPop"
    output_directory_for_simulation.mkdir(parents=True, exist_ok=True)
    # Simulate the model on the synthetic population
    if year == 2022:
        data_file_name_for_simulation = "persons_from_SynPop2022.pkl"
    else:
        raise Exception("Year not well defined!")
    df_persons = pd.read_pickle(
        input_data_for_simulation / data_file_name_for_simulation
    )
    try:
        results = res.bioResults(
            pickleFile=output_directory / "2015_2021/dcm_indivPT.pickle"
        )
    except excep.BiogemeError:
        sys.exit("Could not find estimation results. Please run the estimation first.")
    beta_values = results.getBetaValues()
    dict_results = run_simulation(df_persons, beta_values)
    return dict_results


def generate_data_file_for_simulation(
    input_data_for_simulation: Path, year: int, path_to_mobi_zones: Path
):
    """Generates the data file for applying the model to the synthetic population (SynPop).
    In particular, it changes the format of the SynPop and adds some geospatial information,
    the connection quality of public transport where the person lives (in German: OeV-Gueteklassen, see
    https://www.are.admin.ch/are/de/home/mobilitaet/grundlagen-und-daten/verkehrserschliessung-in-der-schweiz.html
    :return: Nothing, but saves a CSV file 'persons_from_SynPop2017.csv' in data/output/data/application_to_synpop/
    """
    if year == 2022:
        data_file_name = "persons_from_SynPop2022.pkl"
        path_to_input_file = input_data_for_simulation / data_file_name
    else:
        raise Exception(
            "Reference year for synthetic population not well defined ("
            + str(year)
            + ")"
        )
    if path_to_input_file.exists() is False:
        print("Generating data file...")
        df_persons = get_persons_from_synthetic_population(year)
        nb_of_persons_before = len(df_persons)
        df_persons = add_information_about_households_from_synthetic_population(
            df_persons, year
        )
        """ Test that the number of people are still the same """
        nb_of_persons_after = len(df_persons)
        if nb_of_persons_after != nb_of_persons_before:
            raise Exception("Error: Some people got lost on the way!")
        df_persons = add_mobi_variables(
            df_persons,
            path_to_mobi_zones,
            mobi_variables=["accsib_mul", "accsib_pt", "accsib_car"],
            x_variable="xcoord",
            y_variable="ycoord",
            crs="epsg:2056",
        )
        # Keep only the variables for the simulation of the model
        df_persons["cars_per_adult"] = (df_persons["nb_persons_in_hh"] > 0) * (
            df_persons["hcar_ownership"] / df_persons["nb_persons_in_hh"]
        )
        df_persons = df_persons.drop("nb_persons_in_hh", axis=1)
        df_persons["german"] = np.where(df_persons["language"] == 1, 1, 0)
        df_persons = df_persons.drop("language", axis=1)
        df_persons["is_swiss"] = np.where(df_persons["nation"] == 0, 1, 0)
        df_persons = df_persons.drop("nation", axis=1)
        df_persons["full_time"] = np.where(df_persons["work_percentage"] >= 90, 1, 0)
        df_persons["part_time"] = np.where(
            (df_persons["work_percentage"] > 0) & (df_persons["work_percentage"] < 90),
            1,
            0,
        )
        df_persons = df_persons.drop("work_percentage", axis=1)
        df_persons["couple_without_children"] = np.where(
            (df_persons["htype"] == 20)
            | (df_persons["htype"] == 21)
            | (df_persons["htype"] == 22),
            1,
            0,
        )
        df_persons["couple_with_children"] = np.where(
            (df_persons["htype"] == 30)
            | (df_persons["htype"] == 31)
            | (df_persons["htype"] == 32),
            1,
            0,
        )
        df_persons["single_parent_house"] = np.where(df_persons["htype"] == 4, 1, 0)
        df_persons["one_person_household"] = np.where(df_persons["htype"] == 1, 1, 0)
        df_persons = df_persons.drop("htype", axis=1)
        df_persons["boxcox_accessib_pt"] = (
            (df_persons["accsib_pt"] / 1000000) ** 0.1552 - 1
        ) / 0.1552
        df_persons = df_persons.drop("accsib_pt", axis=1)
        df_persons["boxcox_accessib_car"] = (
            (df_persons["accsib_car"] / 1000000) ** 0.1741 - 1
        ) / 0.1741
        df_persons = df_persons.drop("accsib_car", axis=1)
        df_persons["boxcox_accsib_mul"] = (
            (df_persons["accsib_mul"] / 1000000) ** 0.1973 - 1
        ) / 0.1973
        df_persons = df_persons.drop("accsib_mul", axis=1)
        df_persons["urban"] = np.where(df_persons["sl3_id"] == 1, 1, 0)
        df_persons = df_persons.drop("sl3_id", axis=1)
        """ Save the file """
        """ Test that no column contains NA values """
        for column in df_persons.columns:
            if df_persons[column].isna().any():
                print("There are NA values in column", column)
        df_persons.to_pickle(path_to_input_file)


def add_information_about_households_from_synthetic_population(
    df_persons: pd.DataFrame, year: int
) -> pd.DataFrame:
    """Read the households from the synthetic population"""
    if year == 2022:
        synpop_folder_path = Path(
            r"\\wsbbrz0283\mobi\42_SynPop\22_SynPop_MOBi_5.x\Lieferungen_Strittmatter\240402_ARE_SBB_Schlussabgabe_4\01_Daten\240327_CH_2022_NPVM_v29_040_BEST1"
        )
        synpop_households_file_name = "households.csv"
    else:
        raise ValueError(
            'Reference year of the synthetic population not well defined for "households"'
        )
    selected_columns = [
        "household_id",
        "htype",  # Type of household (1: single, ...)
        "hcar_ownership",  # nb of cars in hh
        "location_id",
        "xcoord",
        "ycoord",
    ]
    with open(synpop_folder_path / synpop_households_file_name, "r") as households_file:
        df_households = pd.read_csv(households_file, sep=";", usecols=selected_columns)
    df_households = add_urban_typology(df_households)
    df_persons = pd.merge(df_persons, df_households, on="household_id", how="left")
    return df_persons


def add_urban_typology(df_households: pd.DataFrame) -> pd.DataFrame:
    """Add urban/rural typology of the home place from zone_id
    :param df_households: Contains the households from the SynPop, incl. zone ID
    :return: df_households: Contains the households from the SynPop, including a column containing the urban/rural
    typology
         French        German      English (my own translation)
    - 1: Urbain        Städtisch   urban
    - 2: Intermédiaire Intermediär periruban
    - 3: Rural         Ländlich    rural
    """
    # Read the CSV file containing the urban/rural typology 2017
    zones_folder_path = Path(r"Z:\50_Ergebnisse\MOBi_4.0\2017\plans\3.3.2017.7.100pct")
    selected_columns = ["sl3_id", "zone_id"]
    with open(zones_folder_path / "mobi-zones.csv", "r") as zone_file:
        df_urban_typology = pd.read_csv(zone_file, sep=";", usecols=selected_columns)
    df_households = pd.merge(
        df_households,
        df_urban_typology,
        left_on="location_id",
        right_on="zone_id",
        how="left",
    )
    return df_households


def get_persons_from_synthetic_population(year: int):
    """Read the persons from the synthetic population"""
    if year == 2022:
        synpop_folder_path = Path(
            r"path_to_synpop_files"
        )
        synpop_persons_file_name = "persons.csv"
    else:
        raise ValueError(
            'Reference year of the synthetic population not well defined for "persons"'
        )
    selected_columns = [
        "dbirth",  # date of birth
        "household_id",
        "nation",
        "language",
        "person_id",
        "driving_licence",
        "public_transport",
        "empl_fte",
        "jtype",  # Type of job: 0 unemployed, 1 one job, 2 two jobs, 3 apprentice, 9 working abroad
    ]
    with open(synpop_folder_path / synpop_persons_file_name, "r") as persons_file:
        df_persons = pd.read_csv(persons_file, sep=";", usecols=selected_columns)
    """ Transform the data structure """
    # Transform the 'date of birth' variable to an 'age' variable (reference year: 2022 or 2023?)
    df_persons["age"] = year - df_persons["dbirth"].str.split("-", expand=True)[
        2
    ].astype(int)
    del df_persons["dbirth"]
    df_persons = df_persons.loc[df_persons["age"] >= 18, :]
    # Transform the variable about employment to a variable about being employed
    df_persons["employed"] = df_persons["jtype"].apply(
        lambda x: -99 if isnan(x) else (1 if (x == 1) | (x == 2) | (x == 9) else 1)
    )
    # Transform the variable about level of employment to a binary variable about working full time
    df_persons.rename(columns={"empl_fte": "work_percentage"}, inplace=True)
    # Recode NA values in mobility resources variable ("mobility")
    df_persons["jtype"] = df_persons["jtype"].fillna(-99)
    df_persons["nb_persons_in_hh"] = df_persons.groupby(["household_id"])[
        "household_id"
    ].transform(
        "count"
    )  # Aggregate over people
    # Get number of adults in hh # not needed: only adults in this case
    # df_adults = df_persons.loc[df_persons.age >= 18, ["household_id", "person_id"]]
    # nb_adults_by_hh = df_adults.groupby(['household_id']).count()
    # nb_adults_by_hh = nb_adults_by_hh.rename(columns={'person_id': 'nb_adults_in_hh',})
    # df_persons = pd.merge(df_persons, nb_adults_by_hh, left_on="household_id", right_index=True, how="left")
    # df_persons['nb_adults_in_hh'] = df_persons['nb_adults_in_hh'].fillna(0)
    return df_persons
