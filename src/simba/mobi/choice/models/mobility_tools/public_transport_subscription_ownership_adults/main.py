from pathlib import Path

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.calibrate_the_constants import (
    calibrate_the_constant_by_simulating_on_microcensus,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.calibrate_the_constants import (
    calibrate_the_constant_by_simulating_on_synthetic_population,
)
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
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.validate_model_with_synpop import (
    validate_model_with_syn_pop_2022,
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
    # calibrate_the_constant_by_simulating_on_microcensus(input_directory, df_zp)
    validate_model_with_syn_pop_2022(
        input_directory, output_directory, path_to_mobi_zones
    )
    calibrate_the_constant_by_simulating_on_synthetic_population(
        input_directory, output_directory
    )


if __name__ == "__main__":
    public_transport_subscription_ownership()
