import os
from pathlib import Path

import geopandas
import numpy as np
import openmatrix as omx
import pandas as pd

from simba.mobi.choice.models.homeoffice.constants import hh_columns
from simba.mobi.choice.models.homeoffice.constants import zp_columns
from simba.mobi.choice.models.homeoffice.model_definition import (
    define_telecommuting_variable,
)
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hh
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hhp
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_zp


def get_data(input_directory: Path) -> pd.DataFrame:
    path_to_mtmc_data = r"path_to_transport_and_mobility_microcensus_folder"
    path_to_data_folder_for_all_years = input_directory / "2015_2020_2021"
    if os.path.isfile(path_to_data_folder_for_all_years / "persons.csv"):
        df_zp_2015_2020_2021 = pd.read_csv(
            path_to_data_folder_for_all_years / "persons.csv", sep=";"
        )
    else:
        df_zp_2015 = get_data_per_year(2015, input_directory, path_to_mtmc_data)
        df_zp_2020 = get_data_per_year(2020, input_directory, path_to_mtmc_data)
        df_zp_2021 = get_data_per_year(2021, input_directory, path_to_mtmc_data)
        df_zp_2015_2020 = merge_data_files(df_zp_2015, df_zp_2020)
        df_zp_2015_2020_2021 = merge_data_files(df_zp_2015_2020, df_zp_2021)
        path_to_data_folder_for_all_years.mkdir(parents=True, exist_ok=True)
        df_zp_2015_2020_2021.to_csv(
            path_to_data_folder_for_all_years / "persons.csv", sep=";", index=False
        )
    return df_zp_2015_2020_2021


def merge_data_files(df_zp1: pd.DataFrame, df_zp2: pd.DataFrame) -> pd.DataFrame:
    # if year == 2020:
    #     df_2015 = df_2015.drop('nb_driving_licences', axis=1)

    # Merge year1 and year2
    df_merged = pd.concat([df_zp1, df_zp2], ignore_index=True)

    """ Test that no column contains NA values """
    for column in df_merged.columns:
        if df_merged[column].isna().any():
            print("There are NA values in column", column)
    return df_merged


def get_data_per_year(
    year: int, input_directory: Path, path_to_mtmc_data: Path
) -> pd.DataFrame:
    # Input daten
    path_to_mobi_server = Path(r"\\wsbbrz0283\mobi")
    path_to_mobi_zones = (
        path_to_mobi_server / r"50_Ergebnisse\MOBi_3.1\plans\3.1.4.2020"
    )
    path_to_npvm_zones = (
        path_to_mobi_server.joinpath("10_Daten")
        .joinpath("NPVM_Zonen")
        .joinpath("Verkehrszonen_Schweiz_NPVM_2017")
        .joinpath("Verkehrszonen_Schweiz_NPVM_2017_zone_id.gpkg")
    )
    path_to_typology = path_to_mobi_server / r"10_Daten\Raumgliederungen"
    path_to_skim_file = (
        path_to_mobi_server / r"50_Ergebnisse/MOBi_3.2/plans/3.2_2017_10pct/"
    )
    # Data file for estimation, information about saving a file for a specific year
    path_to_data_file_for_a_year = input_directory / str(year)
    # path_to_data_file_for_a_year.mkdir(parents=True, exist_ok=True)
    data_file_name = "persons.csv"
    path_to_data_file_for_a_year = path_to_data_file_for_a_year / data_file_name
    # Read the data, if a data file for a specific year was already saved
    # if os.path.isfile(path_to_data_file_for_a_year):
    #     df_zp = pd.read_csv(path_to_data_file_for_a_year, sep=";")
    # else:
    # Generate the data
    df_zp = generate_data_file(
        year,
        path_to_mtmc_data,
        path_to_mobi_zones,
        path_to_npvm_zones,
        path_to_typology,
        path_to_data_file_for_a_year,
        path_to_skim_file,
    )
    df_zp["year"] = year
    """ Test that no column contains NA values """
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print("There are NA values in column (" + str(year) + ")", column)
    return df_zp


