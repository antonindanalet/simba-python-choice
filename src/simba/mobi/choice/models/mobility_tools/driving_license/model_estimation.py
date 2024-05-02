from pathlib import Path

import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import bioMax
from biogeme.expressions import bioMin

from simba.mobi.choice.models.mobility_tools.driving_license.model_definition import (
    define_variables,
)
from simba.mobi.choice.models.mobility_tools.driving_license.model_definition import (
    get_dict_betas,
)
from simba.mobi.choice.utils.biogeme import estimate_in_directory


def estimate_model(df_zp, output_directory: Path) -> None:
    estimate_2015 = False
    estimate_2021 = True
    estimate_2015_2020_2021 = False
    if estimate_2015:
        df_zp = df_zp.loc[
            df_zp["year"] == 2015,
        ].copy()
    elif estimate_2021:
        df_zp = df_zp.loc[
            df_zp["year"] == 2021,
        ].copy()
    database = db.Database("indivDL", df_zp)

    define_variables(database, estimate_2015_2020_2021)
    globals().update(database.variables)

    dict_betas = get_dict_betas(estimate_2015_2020_2021)

    if estimate_2015_2020_2021:
        V_NODL = 0

        V_DL = (
            dict_betas["ASC_DL"]
            + dict_betas["B_FULLTIME152021"] * full_time15
            + dict_betas["B_PARTTIME152021"] * part_time15
            + dict_betas["B_ACCESSIB_PT152021"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_MULTI152021"] * boxcox_accessib_multi15
            + dict_betas["B_parking_cost_car152021"] * pc_car15
            + dict_betas["B_parking_cost_car_log152021"]
            * (1 - free_parking_car15)
            * parking_cost_car_log15
            + dict_betas["B_free_parking_car152021"] * free_parking_car15
            + dict_betas["B_is_swiss152021"] * is_swiss15
            + dict_betas["beta_couple_with_children152021"] * couple_with_children15
            + dict_betas["beta_couple_without_children152021"]
            * couple_without_children15
            + dict_betas["beta_single_parent_house15"] * single_parent_house15
            + dict_betas["beta_household_type_NA15"] * household_type_NA15
            + dict_betas["B_LANG_FRENCH152021"] * french15
            + dict_betas["beta_age152021_0_22"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["beta_age1520_23_26"]
            * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["beta_age1520_27_69"]
            * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["beta_age1520_70_89"]
            * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["beta_age152021_90_120"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["mu_2020"]
            * (
                dict_betas["B_FULLTIME152021"] * full_time20
                + dict_betas["B_PARTTIME152021"] * part_time20
                + dict_betas["B_ACCESSIB_PT152021"] * boxcox_accessib_pt20
                + dict_betas["B_ACCESSIB_MULTI152021"] * boxcox_accessib_multi20
                + dict_betas["B_parking_cost_car152021"] * pc_car20
                + dict_betas["B_parking_cost_car_log152021"]
                * (1 - free_parking_car20)
                * parking_cost_car_log20
                + dict_betas["B_free_parking_car152021"] * free_parking_car20
                + dict_betas["B_is_swiss152021"] * is_swiss20
                + dict_betas["beta_couple_with_children152021"] * couple_with_children20
                + dict_betas["beta_couple_without_children152021"]
                * couple_without_children20
                + dict_betas["beta_single_parent_house20"] * single_parent_house20
                + dict_betas["beta_household_type_NA20"] * household_type_NA20
                + dict_betas["B_LANG_FRENCH152021"] * french20
                + dict_betas["beta_age152021_0_22"] * bioMax(0.0, bioMin(age20, 22.5))
                + dict_betas["beta_age1520_23_26"]
                * bioMax(0.0, bioMin((age20 - 22.5), 4.0))
                + dict_betas["beta_age1520_27_69"]
                * bioMax(0.0, bioMin((age20 - 26.5), 43.0))
                + dict_betas["beta_age1520_70_89"]
                * bioMax(0.0, bioMin((age20 - 69.5), 20.0))
                + dict_betas["beta_age152021_90_120"]
                * bioMax(0.0, bioMin((age20 - 89.5), 30.5))
            )
            + dict_betas["mu_2021"]
            * (
                dict_betas["B_FULLTIME152021"] * full_time21
                + dict_betas["B_PARTTIME152021"] * part_time21
                + dict_betas["B_ACCESSIB_PT152021"] * boxcox_accessib_pt21
                + dict_betas["B_ACCESSIB_MULTI152021"] * boxcox_accessib_multi21
                + dict_betas["B_parking_cost_car152021"] * pc_car21
                + dict_betas["B_parking_cost_car_log152021"]
                * (1 - free_parking_car21)
                * parking_cost_car_log21
                + dict_betas["B_free_parking_car152021"] * free_parking_car21
                + dict_betas["B_is_swiss152021"] * is_swiss21
                + dict_betas["beta_couple_with_children152021"] * couple_with_children21
                + dict_betas["beta_couple_without_children152021"]
                * couple_without_children21
                + dict_betas["beta_single_parent_house21"] * single_parent_house21
                + dict_betas["beta_household_type_NA21"] * household_type_NA21
                + dict_betas["B_LANG_FRENCH152021"] * french21
                + dict_betas["beta_age152021_0_22"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["beta_age21_23_26"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["beta_age21_27_69"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["beta_age21_70_89"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["beta_age152021_90_120"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
            )
        )
    else:
        V_NODL = 0

        V_DL = (
            dict_betas["ASC_DL"]
            + dict_betas["B_FULLTIME152021"] * full_time
            + dict_betas["B_PARTTIME152021"] * part_time
            + dict_betas["B_ACCESSIB_PT152021"] * boxcox_accessib_pt
            + dict_betas["B_ACCESSIB_MULTI152021"] * boxcox_accessib_multi
            + dict_betas["B_parking_cost_car152021"] * pc_car
            + dict_betas["B_parking_cost_car_log152021"]
            * (1 - free_parking_car)
            * parking_cost_car_log
            + dict_betas["B_free_parking_car152021"] * free_parking_car
            + dict_betas["B_is_swiss152021"] * is_swiss
            + dict_betas["beta_couple_with_children"] * couple_with_children
            + dict_betas["beta_couple_without_children"] * couple_without_children
            + dict_betas["beta_single_parent_house"] * single_parent_house
            + dict_betas["beta_household_type_NA"] * household_type_NA
            + dict_betas["B_LANG_FRENCH152021"] * french
            + dict_betas["beta_age_0_22"] * bioMax(0.0, bioMin(age, 22.5))
            + dict_betas["beta_age_23_26"] * bioMax(0.0, bioMin((age - 22.5), 4.0))
            + dict_betas["beta_age_27_69"] * bioMax(0.0, bioMin((age - 26.5), 43.0))
            + dict_betas["beta_age_70_89"] * bioMax(0.0, bioMin((age - 69.5), 20.0))
            + dict_betas["beta_age_90_120"] * bioMax(0.0, bioMin((age - 89.5), 30.5))
        )

    V = {0: V_NODL, 1: V_DL}
    av = {0: 1, 1: 1}

    # Definition of the model. This is the contribution of each
    # observation to the log likelihood function.
    logprob = models.loglogit(V, av, driving_licence)

    # Define the directory where biogeme writes the output
    if estimate_2015_2020_2021:
        output_directory = Path(output_directory, "2015_2020_2021/")
    elif estimate_2015:
        output_directory = Path(output_directory, "2015_updated/")
    elif estimate_2021:
        output_directory = Path(output_directory, "2021/")

    output_directory.mkdir(parents=True, exist_ok=True)
    # Create the Biogeme object
    the_biogeme = bio.BIOGEME(database, logprob)
    the_biogeme.modelName = "dcm_hh_dl"

    # Calculate the null log likelihood for reporting.
    the_biogeme.calculateNullLoglikelihood(av)

    results = estimate_in_directory(the_biogeme, output_directory)

    # Get the results in a pandas table
    df_parameters = results.getEstimatedParameters()
    df_parameters.to_csv(output_directory.joinpath("parameters_dcm_hh_dl.csv"))
