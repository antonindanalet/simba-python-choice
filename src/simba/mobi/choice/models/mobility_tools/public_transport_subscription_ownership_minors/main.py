from pathlib import Path

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_minors.data_loader import (
    get_data,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_minors.model_estimation import (
    estimate_model_minors,
)


def public_transport_subscription_ownership_minors() -> None:
    path_to_mobi_zones = Path(
        r"\\wsbbrz0283\mobi\50_Ergebnisse\MOBi_4.0\2017\plans\3.3.2017.7.100pct\mobi-zones.shp"
    )
    path_to_mtmc = Path(r"\\wsbbrz0283\mobi\41_MZMV\01_Inputdaten\MZMV")
    data_directory = Path(Path(__file__).parent.parent.parent.parent.joinpath("data"))
    input_directory = data_directory.joinpath("input").joinpath(
        "public_transport_subscription_ownership_minor"
    )
    df_zp = get_data(input_directory, path_to_mtmc, path_to_mobi_zones)
    output_directory = data_directory.joinpath("output").joinpath(
        "public_transport_subscription_ownership_minor"
    )
    output_directory.mkdir(parents=True, exist_ok=True)
    estimate_model_minors(df_zp, output_directory)


if __name__ == "__main__":
    public_transport_subscription_ownership_minors()
