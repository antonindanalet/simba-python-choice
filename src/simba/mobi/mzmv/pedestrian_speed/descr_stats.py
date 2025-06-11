from typing import List
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd

from simba.mobi.mzmv.config import path_to_mtmc_data
from simba.mobi.mzmv.pedestrian_speed.utils import get_and_filter_etappen
from simba.mobi.mzmv.pedestrian_speed.utils import get_and_filter_walk_etappen
from simba.mobi.mzmv.pedestrian_speed.utils import get_hours_as_text
from simba.mobi.mzmv.utils2015.compute_confidence_interval import (
    get_weighted_avg_and_std,
)
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_hh
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_trips_in_switzerland
from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_zp


def run_pedestrian_descr_stats(year: int) -> None:
    results_for_full_population(year)
    results_by_type_of_trip(year)
    results_by_age(year)
    results_by_purpose(year)
    results_by_daytime(year)
    results_sprache(year)
    results_region(year)
    results_urban_rural(year)


def results_urban_rural(year: int) -> None:

    selected_columns_etappen = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
    ]
    walk_etappen = get_and_filter_walk_etappen(year, selected_columns_etappen)

    selected_columns_households = ["HHNR", "W_stadt_land_2012"]
    households = get_hh(year, path_to_mtmc_data, selected_columns_households)
    walk_etappen = pd.merge(walk_etappen, households, on="HHNR", how="left")

    list_urban_rural: List[str] = []
    list_speeds_per_hour = []
    list_errors = []

    for region_code, region_name in [[1, "Urban"], [2, "Intermediary"], [3, "Rural"]]:
        walk_etappen_region = walk_etappen.loc[
            walk_etappen["W_stadt_land_2012"] == region_code, :
        ]
        avg, std = sum_and_average(walk_etappen_region)
        print(f"Average speed, {region_name}: {avg:.2f} (+/- {std:.2f})")
        list_urban_rural.append(str(region_name))
        list_speeds_per_hour.append(avg)
        list_errors.append(std)

    plt.bar(
        list_urban_rural,
        list_speeds_per_hour,
        yerr=list_errors,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)
    # Add a title and labels
    plt.title("Pedestrian speed by urban typology")
    plt.ylabel("Speed (km/h)")

    plt.tight_layout()  # Adjust layout to ensure labels are not cut off

    # Show the plot
    plt.savefig("speed_by_urban_typology.png")
    plt.clf()


def results_region(year: int) -> None:
    selected_columns_etappen = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
    ]
    walk_etappen = get_and_filter_walk_etappen(year, selected_columns_etappen)

    selected_columns_households = ["HHNR", "W_REGION"]
    households = get_hh(year, path_to_mtmc_data, selected_columns_households)
    walk_etappen = pd.merge(walk_etappen, households, on="HHNR", how="left")

    list_region: List[str] = []
    list_speeds_per_hour = []
    list_errors = []

    for region_code, region_name in [
        [1, "Région lémanique"],
        [2, "Espace Mittelland"],
        [3, "Nordwestschweiz"],
        [4, "Zürich"],
        [5, "Ostschweiz"],
        [6, "Zentralschweiz"],
        [7, "Ticino"],
    ]:
        walk_etappen_region = walk_etappen.loc[
            walk_etappen["W_REGION"] == region_code, :
        ]
        avg, std = sum_and_average(walk_etappen_region)
        print(f"Average speed, {region_name}: {avg:.2f} (+/- {std:.2f})")
        list_region.append(str(region_name))
        list_speeds_per_hour.append(avg)
        list_errors.append(std)

    plt.bar(
        list_region,
        list_speeds_per_hour,
        yerr=list_errors,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)
    # Add a title and labels
    plt.title("Pedestrian speed by region")
    plt.xlabel("Region")
    plt.ylabel("Speed (km/h)")

    plt.tight_layout()  # Adjust layout to ensure labels are not cut off

    # Show the plot
    plt.savefig("speed_by_region.png")
    plt.clf()


