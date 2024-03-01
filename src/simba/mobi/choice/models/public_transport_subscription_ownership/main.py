from pathlib import Path

from simba.mobi.choice.models.public_transport_subscription_ownership.data_loader import (
    get_data,
)
from simba.mobi.choice.models.public_transport_subscription_ownership.descriptive_stats import (
    visualize_piecewise_age,
)
from simba.mobi.choice.models.public_transport_subscription_ownership.model_estimation import (
    estimate_model,
)


def public_transport_subscription_ownership() -> None:
    data_directory = Path(Path(__file__).parent.parent.parent.joinpath("data"))
    input_directory = data_directory.joinpath("input").joinpath(
        "public_transport_subscription_ownership"
    )
    df_zp = get_data(input_directory)
    output_directory = data_directory.joinpath("output").joinpath(
        "public_transport_subscription_ownership"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    estimate_model(df_zp, output_directory)
    visualize_piecewise_age(output_directory)


if __name__ == "__main__":
    public_transport_subscription_ownership()