def generate_data_file(
    year: int,
    path_to_mtmc_data: Path,
    path_to_mobi_zones: Path,
    path_to_npvm_zones: Path,
    path_to_typology: Path,
    path_to_output_data_file: Path,
    path_to_skim_file: Path,
) -> pd.DataFrame:
    """This function reads the  data about the person.
    It then joins them with the data about the household and the spatial typology.
    It returns nothing, but saves the output as a data file for Biogeme.
        :param: Year of the Mobility and Transport Microcensus. Possible values: 2015 or 2020.
        :return: The dataframe.
        It can save the dataframe as a CSV file (separator: tab) without NA values, in Biogeme format.
    """
    """ Select the variables about the person from the tables of the MTMC """
    selected_columns_zp = zp_columns[year]
    df_zp = get_zp(year, path_to_mtmc_data, selected_columns_zp)
    selected_columns_hh = hh_columns[year]
    df_hh = get_hh(year, path_to_mtmc_data, selected_columns_hh)
    df_zp = pd.merge(df_zp, df_hh, on="HHNR", how="left")

    df_zp = add_accessibility(df_zp, path_to_mobi_zones, path_to_npvm_zones)

    """Public transport connection quality was tested, was however not significant.
    The variable is not added in the dataset anymore."""
    # df_zp = add_public_transport_connection_quality(df_zp, year)

    df_zp = add_home_work_crow_fly_distance(df_zp)

    df_zp = add_spatial_typology(df_zp, year, path_to_typology)

    """ Get information about the members of the household """
    df_hhp = get_hhp(year, path_to_mtmc_data, selected_columns=["HHNR", "alter"])

    df_zp = add_number_of_children(df_zp, df_hhp, age_limit=21)
    del df_zp["hhgr"]

    # df_zp = add_number_of_driving_licence(df_zp, df_hhp)

    """ Generate the variable about work position:
    Code FaLC in English     FaLC in German   NPVM                       Code used below
     0   Unemployed                                                      0
     1   CEO                 Geschäftsführer  qualifizierter Mitarbeiter 1
     11  business management Geschäftsleitung qualifizierter Mitarbeiter 1
     12  management          qualifizierte MA qualifizierter Mitarbeiter 1
     20  Employee            einfache MA      einfacher Mitarbeiter      2
     3   Apprentice          Lehrling                                    3
     "NPVM" stands for "nationale Personenverkehrsmodell", the Swiss national passenger transport model.
     "MTMC", below, stands for Mobility and Transport Microcensus, the Swiss travel survey.
     In the code below, -99 corresponds to no answer/doesn't know to the question about work position
     (if working) """
    df_zp.loc[
        df_zp["f40800_01"].isin(
            [
                1,  # MTMC: "Selbstständig Erwerbende(r)"
                2,  # MTMC: Arbeitnehmer in AG/GmbH, welche IHNEN selbst gehört
                3,
            ]
        ),  # MTMC: Arbeitnehmer im Familienbetrieb von Haushaltsmitglied
        "work_position",
    ] = 1  # NPVM: Qualifiziert
    df_zp.loc[
        (df_zp["f40800_01"] == 4)
        & (  # MTMC: Arbeitnehmer bei einem sonstigen Unternehmen
            df_zp["f41100_01"] == 1
        ),  # MTMC: Angestellt ohne Cheffunktion
        "work_position",
    ] = 2  # NPVM: Einfach
    df_zp.loc[
        (df_zp["f40800_01"] == 4)
        & (  # MTMC: Arbeitnehmer bei einem sonstigen Unternehmen
            df_zp["f41100_01"].isin([2, 3])  # MTMC: Angestellt mit Chefposition
        ),  # MTMC: Angestellt als Mitglied von der Direktion
        "work_position",
    ] = 1  # SynPop: Qualifiziert
    df_zp.loc[
        df_zp["f40800_01"] == 5, "work_position"  # MTMC: Lehrling
    ] = 3  # NPVM: Apprentice
    df_zp.loc[
        df_zp["f41100_01"] == 3,  # MTMC: Angestellt als Mitglied von der Direktion
        "work_position",
    ] = 1  # NPVM: Qualifiziert
    df_zp.loc[
        df_zp["f40800_01"] == -99, "work_position"  # MTMC: Nicht erwerbstätig
    ] = 0  # NPVM: Unemployed
    df_zp.loc[
        (df_zp["f40800_01"] == 4) & (df_zp["f41100_01"].isin([-98, -97])),
        "work_position",
    ] = -99
    del df_zp["f40800_01"]
    del df_zp["f41100_01"]

    # Rename the variables
    if year == 2015:
        highest_education_variable_name = "HAUSB"
    elif (year == 2020) | (year == 2021):
        highest_education_variable_name = "f40120"
    else:
        raise ValueError("Year must be 2015, 2020 or 2021!")
    df_zp = df_zp.rename(
        columns={
            "gesl": "sex",
            highest_education_variable_name: "highest_educ",
            "f81300": "telecommuting_is_possible",
            "hhtyp": "hh_type",
            "W_OeV_KLASSE": "public_transport_connection_quality_ARE_home",  # in 2015
            "W_OEV_KLASSE": "public_transport_connection_quality_ARE_home",  # in 2020/2021
            "alter": "age",
            "f81400": "percentage_telecommuting",
            "sprache": "language",
            "f40900": "full_part_time_job",
            "f40901_02": "percentage_first_part_time_job",  # only in 2015
            "f40903": "percentage_second_part_time_job",  # only in 2015
            "f40920": "percentage_part_time_job",  # only in 2020
            "F20601": "hh_income",  # naming 2015
            "f20601": "hh_income",  # naming 2020
            "f42100e": "car_avail",
            "f41610a": "GA_ticket",  # 2015
            "f41610b": "halbtax_ticket",  # 2015
            "f41610c": "Verbund_Abo",  # 2015
            "f41600_01a": "GA_ticket",  # 2020
            "f41600_01b": "halbtax_ticket",  # 2020
            "f41600_01c": "Verbund_Abo",  # 2020
            "f41000a": "other_activities_if_working1",
            "f41000b": "other_activities_if_working2",
            "f41000c": "other_activities_if_working3",
            "f41001a": "activity_status_if_not_working1",
            "f41001b": "activity_status_if_not_working2",
            "f41001c": "activity_status_if_not_working3",
            "f20400a": "has_driving_license",
            "f30100": "num_cars_in_hh",
        }
    )
    df_zp["mobility_resources"] = df_zp.apply(
        define_mobility_resources_variable, axis=1
    )

    """ Removing people who did not get the question or did not answer. """
    df_zp.drop(df_zp[df_zp.telecommuting_is_possible < 0].index, inplace=True)
    # ''' Define the variable home office as "possibility to do home office" '''
    df_zp["telecommuting"] = df_zp.apply(define_telecommuting_variable, axis=1)

    """ Define the business sectors:
    The 10 business sectors are an aggregation of the General Classification of Economic Activities (NOGA 2008)
    defined by the Swiss Federal Statistical Office (FSO).
    The correspondence between NOGA codes and the aggregation can be found in:
    Balz Bodenmann, Pascal Buerki, Camilla Philipp, Nadja Bernhard, Kirill Mueller, Andreas Justen, Antonin Danalet,
    Nicole A. Mathys, Wolfgang Scherr, Denis Metrailler, and Nathalie Frischknecht. Synthetische Population 2017 -
    Modellierung mit dem Flaechennutzungsmodell FaLC. Technical report, Federal Office for Spatial Development ARE and
    Swiss Federal Railways SBB, Bern, 2019,
    https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/synthetische-population-2017.html
    The correspondence between the numeric NOGA codes and the names of the economic activities can be found in:
    Federal Statistical Office. NOGA 2008, General Classification of Economic Activities - Structure. Technical
    report, Federal Statistical Office, Neuchatel, 2008,
    https://www.bfs.admin.ch/bfs/en/home/statistics/industry-services/nomenclatures/noga/publications-noga-2008.assetdetail.344622.html
    """
    df_zp["business_sector_agriculture"] = np.where(
        (1 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 7), 1, 0
    )
    df_zp["business_sector_other_services"] = np.where(
        ((86 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 90))
        | ((92 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 96))
        | (df_zp["noga_08"] == 59)
        | (df_zp["noga_08"] == 68),
        1,
        0,
    )
    df_zp["business_sector_others"] = np.where(
        (97 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 98), 1, 0
    )
    df_zp["business_sector_finance"] = np.where(
        (64 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 67), 1, 0
    )

    df_zp["business_sector_retail"] = np.where(df_zp["noga_08"] == 47, 1, 0)
    df_zp["business_sector_gastronomy"] = np.where(
        (55 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 56), 1, 0
    )
    df_zp["business_sector_production"] = np.where(
        ((10 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 35))
        | ((41 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 43)),
        1,
        0,
    )
    df_zp["business_sector_wholesale"] = np.where(
        ((45 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 46))
        | ((49 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 53)),
        1,
        0,
    )
    df_zp["business_sector_services_fc"] = np.where(
        ((60 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 63))
        | ((69 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 82))
        | (df_zp["noga_08"] == 58),
        1,
        0,
    )
    df_zp["business_sector_non_movers"] = np.where(
        ((8 <= df_zp["noga_08"]) & (df_zp["noga_08"] <= 9))
        | (df_zp["noga_08"] == 84)
        | (df_zp["noga_08"] == 85)
        | (df_zp["noga_08"] == 91)
        | (df_zp["noga_08"] == 99),
        1,
        0,
    )

    """ Deal with work percentage higher than 100 in MTMC (and not in SynPop):
     The sum of the work percentage can be higher than 100 in the Mobility and Transport Microcensus 2015,
     when people declare two part time jobs or more.
     It is not the case in the synthetic population, by definition.
     Therefore, the work percentage has been fixed to 100 when it was higher than 100 for the estimation of the model.
     """
    if year == 2015:
        df_zp["work_percentage"] = np.minimum(
            (df_zp["full_part_time_job"] == 1) * 100
            + df_zp["percentage_first_part_time_job"]
            * (df_zp["percentage_first_part_time_job"] > 0)
            + df_zp["percentage_second_part_time_job"]
            * (df_zp["percentage_second_part_time_job"] > 0),
            100,
        )
        del df_zp["full_part_time_job"]
        del df_zp["percentage_first_part_time_job"]
        del df_zp["percentage_second_part_time_job"]
    elif (year == 2020) | (year == 2021):
        """In the Mobility and Transport Microcensus 2020 and 2021, there is no information about several jobs anymore.
        However, there are still values higher than 100% (up to 150%). As for 2015, we define a maximum of 100."""
        df_zp["work_percentage"] = np.minimum(df_zp["percentage_part_time_job"], 100)
        del df_zp["percentage_part_time_job"]

    """ Code the aggregate level of education """
    if year == 2015:
        df_zp["no_post_school_educ"] = np.where(
            (df_zp["highest_educ"] == 1)
            | (df_zp["highest_educ"] == 2)
            | (df_zp["highest_educ"] == 3)
            | (df_zp["highest_educ"] == 4),
            1,
            0,
        )
        df_zp["secondary_education"] = np.where(
            (df_zp["highest_educ"] == 5)
            | (df_zp["highest_educ"] == 6)
            | (df_zp["highest_educ"] == 7)
            | (df_zp["highest_educ"] == 8)
            | (df_zp["highest_educ"] == 9)
            | (df_zp["highest_educ"] == 10)
            | (df_zp["highest_educ"] == 11)
            | (df_zp["highest_educ"] == 12),
            1,
            0,
        )
        df_zp["tertiary_education"] = np.where(
            (df_zp["highest_educ"] == 13)
            | (df_zp["highest_educ"] == 14)
            | (df_zp["highest_educ"] == 15)
            | (df_zp["highest_educ"] == 16),
            1,
            0,
        )
        df_zp["university"] = np.where(
            (df_zp["highest_educ"] == 17)
            | (df_zp["highest_educ"] == 18)
            | (df_zp["highest_educ"] == 19),
            1,
            0,
        )
    elif (year == 2020) | (year == 2021):
        df_zp["no_post_school_educ"] = np.where(
            (df_zp["highest_educ"] == 1) | (df_zp["highest_educ"] == 2), 1, 0
        )
        df_zp["secondary_education"] = np.where(
            (df_zp["highest_educ"] == 3)
            | (df_zp["highest_educ"] == 4)
            | (df_zp["highest_educ"] == 5),
            1,
            0,
        )
        df_zp["tertiary_education"] = np.where(
            (df_zp["highest_educ"] == 6) | (df_zp["highest_educ"] == 7), 1, 0
        )
        df_zp["university"] = np.where(
            (df_zp["highest_educ"] == 8) | (df_zp["highest_educ"] == 9), 1, 0
        )

    # Define a binary variable: studying or not
    df_zp = add_is_studying(df_zp)

    """ Add home-work distance from SIMBA MOBi """
    df_zp = add_home_work_distance(df_zp, path_to_mobi_zones, path_to_skim_file)

    """ Test that no column contains NA values """
    for column in df_zp.columns:
        if df_zp[column].isna().any():
            print("There are NA values in column", column)
    """ Save the file, for manual check if needed """
    # df_zp.to_csv(path_to_output_data_file, sep=";", index=False)
    return df_zp