def results_sprache(year: int) -> None:
    selected_columns_etappen = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
    ]
    walk_etappen = get_and_filter_walk_etappen(year, selected_columns_etappen)

    selected_columns_households = ["HHNR", "sprache"]
    households = get_hh(year, path_to_mtmc_data, selected_columns_households)
    walk_etappen = pd.merge(walk_etappen, households, on="HHNR", how="left")

    list_language = []
    list_speeds_per_hour = []
    list_errors = []

    walk_etappen_german = walk_etappen.loc[walk_etappen["sprache"] == 1, :]
    language = "German"
    avg, std = sum_and_average(walk_etappen_german)
    print(f"Average speed, {language}: {avg:.2f} (+/- {std:.2f})")
    list_language.append(language)
    list_speeds_per_hour.append(avg)
    list_errors.append(std)

    walk_etappen_german = walk_etappen.loc[walk_etappen["sprache"] == 2, :]
    language = "French"
    avg, std = sum_and_average(walk_etappen_german)
    print(f"Average speed, {language}: {avg:.2f} (+/- {std:.2f})")

    walk_etappen_german = walk_etappen.loc[walk_etappen["sprache"] == 3, :]
    language = "Italian"
    avg, std = sum_and_average(walk_etappen_german)
    print(f"Average speed, {language}: {avg:.2f} (+/- {std:.2f})")

    walk_etappen_german = walk_etappen.loc[walk_etappen["sprache"] != 1, :]
    language = "Not German"
    avg, std = sum_and_average(walk_etappen_german)
    print(f"Average speed, {language}: {avg:.2f} (+/- {std:.2f})")
    list_language.append(language)
    list_speeds_per_hour.append(avg)
    list_errors.append(std)

    plt.bar(
        list_language,
        list_speeds_per_hour,
        yerr=list_errors,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)
    # Add a title and labels
    plt.title("Pedestrian speed by language")
    plt.xlabel("Language")
    plt.ylabel("Speed (km/h)")

    plt.tight_layout()  # Adjust layout to ensure labels are not cut off

    # Show the plot
    plt.savefig("speed_by_language.png")
    plt.clf()


def results_by_daytime(year: int) -> None:
    selected_columns_etappen = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
        "f51100",  # Departure time (in minute after midnight)
        "f51400",  # Arrival time (in minute after midnight)
    ]
    walk_etappen = get_and_filter_walk_etappen(year, selected_columns_etappen)

    list_hours_as_text = []
    list_speeds_per_hour = []
    list_errors = []
    for lower_bound_interval in range(1, 24 * 60, 60 * 3):
        upper_bound_interval = lower_bound_interval + 60 * 3
        walk_etappen_time_interval = walk_etappen.loc[
            (walk_etappen["f51100"] >= lower_bound_interval)
            & (walk_etappen["f51100"] < upper_bound_interval),
            :,
        ]
        hours_as_text = get_hours_as_text(lower_bound_interval, upper_bound_interval)
        avg, std = sum_and_average(walk_etappen_time_interval)
        # print(f"Average speed, {hours_as_text}: {avg:.2f} (+/- {std:.2f})")
        list_hours_as_text.append(hours_as_text)
        list_speeds_per_hour.append(avg)
        list_errors.append(std)

    plt.bar(
        list_hours_as_text,
        list_speeds_per_hour,
        yerr=list_errors,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)
    # Add a title and labels
    plt.title("Pedestrian speed by time of day")
    plt.xlabel("Time of day")
    plt.ylabel("Speed (km/h)")

    # Show the plot
    plt.savefig("speed_by_time_of_day.png")
    plt.clf()

    # 0-5
    for lower_bound_interval, time_interval_in_hours in [
        [1, 5],
        [5, 3],
        [8, 1],
        [9, 2],
        [11, 2],
        [13, 1],
        [14, 1],
        [15, 1],
        [16, 1],
        [17, 7],
    ]:
        if lower_bound_interval != 1:
            lower_bound_interval = lower_bound_interval * 60 + 1
        upper_bound_interval = lower_bound_interval + 60 * time_interval_in_hours
        hours_as_text = get_hours_as_text(lower_bound_interval, upper_bound_interval)
        walk_etappen_time_interval = walk_etappen.loc[
            (walk_etappen["f51100"] >= lower_bound_interval)
            & (walk_etappen["f51100"] < upper_bound_interval),
            :,
        ]
        avg, std = sum_and_average(walk_etappen_time_interval)
        print(f"Average speed, {hours_as_text}: {avg:.2f} (+/- {std:.2f})")


