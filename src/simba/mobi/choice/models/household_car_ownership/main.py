from pathlib import Path

from simba.mobi.choice.models.household_car_ownership.data_loader import get_data
from simba.mobi.choice.models.household_car_ownership.model_estimation import (
    estimate_model_parameters,
)


def main() -> None:
    path_to_mobi_zones = Path(
        r"path_to\mobi-zones.shp"
    )
    path_to_mtmc = Path(r"path_to_transport_and_mobility_microcensus_folder")

    data_directory = Path(Path(__file__).parent.parent.parent.joinpath("data"))
    input_directory = data_directory.joinpath("input").joinpath(
        "household_car_ownership"
    )

    df_hh = get_data(input_directory, path_to_mobi_zones, path_to_mtmc)

    output_directory = data_directory.joinpath("output").joinpath(
        "household_car_ownership"
    )
    output_directory.mkdir(parents=True, exist_ok=True)

    estimate_model_parameters(df_hh, output_directory)


if __name__ == "__main__":
    main()