def add_is_studying(df_zp: pd.DataFrame) -> pd.DataFrame:
    """The variable has the following values:
    1: is studying
    0: is not studying
    The definition of someone studying is as follows:
    - Not an apprentice
    - Strictly older than 18
    - Has mentioned "studying" as an activity in one question about the side activity apart form work or in general
    - The person has (already) finished at least high school and can be admitted in a university
    Note that the apprentices have not been asked about work from home in the Mobility and Transport Microcensus.
    They are consequently not considered in this model, since the choice variable, telecommuting, is not defined.
    :param df_zp: the file with one person per row, without studying information
    :return: df_zp with studying information
    """
    df_zp["is_studying"] = 0
    df_zp.loc[
        (df_zp["age"] > 18)
        & (df_zp["work_position"] != 3)  # by definition, students are older than 18
        & (  # we take apprentices out, even if it does not change anything at the end
            (df_zp["other_activities_if_working1"] == 32)
            | (df_zp["other_activities_if_working2"] == 32)
            | (df_zp["other_activities_if_working3"] == 32)
            | (df_zp["activity_status_if_not_working1"] == 32)
            | (  # People not working don't answer about...
                df_zp["activity_status_if_not_working2"] == 32
            )
            | (  # ... work from home, so these three lines is not...
                df_zp["activity_status_if_not_working3"] == 32
            )
        )
        & (  # really useful.
            df_zp["highest_educ"].isin([10, 11, 12, 14, 15, 16, 17, 18, 19])
        ),
        "is_studying",
    ] = 1  # WHY NOT 13???
    df_zp.drop(
        [
            "other_activities_if_working1",
            "other_activities_if_working2",
            "other_activities_if_working3",
            "activity_status_if_not_working1",
            "activity_status_if_not_working2",
            "activity_status_if_not_working3",
        ],
        axis=1,
        inplace=True,
    )
    return df_zp