def results_by_purpose(year: int) -> None:
    selected_columns_etappen = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
        "WEGNR",  # for merging with the trip dataset
    ]
    walk_etappen = get_and_filter_walk_etappen(year, selected_columns_etappen)

    selected_columns_trips = ["HHNR", "WEGNR", "wzweck1"]
    df_trips = get_trips_in_switzerland(year, path_to_mtmc_data, selected_columns_trips)
    walk_etappen = pd.merge(walk_etappen, df_trips, on=["HHNR", "WEGNR"], how="left")

    list_purpose: List[str] = []
    list_avg = []
    list_std = []

    for purpose_code, purpose_name in [
        [2, "work"],
        [3, "education"],
        [4, "shopping"],
        [8, "leisure"],
    ]:
        walk_etappen_purpose = walk_etappen.loc[
            walk_etappen["wzweck1"] == purpose_code, :
        ]
        avg, std = sum_and_average(walk_etappen_purpose)
        print(f"Average speed, {purpose_name}: {avg:.2f} (+/- {std:.2f})")
        if (purpose_code == 4) | (purpose_code == 8):
            list_purpose.append(str(purpose_name))
            list_avg.append(avg)
            list_std.append(std)

    walk_etappen_work_education = walk_etappen.loc[
        (walk_etappen["wzweck1"] == 2) | (walk_etappen["wzweck1"] == 3), :
    ]
    avg, std = sum_and_average(walk_etappen_work_education)
    purpose_name = "work & education"
    print(f"Average speed, {purpose_name}: {avg:.2f} (+/- {std:.2f})")
    list_purpose.append(purpose_name)
    list_avg.append(avg)
    list_std.append(std)

    plt.bar(
        list_purpose,
        list_avg,
        yerr=list_std,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)
    # Add a title and labels
    plt.title("Pedestrian speed by age category")
    plt.xlabel("Age category")
    plt.ylabel("Speed (km/h)")
    plt.tight_layout()  # Adjust layout to ensure labels are not cut off

    plt.savefig("speed_by_purpose.png")
    plt.clf()


