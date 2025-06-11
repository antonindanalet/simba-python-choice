from simba.mobi.mzmv.pedestrian_speed.descr_stats import run_pedestrian_descr_stats
from simba.mobi.mzmv.pedestrian_speed.run_pedestrian_regressions import (
    linear_regression_person,
)
from simba.mobi.mzmv.pedestrian_speed.run_pedestrian_regressions import (
    linear_regression_trip,
)


def run_pedestrian_speed() -> None:
    year = 2021
    run_pedestrian_descr_stats(year)
    linear_regression_trip(year)
    linear_regression_person(year)


if __name__ == "__main__":
    run_pedestrian_speed()