def add_number_of_driving_licence(
    df_zp: pd.DataFrame, df_hhp: pd.DataFrame
) -> pd.DataFrame:
    hh_driving_licence = df_hhp[df_hhp.f20400a == 1]
    nb_driving_licence_per_hh = (
        hh_driving_licence.groupby(by="HHNR")
        .count()
        .reset_index()[["HHNR", "alter"]]
        .rename(columns={"alter": "nb_driving_licences"})
    )
    df_zp = df_zp.merge(nb_driving_licence_per_hh, on="HHNR", how="left")
    df_zp["nb_driving_licences"].fillna(0, inplace=True)
    return df_zp


def add_number_of_children(
    df_zp: pd.DataFrame, df_hhp: pd.DataFrame, age_limit: int
) -> pd.DataFrame:
    name_of_new_variable = "number_of_children_less_than_" + str(age_limit)
    """ Let first count the number of members of the household younger than [age_limit] """
    df_hhp["less_than_x"] = df_hhp.apply(
        lambda x: 1 if x["alter"] <= age_limit else 0, axis=1
    )
    df_hhp_less_than_x_per_hh = df_hhp[["HHNR", "less_than_x"]].groupby(["HHNR"]).sum()
    df_zp = pd.merge(
        df_zp, df_hhp_less_than_x_per_hh, left_on="HHNR", right_on="HHNR", how="left"
    )
    """ Two cases of household structure: couples with children or single parent with children at home """
    df_zp[name_of_new_variable] = 0
    # Case "couples with children"
    df_zp.loc[df_zp.hhtyp == 220, name_of_new_variable] = df_zp[
        ["hhgr", "less_than_x"]
    ].apply(lambda x: min(x[0] - 2, x[1]), axis=1)
    # Case "single parents"
    df_zp.loc[df_zp.hhtyp == 230, name_of_new_variable] = df_zp[
        ["hhgr", "less_than_x"]
    ].apply(lambda x: min(x[0] - 1, x[1]), axis=1)

    # Special case: the age of household members are not well known
    unknown_age_in_hh = df_hhp[df_hhp["alter"] < 0]["HHNR"].unique()
    df_zp.loc[df_zp["HHNR"].isin(unknown_age_in_hh), name_of_new_variable] = -999
    del df_zp["less_than_x"]
    return df_zp