def results_by_age(year: int) -> None:
    walk_etappen = get_and_filter_walk_etappen(
        year,
        selected_columns=[
            "f51300",  # transport mode
            "HHNR",
            "E_Ausland",  # Is abroad or not
            "rdist",  # distance
            "e_dauer",  # duration
            "WP",  # weights
            "WEGNR",  # for merging with the trip dataset
        ],
    )
    df_persons = get_zp(year, path_to_mtmc_data, selected_columns=["HHNR", "alter"])
    walk_etappen = pd.merge(walk_etappen, df_persons, on="HHNR", how="left")

    list_age_category = []
    list_avg = []
    list_std = []

    for upper_bound_age in [17, 24]:
        walk_etappen_age_category = walk_etappen.loc[
            walk_etappen["alter"] <= upper_bound_age, :
        ]
        avg, std = sum_and_average(walk_etappen_age_category)
        age_category = f"6-{upper_bound_age} old"
        print(f"Average speed, {age_category}: {avg:.2f} (+/- {std:.2f})")
        if upper_bound_age == 24:
            list_age_category.append(age_category)
            list_avg.append(avg)
            list_std.append(std)

    for lower_age, upper_age in [[18, 24], [25, 64], [65, 74]]:
        walk_etappen_age_category = walk_etappen.loc[
            (walk_etappen["alter"] >= lower_age) & (walk_etappen["alter"] <= upper_age),
            :,
        ]
        avg, std = sum_and_average(walk_etappen_age_category)
        age_category = f"{lower_age}-{upper_age} old"
        print(f"Average speed, {age_category}: {avg:.2f} (+/- {std:.2f})")
        if ((lower_age == 25) and (upper_age == 64)) | (
            (lower_age == 65) and (upper_age == 74)
        ):
            list_age_category.append(age_category)
            list_avg.append(avg)
            list_std.append(std)

    walk_etappen_75plus = walk_etappen.loc[walk_etappen["alter"] >= 75, :]
    avg, std = sum_and_average(walk_etappen_75plus)
    age_category = "75+ old"
    print(f"Average speed, {age_category}: {avg:.2f} (+/- {std:.2f})")
    list_age_category.append(age_category)
    list_avg.append(avg)
    list_std.append(std)

    plt.bar(
        list_age_category,
        list_avg,
        yerr=list_std,
        capsize=5,
        color="skyblue",
        edgecolor="black",
    )
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)
    # Add a title and labels
    plt.title("Pedestrian speed by age category")
    plt.xlabel("Age category")
    plt.ylabel("Speed (km/h)")
    plt.tight_layout()  # Adjust layout to ensure labels are not cut off

    plt.savefig("speed_by_age.png")
    plt.clf()


def results_by_type_of_trip(year: int) -> None:
    """
    This function calculates the average walking speed among different types of trips,
    prints the results, and then creates a bar plot (with error bars) of the speeds.
    """

    # Retrieve and merge data
    walk_etappen = get_and_filter_walk_etappen(
        year,
        selected_columns=[
            "f51300",  # transport mode
            "HHNR",
            "E_Ausland",  # abroad indicator
            "rdist",  # distance
            "e_dauer",  # duration
            "WP",  # weights
            "WEGNR",  # merging key
        ],
    )

    df_trips = get_trips_in_switzerland(
        year,
        path_to_mtmc_data,
        selected_columns=[
            "HHNR",
            "WEGNR",
            "wmittel1",  # main transport mode (hierarchical)
            "wmittel1a",  # aggregated main transport mode
            "w_etappen",  # number of "Etappen" in the trip
        ],
    )

    # Merge walk_etappen data with trip data
    walk_etappen = pd.merge(walk_etappen, df_trips, on=["HHNR", "WEGNR"], how="left")

    # Lists to record results for certain trip types (for plotting)
    trip_types = []
    speeds = []
    errors = []

    # A helper function to calculate and print the average speed.
    def calc_and_print(
        df: pd.DataFrame, trip_description: str, include_in_plot: bool = False
    ) -> tuple[float, float]:
        """
        Computes average and standard deviation using sum_and_average() on the provided dataframe.
        Prints the results and, if include_in_plot is True, appends the results to the plot lists.
        Returns the average and standard deviation.
        """
        avg, std = sum_and_average(df)
        print(f"Average speed, {trip_description}: {avg:.2f} (+/- {std:.2f})")
        if include_in_plot:
            trip_types.append(trip_description)
            speeds.append(avg)
            errors.append(std)
        return avg, std

    # 1. Pure walk trips: 100% walking, trip with more than one segment,
    #    and with hierarchical transport mode=16.
    walk_trips = walk_etappen.loc[
        (walk_etappen["wmittel1"] == 16) & (walk_etappen["w_etappen"] > 1)
    ]
    calc_and_print(walk_trips, "pure walk trips")

    # 2. Round trips: trips with exactly one segment.
    round_trips = walk_etappen.loc[walk_etappen["w_etappen"] == 1]
    calc_and_print(round_trips, "round trips")

    # 3. Trips by public transport: using aggregated transport mode indicator.
    pt_trips = walk_etappen.loc[walk_etappen["wmittel1a"] == 3]
    calc_and_print(pt_trips, "trips by public transport")

    # 4. Trips NOT by public transport.
    non_pt_trips = walk_etappen.loc[walk_etappen["wmittel1a"] != 3]
    # Append these to the plotting lists.
    calc_and_print(non_pt_trips, "trips NOT by public transport", include_in_plot=True)

    # 5. Specific transport modes: "car" (code=8) and "train" (code=2)
    for mode_code, mode_name in ((8, "car"), (2, "train")):
        mode_trips = walk_etappen.loc[walk_etappen["wmittel1"] == mode_code]
        # Only include the train trips in the bar plot data.
        calc_and_print(
            mode_trips, f"trips by {mode_name}", include_in_plot=(mode_code == 2)
        )

    # 6. Non-train public transport: use trips by public transport that are not by train.
    non_train_pt = walk_etappen.loc[
        (walk_etappen["wmittel1a"] == 3) & (walk_etappen["wmittel1"] != 2)
    ]
    calc_and_print(
        non_train_pt, "trips by non-train public transport", include_in_plot=True
    )

    # Plotting the results for the subset of trip types recorded in the lists
    plt.figure(figsize=(8, 6))
    plt.bar(
        trip_types, speeds, yerr=errors, capsize=5, color="skyblue", edgecolor="black"
    )
    plt.xticks(rotation=45)
    plt.title("Pedestrian speed by type of trips")
    plt.xlabel("Type of trip")
    plt.ylabel("Speed (km/h)")
    plt.tight_layout()  # Adjust layout to ensure no parts are cut off

    plt.savefig("speed_by_trip_type.png")
    plt.clf()

    plt.figure(figsize=(8, 6))
    plt.bar(
        trip_types, speeds, yerr=errors, capsize=5, color="skyblue", edgecolor="black"
    )
    plt.xticks(rotation=45)
    plt.title("Pedestrian speed by type of trips")
    plt.xlabel("Type of trip")
    plt.ylabel("Speed (km/h)")
    plt.tight_layout()  # Adjust layout to ensure no parts are cut off

    plt.savefig("speed_by_trip_type.png")
    plt.clf()


