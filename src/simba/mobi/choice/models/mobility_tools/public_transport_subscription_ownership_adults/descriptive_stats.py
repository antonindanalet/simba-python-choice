from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from simba.mobi.mzmv.utils_mtmc.get_mtmc_files import get_zp


def distribution_half_fare_regional_travelcards(path_to_mtmc: Path) -> None:
    for year in [2015, 2021]:
        if year == 2015:
            selected_columns = [
                "HHNR",
                "WP",
                "alter",
                "f41610b",  # Halbtax
                "f41610c",
            ]  # Verbundabo
        elif year == 2021:
            selected_columns = [
                "HHNR",
                "WP",
                "alter",
                "f41600_01b",  # Halbtax
                "f41600_01c",
            ]  # Verbundabo
        else:
            raise ValueError("Year not well defined! It must be 2015 or 2021...")
        df_zp = get_zp(year, path_to_mtmc, selected_columns=selected_columns)
        df_zp = df_zp.rename(
            columns={
                "f41610c": "Verbund_Abo",
                "f41610b": "halbtax_ticket",
                "f41600_01c": "Verbund_Abo",
                "f41600_01b": "halbtax_ticket",
            }
        )
        df_zp = df_zp.loc[df_zp.alter >= 18, :]  # Adults only
        df_zp = df_zp.loc[
            df_zp.Verbund_Abo >= 1, :
        ]  # Valid ansers only, regional tickets
        df_zp = df_zp.loc[
            df_zp.halbtax_ticket >= 1, :
        ]  # Valid ansers only, halfare tickets
        total = df_zp.WP.sum()
        df_zp = df_zp.loc[
            (df_zp.Verbund_Abo == 1) | (df_zp.halbtax_ticket == 1), :
        ]  # People with at least one abo
        nb_halfare_only = df_zp.loc[
            (df_zp.Verbund_Abo == 2) & (df_zp.halbtax_ticket == 1), "WP"
        ].sum()
        nb_regional_only = df_zp.loc[
            (df_zp.Verbund_Abo == 1) & (df_zp.halbtax_ticket == 2), "WP"
        ].sum()
        nb_both = df_zp.loc[
            (df_zp.Verbund_Abo == 1) & (df_zp.halbtax_ticket == 1), "WP"
        ].sum()
        subtotal = df_zp.WP.sum()
        print(year)
        print("Relative ratio of both:", nb_both / subtotal)
        print("Relative ratio of halfare only:", nb_halfare_only / subtotal)
        print("Relative ratio of regional only:", nb_regional_only / subtotal)
        print("Ratio of both in the total population:", nb_both / total)
        print("Ratio of halfare only in the total population:", nb_halfare_only / total)
        print(
            "Ratio of regional only in the total population:", nb_regional_only / total
        )
        tot_adult_pop = 7247286.3
        nb_both = tot_adult_pop * nb_both / total
        print(
            "Nb of halfare in the total population:",
            tot_adult_pop * nb_halfare_only / total + nb_both,
        )
        print(
            "Nb of regional in the total population:",
            tot_adult_pop * nb_regional_only / total + nb_both,
        )


def visualize_piecewise_age(output_directory: Path) -> None:
    x_axis_values_age = np.arange(18, 90, 1)

    y = []
    for i in range(len(x_axis_values_age)):
        y.append(f_piecewise(x_axis_values_age[i]))

    plt.plot(x_axis_values_age, y, c="red", ls="", ms=5, marker=".")
    ax = plt.gca()
    plt.xlabel("Alter")
    plt.ylabel("Nutzen")

    plt.savefig(output_directory / "fig_piecewise_age.png")


def f_piecewise(x_axis_values_age: np.ndarray) -> float:
    b_age_18_22_ga1521 = -0.095240029
    b_age_23_26_ga1521 = -0.327557888
    b_age_27_69_ga1521 = -0.006744077
    b_age_70_89_ga1521 = -0.033700028
    b_age_90_plus_ga1521 = -0.205749341

    return (
        b_age_18_22_ga1521 * max(0.0, min(x_axis_values_age, 22.5))
        + b_age_23_26_ga1521 * max(0.0, min((x_axis_values_age - 22.5), 4.0))
        + b_age_27_69_ga1521 * max(0.0, min((x_axis_values_age - 26.5), 43.0))
        + b_age_70_89_ga1521 * max(0.0, min((x_axis_values_age - 69.5), 20.0))
        + b_age_90_plus_ga1521 * max(0.0, min((x_axis_values_age - 89.5), 30.5))
    )