def add_accessibility(
    df_zp: pd.DataFrame, path_to_mobi_zones: Path, path_to_npvm_zones: Path
) -> pd.DataFrame:
    """Add traffic zones IDs for home location"""
    df_zp = geopandas.GeoDataFrame(
        df_zp, geometry=geopandas.points_from_xy(df_zp.W_X, df_zp.W_Y), crs="epsg:4326"
    )
    df_zp.to_crs(epsg=2056, inplace=True)
    # Read the Geopackage file containing the zones. Proj: 2056, CH1903+
    df_zones = geopandas.read_file(path_to_npvm_zones)
    df_zp = geopandas.sjoin(
        df_zp, df_zones[["zone_id", "geometry"]], how="left", predicate="intersects"
    )
    df_zp["zone_id"].fillna(-999, inplace=True)
    # Rename the column with the zone ID
    df_zp.rename(columns={"zone_id": "zone_id_home"}, inplace=True)

    """ Add accessibility for home location """
    path_to_mobi_zones_csv = path_to_mobi_zones / "mobi-zones.csv"
    with open(path_to_mobi_zones_csv, "r", encoding="latin1") as accessibility_file:
        df_accessibility = pd.read_csv(
            accessibility_file,
            sep=";",
            usecols=["zone_id", "accsib_car", "accsib_mul", "accsib_pt"],
        )
    df_zp = pd.merge(
        df_zp, df_accessibility, left_on="zone_id_home", right_on="zone_id", how="left"
    )
    df_zp.rename(
        columns={
            "accsib_car": "accsib_car_home",
            "accsib_mul": "accsib_mul_home",
            "accsib_pt": "accsib_pt_home",
        },
        inplace=True,
    )
    del df_zp["zone_id"]
    del df_zp["index_right"]

    """ Add traffic zones IDs for work location """
    df_zp_with_work_coord = df_zp[(df_zp.A_X != -999) & (df_zp.A_X != -997)]
    df_zp_with_work_coord = geopandas.GeoDataFrame(
        df_zp_with_work_coord,
        geometry=geopandas.points_from_xy(
            df_zp_with_work_coord.A_X, df_zp_with_work_coord.A_Y
        ),
        crs="epsg:4326",
    )
    df_zp_with_work_coord.to_crs(epsg=2056, inplace=True)
    df_zp_with_work_coord = geopandas.sjoin(
        df_zp_with_work_coord,
        df_zones[["zone_id", "geometry"]],
        how="left",
        predicate="intersects",
    )
    # Rename the column with the zone ID
    df_zp_with_work_coord.rename(columns={"zone_id": "zone_id_work"}, inplace=True)
    df_zp_with_work_coord["zone_id_work"].fillna(-999, inplace=True)
    df_zp.loc[df_zp.A_X != -999, "zone_id_work"] = df_zp_with_work_coord["zone_id_work"]
    df_zp["zone_id_work"].fillna(-999, inplace=True)

    df_zp = pd.merge(
        df_zp, df_accessibility, left_on="zone_id_work", right_on="zone_id", how="left"
    )
    df_zp.rename(
        columns={
            "accsib_car": "accsib_car_work",
            "accsib_mul": "accsib_mul_work",
            "accsib_pt": "accsib_pt_work",
        },
        inplace=True,
    )
    df_zp["accsib_car_work"].fillna(-999, inplace=True)
    df_zp["accsib_mul_work"].fillna(-999, inplace=True)
    df_zp["accsib_pt_work"].fillna(-999, inplace=True)
    del df_zp["geometry"]
    del df_zp["zone_id"]
    return df_zp


