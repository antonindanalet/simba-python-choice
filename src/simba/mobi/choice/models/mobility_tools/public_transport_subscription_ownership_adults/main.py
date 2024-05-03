from pathlib import Path

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.data_loader import (
    get_data,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.descriptive_stats import (
    distribution_half_fare_regional_travelcards,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.descriptive_stats import (
    visualize_piecewise_age,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.model_estimation import (
    estimate_model,
)


def public_transport_subscription_ownership() -> None:
    path_to_mobi_zones = Path(
        r"\\path_to\mobi-zones.shp"
    )
    path_to_mtmc = Path(r"\\path_to_transport_and_mobility_microcensus_folder")
    data_directory = Path(Path(__file__).parent.parent.parent.parent.joinpath("data"))
    input_directory = data_directory.joinpath("input").joinpath(
        "public_transport_subscription_ownership"
    )
    df_zp = get_data(input_directory, path_to_mtmc, path_to_mobi_zones)
    output_directory = data_directory.joinpath("output").joinpath(
        "public_transport_subscription_ownership"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    estimate_model(df_zp, output_directory)
    visualize_piecewise_age(output_directory)
    distribution_half_fare_regional_travelcards(path_to_mtmc)


if __name__ == "__main__":
    public_transport_subscription_ownership()
