import os
from pathlib import Path

import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
import pandas as pd
from biogeme.expressions import bioMax
from biogeme.expressions import bioMin

from simba.mobi.choice.models.homeoffice.model_definition import define_variables
from simba.mobi.choice.models.homeoffice.model_definition import get_dict_betas


def estimate_choice_model_telecommuting(
    df_zp: pd.DataFrame, output_directory: Path
) -> None:
    output_directory = output_directory / "models/estimation/2015_2020_2021/"
    output_directory.mkdir(parents=True, exist_ok=True)
    run_estimation(df_zp, output_directory)


def run_estimation(
    df_zp: pd.DataFrame,
    output_directory: Path,
) -> None:
    """
    :author: Antonin Danalet, based on the example '01logit.py' by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    A binary logit model on the ability to work from home."""
    database = db.Database("persons", df_zp)

    define_variables(database)

    dict_betas = get_dict_betas()

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    U = (
        dict_betas["alternative_specific_constant"]
        + models.piecewiseFormula(age_1520, [18, 35])
        + models.piecewiseFormula(work_percentage_15, [0, 95, 101])
        + dict_betas["b_executives_1520"] * executives_1520
        + dict_betas["b_german"] * german
        + dict_betas["b_no_post_school_education"] * no_post_school_educ
        + dict_betas["b_secondary_education"] * secondary_education
        + dict_betas["b_tertiary_education"] * tertiary_education
        + dict_betas["b_rural_work_1520"] * rural_work_1520
        + dict_betas["b_hh_income_na"] * hh_income_na
        + dict_betas["b_hh_income_8000_or_less"] * hh_income_less_than_2000
        + dict_betas["b_hh_income_8000_or_less"] * hh_income_2000_to_4000
        + dict_betas["b_hh_income_8000_or_less"] * hh_income_4001_to_6000
        + dict_betas["b_hh_income_8000_or_less"] * hh_income_6001_to_8000
        + dict_betas["b_number_of_children"] * number_of_children_not_NA
        + dict_betas["b_number_of_children_NA"] * number_of_children_NA
        + dict_betas["b_single_household"] * single_household
        + dict_betas["b_general_abo_halbtax"] * general_abo_halbtax
        + models.piecewiseFormula(home_work_distance_car, [0, 0.15])
        + dict_betas["b_home_work_distance_car_NA"] * home_work_distance_car_NA
        + dict_betas["b_is_agriculture_1_15"] * business_sector_agriculture_15
        + dict_betas["b_is_production_1520"] * business_sector_production_1520
        + dict_betas["b_is_wohlesale_1520"] * business_sector_wholesale_1520
        + dict_betas["b_is_falc_id_6to9_1520"] * is_falc_id_6to9_1520
        + dict_betas["b_falc_id_NA"] * falc_id_NA
        + dict_betas["beta_accsib_home_not_NA_5_10_1520"]
        * bioMax(0.0, bioMin((accsib_home_not_NA_1520 - 5.0), 5.0))
        + dict_betas["beta_accsib_home_not_NA_10_24_1520"]
        * bioMax(0.0, bioMin((accsib_home_not_NA_1520 - 10.0), 14.0))
        + dict_betas["beta_work_percentage_0_95_20"]
        * bioMax(0.0, bioMin((work_percentage_20 - 0.0), 95.0))
        + dict_betas["beta_work_percentage_95_101_20_21"]
        * bioMax(0.0, bioMin((work_percentage_20_21 - 95.0), 6.0))
        + models.piecewiseFormula(age_21, [18, 35])
        + dict_betas["beta_work_percentage_0_95_21"]
        * bioMax(0.0, bioMin((work_percentage_21 - 0.0), 95.0))
        + dict_betas["b_executives_21"] * executives_21
        + dict_betas["b_is_agriculture_1_21"] * business_sector_agriculture_21
        + dict_betas["b_is_production_1_21"] * business_sector_production_21
        + dict_betas["b_is_wohlesale_1_21"] * business_sector_wholesale_21
        + dict_betas["b_is_falc_id_6to9_1_21"] * is_falc_id_6to9_21
        + dict_betas["beta_accsib_home_not_NA_5_10_21"]
        * bioMax(0.0, bioMin((accsib_home_not_NA_21 - 5.0), 5.0))
        + dict_betas["beta_accsib_home_not_NA_10_24_21"]
        * bioMax(0.0, bioMin((accsib_home_not_NA_21 - 10.0), 14.0))
    )
    U_no_telecommuting = 0

    # Scale associated with 2020 is estimated
    scale = (
        (year == 2015)
        + (year == 2020) * dict_betas["scale_2020"]
        + (year == 2021) * dict_betas["scale_2021"]
    )

    # Associate utility functions with the numbering of alternatives
    V = {1: scale * U, 0: U_no_telecommuting}  # 1: Yes or sometimes, 2: No

    # All alternatives are supposed to be always available
    av = {1: 1, 0: 1}

    # Definition of the model. This is the contribution of each observation to the log likelihood function.
    # Choice variable: "telecommuting"
    logprob = models.loglogit(V, av, telecommuting)

    # Change the working directory, so that biogeme writes in the correct folder
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    # Create the Biogeme object
    the_biogeme = bio.BIOGEME(database, logprob)
    the_biogeme.modelName = "wfh_model_sbb"

    # Calculate the null log likelihood for reporting.
    the_biogeme.calculateNullLoglikelihood(av)

    # Estimate the parameters
    results = the_biogeme.estimate()

    # Get the results in LaTeX
    # results.writeLaTeX()

    # Go back to the normal working directory
    os.chdir(standard_directory)