def add_public_transport_connection_quality(
    df_zp: pd.DataFrame, year: int
) -> pd.DataFrame:
    """Add public transport connection quality of the work place"""
    df_zp_with_work_coord = df_zp[df_zp.A_X != -997]
    df_zp_with_work_coord = geopandas.GeoDataFrame(
        df_zp_with_work_coord,
        geometry=geopandas.points_from_xy(
            df_zp_with_work_coord.A_X, df_zp_with_work_coord.A_Y
        ),
        crs="epsg:4326",
    )
    df_zp_with_work_coord.to_crs(epsg=2056, inplace=True)
    # Read the shape file containing the connection quality
    if year == 2015:
        connection_quality_folder_path = Path(
            "../data/input/OeV_Gueteklassen/gueteklassen_oev_2015_2056.gpkg/"
        )
    elif year == 2020:
        connection_quality_folder_path = Path(
            "../data/input/OeV_Gueteklassen/gueteklassen_oev_2020_2056.gpkg/"
        )
    elif year == 2021:
        connection_quality_folder_path = Path(
            "../data/input/OeV_Gueteklassen/gueteklassen_oev_2021_2056.gpkg/"
        )
    else:
        raise ValueError("Year not well defined!")
    df_connection_quality = geopandas.read_file(
        connection_quality_folder_path / "OeV_Gueteklassen_ARE.gpkg"
    )
    df_zp_with_work_coord = geopandas.sjoin(
        df_zp_with_work_coord,
        df_connection_quality[["Klasse", "geometry"]],
        how="left",
        predicate="intersects",
    )
    df_zp_with_work_coord["Klasse"] = df_zp_with_work_coord["Klasse"].map(
        {"A": 1, "B": 2, "C": 3, "D": 4}
    )
    df_zp_with_work_coord["Klasse"].fillna("5", inplace=True)
    df_zp.loc[df_zp.A_X != -997, "Klasse"] = df_zp_with_work_coord["Klasse"]
    df_zp.loc[df_zp.A_X == -997, "Klasse"] = -999
    # Rename the column with the public transport connection quality
    df_zp.rename(
        columns={"Klasse": "public_transport_connection_quality_ARE_work"}, inplace=True
    )
    return df_zp