def results_for_full_population(year: int) -> None:
    selected_columns = [
        "f51300",  # transport mode
        "HHNR",
        "E_Ausland",  # Is abroad or not
        "rdist",  # distance
        "e_dauer",  # duration
        "WP",  # weights
        "WEGNR",  # for merging with the trip datasets later, for detailed analysis
        "f51100",  # Departure time (minutes after midnight)
    ]
    df_etappen = get_and_filter_etappen(year, selected_columns)
    statistical_basis = len(
        df_etappen["HHNR"].unique()
    )  # Corresponds to the basis in the MTMC main report
    print("Basis:", statistical_basis, "people")
    walk_etappen = df_etappen.loc[df_etappen["f51300"] == 1, :]
    avg, std = sum_and_average(walk_etappen)
    print(f"Average speed: {avg}, (+/- {std})")


def sum_and_average(walk_etappen: pd.DataFrame) -> Tuple[float, float]:
    # We aggregate the distance and the travel times for each person and compute one speed per person
    # (which is then weighted per person with WP)
    sum_walk_etappen = (
        walk_etappen.groupby("HHNR")
        .agg({"rdist": "sum", "e_dauer": "sum", "WP": "first"})
        .reset_index()
    )
    sum_walk_etappen["speed"] = (
        sum_walk_etappen["rdist"] / sum_walk_etappen["e_dauer"] * 60
    )  # speed in km/h
    list_of_columns = ["speed"]
    dict_column_weighted_avg_and_std, _, _ = get_weighted_avg_and_std(
        sum_walk_etappen, weights="WP", list_of_columns=list_of_columns
    )
    avg = dict_column_weighted_avg_and_std["speed"][0]
    std = dict_column_weighted_avg_and_std["speed"][1]
    return avg, std


if __name__ == "__main__":
    YEAR = 2021
    run_pedestrian_descr_stats(YEAR)
