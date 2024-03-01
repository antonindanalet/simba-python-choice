from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


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