def add_home_work_distance(
    df_zp: pd.DataFrame, path_to_mobi_zones: Path, path_to_skim_file: Path
) -> pd.DataFrame:
    df_zp_with_work_coord = df_zp[["HHNR", "zone_id_home", "zone_id_work"]]
    df_zp_with_work_coord = df_zp_with_work_coord[
        df_zp_with_work_coord.zone_id_work != -999
    ]

    # Open skim file
    skims = omx.open_file(path_to_skim_file / "skims.omx", "r")
    # Load car network distance matrix as numpy array
    car_network_distance_matrix = np.array(skims["12"])

    """ Get MOBi traffic zones """
    path_to_mobi_zones_shp = path_to_mobi_zones / "mobi-zones.shp"
    # Important: zone_ids must be in ascending order
    mobi_zones = geopandas.read_file(path_to_mobi_zones_shp).sort_values("zone_id")
    mobi_zones.crs = "EPSG:2056"

    """ Get matrix value for origin-destination pairs """
    # We need a mapping "zone ID" to "position of the zone" to read the matrix value
    zone_id_to_zone_index = dict(
        zip(mobi_zones["zone_id"], range(len(mobi_zones["zone_id"])))
    )
    df_zp_with_work_coord["o_ind_temp"] = df_zp_with_work_coord["zone_id_home"].map(
        zone_id_to_zone_index
    )
    df_zp_with_work_coord["d_ind_temp"] = df_zp_with_work_coord["zone_id_work"].map(
        zone_id_to_zone_index
    )
    # Read matrix value
    df_zp_with_work_coord["car_network_distance"] = car_network_distance_matrix[
        df_zp_with_work_coord["o_ind_temp"], df_zp_with_work_coord["d_ind_temp"]
    ]
    # work_car_distances = df_zp_with_work_coord[
    #     [c for c in df_zp_with_work_coord.columns if c not in ['o_ind_temp', 'd_ind_temp']]]

    skims.close()
    df_zp_with_work_coord.drop(
        ["zone_id_home", "zone_id_work", "o_ind_temp", "d_ind_temp"],
        axis=1,
        inplace=True,
    )

    """ Put data back in df_zp """
    df_zp = pd.merge(df_zp, df_zp_with_work_coord, on="HHNR", how="left")

    df_zp["car_network_distance"].fillna(-999, inplace=True)

    df_zp.drop(["A_Y", "A_X"], axis=1, inplace=True)

    return df_zp


def add_home_work_crow_fly_distance(df_zp: pd.DataFrame) -> pd.DataFrame:
    """Add the distance between home and work places"""
    coding_with_coordinates = (df_zp.A_X != -999) & (df_zp.A_X != -997)
    job_in_switzerland = (df_zp.A_BFS != -99) & (df_zp.A_BFS != -97)
    df_zp_with_work_coordinates = df_zp[coding_with_coordinates & job_in_switzerland]
    geodf_home = geopandas.GeoDataFrame(
        df_zp_with_work_coordinates,
        geometry=geopandas.points_from_xy(
            df_zp_with_work_coordinates.W_X, df_zp_with_work_coordinates.W_Y
        ),
        crs="epsg:4326",
    )
    geodf_home.to_crs(epsg=2056, inplace=True)
    geodf_home = geodf_home.copy()
    geodf_work = geopandas.GeoDataFrame(
        df_zp_with_work_coordinates,
        geometry=geopandas.points_from_xy(
            df_zp_with_work_coordinates.A_X, df_zp_with_work_coordinates.A_Y
        ),
        crs="epsg:4326",
    )
    geodf_work.to_crs(epsg=2056, inplace=True)
    df_zp.loc[
        coding_with_coordinates & job_in_switzerland, "home_work_crow_fly_distance"
    ] = geodf_home.distance(geodf_work)
    df_zp["home_work_crow_fly_distance"].fillna(-999, inplace=True)
    df_zp.drop(["W_Y", "W_X"], axis=1, inplace=True)
    return df_zp


def add_spatial_typology(
    df_zp: pd.DataFrame, year: int, path_to_typology: Path
) -> pd.DataFrame:
    """Add the data about the spatial typology of the home address (in particular the home commune)"""
    if year == 2015:
        path_to_typology = path_to_typology / "2015/Raumgliederungen.xlsx"
        spatial_typology_variable_name = "Städtische / Ländliche Gebiete"
    elif year == 2020:
        path_to_typology = path_to_typology / "2020/Raumgliederungen.xlsx"
        spatial_typology_variable_name = "Städtische / Ländliche Gebiete"
    elif year == 2021:
        path_to_typology = path_to_typology / "2021/Raumgliederungen.xlsx"
        spatial_typology_variable_name = "Städtische / Ländliche Gebiete"
    else:
        raise ValueError("Spatial typology is only available for 2015, 2020 and 2021!")
    df_typology = pd.read_excel(
        path_to_typology,
        sheet_name="Daten",
        skiprows=[
            0,
            2,
        ],  # Removes the 1st row, with information, and the 2nd, with links
        usecols="A,G",
    )  # Selects only the BFS commune number and the column with the typology
    df_zp = pd.merge(
        df_zp, df_typology, left_on="W_BFS", right_on="BFS Gde-nummer", how="left"
    )
    df_zp.drop("BFS Gde-nummer", axis=1, inplace=True)
    df_zp = df_zp.rename(
        columns={spatial_typology_variable_name: "urban_typology_home"}
    )

    """ Add the data about the spatial typology of the work address (in particular the work commune) """
    df_zp = pd.merge(
        df_zp, df_typology, left_on="A_BFS", right_on="BFS Gde-nummer", how="left"
    )
    df_zp.drop("BFS Gde-nummer", axis=1, inplace=True)
    df_zp = df_zp.rename(
        columns={spatial_typology_variable_name: "urban_typology_work"}
    )
    df_zp.urban_typology_work.fillna(-99, inplace=True)
    return df_zp


