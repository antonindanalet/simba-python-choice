from pathlib import Path

import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models

from simba.mobi.choice.models.mobility_tools.household_car_ownership.model_definition import (
    define_variables,
)
from simba.mobi.choice.models.mobility_tools.household_car_ownership.model_definition import (
    get_dict_betas,
)
from simba.mobi.choice.utils.biogeme import estimate_in_directory


def estimate_model_parameters(df, output_directory: Path) -> None:
    database = db.Database("hh", df)
    define_variables(database)
    globals().update(database.variables)

    # Beta's for 2021
    dict_betas = get_dict_betas()

    # Utility functions
    V_0 = dict_betas["ASC_0"]

    V_1 = (
        dict_betas["ASC_1"]
        + dict_betas["B_NB_ADULTS_1_21"] * nb_adults21
        + dict_betas["b_nb_children_1_21"] * nb_children21
        + dict_betas["b_nb_dl_1_21"] * nb_driving_licences_not_na21
        + dict_betas["b_nb_dl_na_1_21"] * nb_driving_licences_na21
        + dict_betas["B_ACCESSIB_PT_1_21"] * log_accessib_pt21
        + dict_betas["B_ACCESSIB_CAR_1_21"] * boxcox_accessib_car21
        + dict_betas["B_ACCESSIB_MULTI_1_21"] * accessib_multi_scaled21
        + dict_betas["B_DLS_PER_ADULT_1_21"] * dls_per_adult21
        + dict_betas["B_LANG_GERMAN_1_21"] * german21
        + dict_betas["B_PCOST_1_21"] * pc_car21
        + dict_betas["B_PCOST_FREE_1_21"] * free_parking21
        + dict_betas["B_PCOST_LOG_1_21"] * (1 - free_parking21) * pcost_log21
        + dict_betas["B_COUPLE_CHILDREN_1_21"] * couple_with_children21
        + dict_betas["B_COUPLE_WITHOUT_CHILDREN_1_21"] * couple_without_children21
        + dict_betas["B_SINGLE_PARENT_1_21"] * single_parent_house21
        + dict_betas["B_ONE_PERSON_1_21"] * one_person_household21
        + dict_betas["B_HH_NA_1_21"] * household_type_NA21
        + dict_betas["B_URBAN_1_21"] * urban21
        + dict_betas["B_RURAL_1_21"] * rural21
    )

    V_2 = (
        dict_betas["ASC_2"]
        + dict_betas["B_NB_ADULTS_2_21"] * nb_adults21
        + dict_betas["b_nb_children_2_21"] * nb_children21
        + dict_betas["b_nb_dl_2_21"] * nb_driving_licences_not_na21
        + dict_betas["b_nb_dl_na_2_21"] * nb_driving_licences_na21
        + dict_betas["B_ACCESSIB_PT_2_21"] * log_accessib_pt21
        + dict_betas["B_ACCESSIB_CAR_2_21"] * boxcox_accessib_car21
        + dict_betas["B_ACCESSIB_MULTI_2_21"] * accessib_multi_scaled21
        + dict_betas["B_DLS_PER_ADULT_2_21"] * dls_per_adult21
        + dict_betas["B_LANG_GERMAN_2_21"] * german21
        + dict_betas["B_PCOST_2_21"] * pc_car21
        + dict_betas["B_PCOST_FREE_2_21"] * free_parking21
        + dict_betas["B_PCOST_LOG_2_21"] * (1 - free_parking21) * pcost_log21
        + dict_betas["B_COUPLE_CHILDREN_2_21"] * couple_with_children21
        + dict_betas["B_COUPLE_WITHOUT_CHILDREN_2_21"] * couple_without_children21
        + dict_betas["B_SINGLE_PARENT_2_21"] * single_parent_house21
        + dict_betas["B_ONE_PERSON_2_21"] * one_person_household21
        + dict_betas["B_HH_NA_2_21"] * household_type_NA21
        + dict_betas["B_URBAN_2_21"] * urban21
        + dict_betas["B_RURAL_2_21"] * rural21
    )

    V_3 = (
        dict_betas["ASC_3"]
        + dict_betas["B_NB_ADULTS_3_21"] * nb_adults21
        + dict_betas["b_nb_children_3_21"] * nb_children21
        + dict_betas["b_nb_dl_3_21"] * nb_driving_licences_not_na21
        + dict_betas["b_nb_dl_na_3_21"] * nb_driving_licences_na21
        + dict_betas["B_ACCESSIB_PT_3_21"] * log_accessib_pt21
        + dict_betas["B_ACCESSIB_CAR_3_21"] * boxcox_accessib_car21
        + dict_betas["B_ACCESSIB_MULTI_3_21"] * accessib_multi_scaled21
        + dict_betas["B_DLS_PER_ADULT_3_21"] * dls_per_adult21
        + dict_betas["B_LANG_GERMAN_3_21"] * german21
        + dict_betas["B_PCOST_3_21"] * pc_car21
        + dict_betas["B_PCOST_FREE_3_21"] * free_parking21
        + dict_betas["B_PCOST_LOG_3_21"] * (1 - free_parking21) * pcost_log21
        + dict_betas["B_COUPLE_CHILDREN_3_21"] * couple_with_children21
        + dict_betas["B_COUPLE_WITHOUT_CHILDREN_3_21"] * couple_without_children21
        + dict_betas["B_SINGLE_PARENT_3_21"] * single_parent_house21
        + dict_betas["B_ONE_PERSON_3_21"] * one_person_household21
        + dict_betas["B_HH_NA_3_21"] * household_type_NA21
        + dict_betas["B_URBAN_3_21"] * urban21
        + dict_betas["B_RURAL_3_21"] * rural21
    )

    V = {0: V_0, 1: V_1, 2: V_2, 3: V_3}
    av = {0: 1, 1: 1, 2: 1, 3: 1}

    logprob = models.loglogit(V, av, nb_cars)

    # Define the directory where biogeme writes the output
    output_directory = Path(output_directory, "2021/")
    output_directory.mkdir(parents=True, exist_ok=True)

    the_biogeme = bio.BIOGEME(database, logprob)
    the_biogeme.modelName = "dcm_hh_car_ownership"

    # Calculate the null log likelihood for reporting.
    the_biogeme.calculateNullLoglikelihood(av)

    results = estimate_in_directory(the_biogeme, output_directory)
    df_parameters = results.getEstimatedParameters()
    df_parameters.to_csv(
        output_directory.joinpath("parameters_dcm_hh_car_ownership.csv")
    )
