from pathlib import Path

from simba.mobi.choice.models.mobility_tools.driving_license.data_loader import get_data
from simba.mobi.choice.models.mobility_tools.driving_license.descriptive_stats import (
    visualize_cost,
)
from simba.mobi.choice.models.mobility_tools.driving_license.descriptive_stats import (
    visualize_piecewise_age,
)
from simba.mobi.choice.models.mobility_tools.driving_license.model_estimation import (
    estimate_model,
)


def driving_licence_choice() -> None:
    path_to_mobi_zones = Path(
        r"\\path_to\mobi-zones.shp"
    )
    path_to_mtmc = Path(r"path_to_transport_and_mobility_microcensus_folder")

    data_directory = Path(Path(__file__).parent.parent.parent.joinpath("data"))
    input_directory = data_directory.joinpath("input").joinpath("driving_license")
    input_directory.mkdir(parents=True, exist_ok=True)
    output_directory = data_directory.joinpath("output").joinpath("driving_license")
    output_directory.mkdir(parents=True, exist_ok=True)

    df_zp = get_data(
        input_directory,
        path_to_mtmc_data=path_to_mtmc,
        path_to_mobi_zones=path_to_mobi_zones,
    )
    estimate_model(df_zp, output_directory)
    visualize_piecewise_age(output_directory)
    visualize_cost(output_directory)


if __name__ == "__main__":
    driving_licence_choice()
