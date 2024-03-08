from pathlib import Path

import biogeme.models as models
import numpy as np
from matplotlib import pyplot as plt


def descriptive_statistics(output_directory: Path) -> None:
    visualize_work_percentage(output_directory)
    visualize_accessibility(output_directory)


def visualize_accessibility(output_directory: Path) -> None:
    def f15(x_axis):
        return models.piecewiseFunction(x_axis, [0, 5, 10, 24], [0, -0.0419, 0.0847])

    def f21(x_axis):
        return models.piecewiseFunction(x_axis, [0, 5, 10, 24], [0, 0.0442, 0.0])

    x = np.arange(5, 24, 1)

    y21 = []
    for i in range(len(x)):
        y21.append(f21(x[i]))

    y15 = []
    for i in range(len(x)):
        y15.append(f15(x[i]))

    plt.plot(x, y21, c="red", ls="", ms=5, marker=".", label="2021")
    plt.plot(x, y15, c="green", ls="", ms=5, marker="*", label="2015+2020")
    plt.legend(loc="lower right")
    ax = plt.gca()
    plt.xlabel("Accessibility (* 100'000)")
    plt.ylabel("Nutzen")
    # ax.set_ylim([-1, 2])

    file_name = "effect_accessibility" + ".png"
    plt.savefig(output_directory / file_name)


def visualize_work_percentage(output_directory: Path) -> None:
    def f15(x_axis):
        return models.piecewiseFunction(x_axis, [0, 90, 101], [-0.0124, 0.0782])

    def f20(x_axis):
        return models.piecewiseFunction(x_axis, [0, 90, 101], [-0.00765, 0.0222])

    def f21(x_axis):
        return models.piecewiseFunction(x_axis, [0, 90, 101], [0.0, 0.0222])

    x = np.arange(0, 100, 1)

    y21 = []
    for i in range(len(x)):
        y21.append(f21(x[i]))

    y20 = []
    for i in range(len(x)):
        y20.append(f20(x[i]))

    y15 = []
    for i in range(len(x)):
        y15.append(f15(x[i]))

    plt.plot(x, y21, c="red", ls="", ms=5, marker=".", label="2021")
    plt.plot(x, y20, c="blue", ls="", ms=5, marker="*", label="2020")
    plt.plot(x, y15, c="green", ls="", ms=5, marker="*", label="2015")
    plt.legend(loc="lower right")
    ax = plt.gca()
    plt.xlabel("Alter")
    plt.ylabel("Nutzen")
    # ax.set_ylim([-1, 2])

    file_name = "effect_work_percentage" + ".png"
    plt.savefig(output_directory / file_name)
