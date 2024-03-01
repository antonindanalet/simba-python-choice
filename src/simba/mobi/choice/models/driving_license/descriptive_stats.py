from pathlib import Path

import biogeme
import biogeme.models as models
import matplotlib.pyplot as plt
import numpy as np


def visualize_cost(output_directory: Path) -> None:
    def f(x_values: float) -> float:
        b_parking_cost_car152021 = -0.764154648
        b_parking_cost_car_log152021 = 0.36403461
        b_free_parking_car152021 = -0.570982061
        free_parking_car15 = x_values == 0
        parking_cost_car_log15: float = np.log(x_values) if x_values != 0 else 0
        return (
            b_parking_cost_car152021 * x_values
            + b_parking_cost_car_log152021
            * (1 - free_parking_car15)
            * parking_cost_car_log15
            + b_free_parking_car152021 * free_parking_car15
        )

    x = np.arange(0, 3, 0.1)

    y = []
    for i in range(len(x)):
        y.append(f(x[i]))

    plt.plot(x, y, c="red", ls="", ms=5, marker=".")
    axis = plt.gca()
    plt.xlabel("Parkkosten")
    plt.ylabel("Nutzen")
    # axis.set_ylim([-1, 2])

    plt.savefig(output_directory / "cost.png")


def visualize_piecewise_age(output_directory: Path) -> None:
    def f21(x_values):
        return biogeme.models.piecewiseFunction(
            x_values,
            [0, 22.5, 26.5, 69.5, 89.5, 120],
            [0.45840336, 0.0, 0.018837082, -0.11493256, -0.19493779],
        )

    def f15(x_values):
        return biogeme.models.piecewiseFunction(
            x_values,
            [0, 22.5, 26.5, 69.5, 89.5, 120],
            [0.45840336, 0.112368703, 0.010294773, -0.124612248, -0.19493779],
        )

    x = np.arange(18, 90, 1)

    y21 = []
    for i in range(len(x)):
        y21.append(f21(x[i]))

    y15 = []
    for i in range(len(x)):
        y15.append(f15(x[i]))

    plt.plot(x, y21, c="red", ls="", ms=5, marker=".", label="2021")
    plt.plot(x, y15, c="blue", ls="", ms=5, marker="*", label="2015+2020")
    plt.legend(loc="lower right")
    ax = plt.gca()
    plt.xlabel("Alter")
    plt.ylabel("Nutzen")
    # ax.set_ylim([-1, 2])

    plt.savefig(output_directory / "piecewise_age.png")