def generate_work_position(row) -> int:
    work_position = (
        0  # corresponds to "not employed" - nicht erwerbstaetig / in MTMC: -99
    )
    # in MTMC: 1 independent worker, "Selbstständig Erwerbende(r)",
    #          2 worker in a company owned by the person being interviewed,
    #            "Arbeitnehmer(in) in der AG oder GmbH, welche IHNEN selbst gehört",
    #          3 worker in a company owned by a member of the household,
    #            "Arbeitnehmer(in) im Familienbetrieb von einem Haushaltsmitglied"
    if (row["f40800_01"] == 1) | (row["f40800_01"] == 2) | (row["f40800_01"] == 3):
        work_position = 1  # corresponds to "independent worker"/"Selbststaendige"
    elif row["f40800_01"] == 4:  # in MTMC: employed in a private or public company
        # in MTMC: -98 no answer, "keine Antwort"
        #          -97 don't know, "weiss nicht"
        #            1 employee without executive function, "Angestellt ohne Cheffunktion"
        if (
            (row["f41100_01"] == 1)
            | (row["f41100_01"] == -98)
            | (row["f41100_01"] == -97)
        ):
            work_position = 2  # corresponds to "employee"/"Angestellte"
        # in MTMC: 2 employee with executive function and subordinate employees,
        #            "Angestellt mit Chefposition und unterstellten Mitarbeitern"
        #          3 members of the direction, CEOs,
        #            "Angestellt als Mitglied von der Direktion oder Geschäftsleitung"
        elif (row["f41100_01"] == 2) | (row["f41100_01"] == 3):
            work_position = 3  # corresponds to "cadres"
        else:
            raise Exception("There should not be other cases...")
    elif row["f40800_01"] == 5:  # in Mobility and Transport Microcensus: apprentice
        work_position = 2  # corresponds to "employee"/"Angestellte"
    return work_position


def define_mobility_resources_variable(row) -> int:
    """This is the version of the choice variable used for the generation of the synthetic population (SynPop)."""
    if row["car_avail"] == -98:  # no information about car availability
        return -98
    elif (
        row["car_avail"] == 1 or row["car_avail"] == 2
    ):  # car always available or available on demand
        if row["GA_ticket"] == 1:  # GA
            if row["halbtax_ticket"] == 1:
                # Warning: Person with car available, GA and HT are considered as "car + GA"
                return 1
            elif row["halbtax_ticket"] == 2:  # No HT
                return 1  # Auto + GA (no HT)
            else:
                return -98
        elif row["GA_ticket"] == 2:  # No GA
            if row["halbtax_ticket"] == 1:  # HT
                if row["Verbund_Abo"] == 1:
                    return 20  # Auto + HT + Verbundabo (no GA)
                elif row["Verbund_Abo"] == 2:
                    return 2  # Auto + HT (no GA, no Verbundabo)
                else:  # no info about Verbundabo
                    return -98
            elif row["halbtax_ticket"] == 2:  # No HT
                if row["Verbund_Abo"] == 1:
                    return 30  # Auto + Verbundabo (no GA, no HT)
                elif row["Verbund_Abo"] == 2:
                    return 3  # Car available (no GA, no Verbundabo, no HT)
                else:  # no info about Verbundabo
                    return -98
            else:  # no info about HT
                return -98
        else:  # no information about GA
            return -98
    # car not available, available on demand, or people younger than 18 or without driving license
    elif row["car_avail"] == 3 or row["car_avail"] == -99:
        if row["GA_ticket"] == 1:  # GA
            if row["halbtax_ticket"] == 1:
                # print 'Warning: person with GA and HT!'
                return 4
            # No HT or not available to people younger than 16
            elif row["halbtax_ticket"] == 2 or row["halbtax_ticket"] == -99:
                return 4  # GA (no HT)
            else:
                return -98
        elif row["GA_ticket"] == 2:  # No GA
            if row["halbtax_ticket"] == 1:  # HT
                if row["Verbund_Abo"] == 1:
                    return 50  # HT + Verbundabo (no GA)
                elif row["Verbund_Abo"] == 2:
                    return 5  # HT (no GA, no Verbundabo)
                else:  # no info about Verbundabo
                    return -98
            # No HT or not available to people younger than 16
            elif row["halbtax_ticket"] == 2 or row["halbtax_ticket"] == -99:
                if row["Verbund_Abo"] == 1:
                    return 60  # Verbundabo (no GA, no HT)
                elif row["Verbund_Abo"] == 2:
                    return 6  # Nothing (no GA, no Verbundabo, no HT)
                else:  # no info about Verbundabo
                    return -98
            else:  # no info about HT
                return -98
        else:  # no information about GA
            return -98
    elif (
        row["car_avail"] == -98 or row["car_avail"] == -97
    ):  # no answer or does not know
        return -98
