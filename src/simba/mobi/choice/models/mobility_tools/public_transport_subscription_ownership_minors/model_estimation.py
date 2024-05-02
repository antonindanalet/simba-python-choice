import os

import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import bioMax
from biogeme.expressions import bioMin

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_minors.model_definition import (
    define_variables,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_minors.model_definition import (
    get_dict_betas,
)
from simba.mobi.choice.utils.biogeme import estimate_in_directory


def estimate_model_minors(df, output_directory):
    estimate_2015 = False
    estimate_2021 = False
    estimate_2015_2021 = True
    if estimate_2021:
        df = df.loc[
            df["year"] == 2021,
        ].copy()
    elif estimate_2015:
        df = df.loc[
            df["year"] == 2015,
        ].copy()

    database = db.Database("indivPT", df)
    define_variables(database)
    globals().update(database.variables)

    dict_betas = get_dict_betas(estimate_2015, estimate_2021, estimate_2015_2021)

    if estimate_2015_2021:
        V_NONE = (
            dict_betas["ASC_NONE"]
            + dict_betas["B_ACCESSIB_CAR_NONE1521"] * boxcox_accessib_car15
            + dict_betas["mu_2021"]
            * (dict_betas["B_ACCESSIB_CAR_NONE1521"] * boxcox_accessib_car21)
        )

        V_GA = (
            dict_betas["ASC_GA"]
            + dict_betas["beta_age15_5_12_GA"] * bioMax(0.0, bioMin((age15 - 5.0), 7.0))
            + dict_betas["beta_age1521_12_18_GA"]
            * bioMax(0.0, bioMin((age15 - 12.0), 7.0))
            + dict_betas["B_ACCESSIB_MULTI_GA15"] * accessib_multi_scaled15
            + dict_betas["B_is_swiss_GA1521"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_GA15"] * german15
            + dict_betas["b_couple_without_children_GA15"] * couple_without_children15
            + dict_betas["b_couple_with_children_GA15"] * couple_with_children15
            + dict_betas["b_single_parent_house_GA15"] * single_parent_house15
            + dict_betas["b_one_person_household_GA15"] * one_person_household15
            + dict_betas["b_household_type_NA_GA15"] * household_type_NA15
            + dict_betas["B_URBAN_GA15"] * urban15
            + dict_betas["B_FULLTIME_GA15"] * full_time15
            + dict_betas["B_PARTTIME_GA15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_GA15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_GA15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_GA15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_GA_NA15"] * nb_cars_NA15
        ) + dict_betas["mu_2021"] * (
            dict_betas["beta_age21_5_12_GA"] * bioMax(0.0, bioMin((age21 - 5.0), 7.0))
            + dict_betas["beta_age1521_12_18_GA"]
            * bioMax(0.0, bioMin((age21 - 12.0), 7.0))
            + dict_betas["B_ACCESSIB_MULTI_GA21"] * accessib_multi_scaled21
            + dict_betas["B_is_swiss_GA1521"] * is_swiss21
            + dict_betas["B_LANG_GERMAN_GA21"] * german21
            + dict_betas["b_couple_without_children_GA21"] * couple_without_children21
            + dict_betas["b_couple_with_children_GA21"] * couple_with_children21
            + dict_betas["b_single_parent_house_GA21"] * single_parent_house21
            + dict_betas["b_one_person_household_GA21"] * one_person_household21
            + dict_betas["b_household_type_NA_GA21"] * household_type_NA21
            + dict_betas["B_URBAN_GA21"] * urban21
            + dict_betas["B_FULLTIME_GA21"] * full_time21
            + dict_betas["B_PARTTIME_GA21"] * part_time21
            + dict_betas["B_ACCESSIB_PT_GA21"] * boxcox_accessib_pt21
            + dict_betas["B_ACCESSIB_CAR_GA21"] * boxcox_accessib_car21
            + dict_betas["B_NB_CARS_HH_GA21"] * nb_cars_not_NA21
            + dict_betas["B_NB_CARS_HH_GA_NA15"] * nb_cars_NA21
        )

        V_HT = (
            dict_betas["ASC_HT"]
            + dict_betas["b_age15_HT"] * age15
            + dict_betas["B_ACCESSIB_MULTI_HT15"] * accessib_multi_scaled15
            + dict_betas["B_is_swiss_HT1521"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_HT1521"] * german15
            + dict_betas["b_couple_without_children_HT15"] * couple_without_children15
            + dict_betas["b_couple_with_children_HT15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HT15"] * single_parent_house15
            + dict_betas["b_one_person_household_HT15"] * one_person_household15
            + dict_betas["b_household_type_NA_HT1521"] * household_type_NA15
            + dict_betas["B_URBAN_HT15"] * urban15
            + dict_betas["B_FULLTIME_HT15"] * full_time15
            + dict_betas["B_PARTTIME_HT15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_HT15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_HT15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_HT15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_HT_NA15"] * nb_cars_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_age21_HT"] * age21
                + dict_betas["B_ACCESSIB_MULTI_HT21"] * accessib_multi_scaled21
                + dict_betas["B_is_swiss_HT1521"] * is_swiss21
                + dict_betas["B_LANG_GERMAN_HT1521"] * german21
                + dict_betas["b_couple_without_children_HT21"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_HT21"] * couple_with_children21
                + dict_betas["b_single_parent_house_HT21"] * single_parent_house21
                + dict_betas["b_one_person_household_HT21"] * one_person_household21
                + dict_betas["b_household_type_NA_HT1521"] * household_type_NA21
                + dict_betas["B_URBAN_HT21"] * urban21
                + dict_betas["B_FULLTIME_HT21"] * full_time21
                + dict_betas["B_PARTTIME_HT21"] * part_time21
                + dict_betas["B_ACCESSIB_PT_HT21"] * boxcox_accessib_pt21
                + dict_betas["B_ACCESSIB_CAR_HT21"] * boxcox_accessib_car21
                + dict_betas["B_NB_CARS_HH_HT21"] * nb_cars_not_NA21
                + dict_betas["B_NB_CARS_HH_HT_NA21"] * nb_cars_NA21
            )
        )

        V_V = (
            dict_betas["ASC_V"]
            + dict_betas["b_age15_V"] * age15
            + dict_betas["B_ACCESSIB_MULTI_V1521"] * accessib_multi_scaled15
            + dict_betas["B_is_swiss_V15"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_V1521"] * german15
            + dict_betas["b_couple_with_children_V15"] * couple_with_children15
            + dict_betas["b_single_parent_house_V15"] * single_parent_house15
            + dict_betas["b_one_person_household_V15"] * one_person_household15
            + dict_betas["b_household_type_NA_V15"] * household_type_NA15
            + dict_betas["b_couple_without_children_V15"] * couple_without_children15
            + dict_betas["B_URBAN_V15"] * urban15
            + dict_betas["B_FULLTIME_V15"] * full_time15
            + dict_betas["B_PARTTIME_V15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_V15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_V15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_V15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_V_NA15"] * nb_cars_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_age21_V"] * age21
                + dict_betas["B_ACCESSIB_MULTI_V1521"] * accessib_multi_scaled21
                + dict_betas["B_is_swiss_V21"] * is_swiss21
                + dict_betas["B_LANG_GERMAN_V1521"] * german21
                + dict_betas["b_couple_with_children_V21"] * couple_with_children21
                + dict_betas["b_single_parent_house_V21"] * single_parent_house21
                + dict_betas["b_one_person_household_V21"] * one_person_household21
                + dict_betas["b_household_type_NA_V21"] * household_type_NA21
                + dict_betas["b_couple_without_children_V21"]
                * couple_without_children21
                + dict_betas["B_URBAN_V21"] * urban21
                + dict_betas["B_FULLTIME_V21"] * full_time21
                + dict_betas["B_PARTTIME_V21"] * part_time21
                + dict_betas["B_ACCESSIB_PT_V21"] * boxcox_accessib_pt21
                + dict_betas["B_ACCESSIB_CAR_V21"] * boxcox_accessib_car21
                + dict_betas["B_NB_CARS_HH_V21"] * nb_cars_not_NA21
                + dict_betas["B_NB_CARS_HH_V_NA21"] * nb_cars_NA21
            )
        )

        V_HTV = (
            dict_betas["ASC_HTV"]
            + dict_betas["b_age15_HTV"] * age15
            + dict_betas["B_ACCESSIB_MULTI_HTV15"] * accessib_multi_scaled15
            + dict_betas["b_is_swiss_htv15"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_HTV15"] * german15
            + dict_betas["b_couple_without_children_HTV15"] * couple_without_children15
            + dict_betas["b_couple_with_children_HTV15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HTV15"] * single_parent_house15
            + dict_betas["b_one_person_household_HTV1521"] * one_person_household15
            + dict_betas["b_household_type_NA_HTV1521"] * household_type_NA15
            + dict_betas["B_URBAN_HTV15"] * urban15
            + dict_betas["B_FULLTIME_HTV15"] * full_time15
            + dict_betas["B_PARTTIME_HTV15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_HTV15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_HTV15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_HTV15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_HTV_NA15"] * nb_cars_NA15
        ) + dict_betas["mu_2021"] * (
            dict_betas["b_age21_HTV"] * age21
            + dict_betas["B_ACCESSIB_MULTI_HTV21"] * accessib_multi_scaled21
            + dict_betas["b_is_swiss_htv21"] * is_swiss21
            + dict_betas["B_LANG_GERMAN_HTV21"] * german21
            + dict_betas["b_couple_without_children_HTV21"] * couple_without_children21
            + dict_betas["b_couple_with_children_HTV21"] * couple_with_children21
            + dict_betas["b_single_parent_house_HTV21"] * single_parent_house21
            + dict_betas["b_one_person_household_HTV1521"] * one_person_household21
            + dict_betas["b_household_type_NA_HTV1521"] * household_type_NA21
            + dict_betas["B_URBAN_HTV21"] * urban21
            + dict_betas["B_FULLTIME_HTV21"] * full_time21
            + dict_betas["B_PARTTIME_HTV21"] * part_time21
            + dict_betas["B_ACCESSIB_PT_HTV21"] * boxcox_accessib_pt21
            + dict_betas["B_ACCESSIB_CAR_HTV21"] * boxcox_accessib_car21
            + dict_betas["B_NB_CARS_HH_HTV21"] * nb_cars_not_NA21
            + dict_betas["B_NB_CARS_HH_HTV_NA21"] * nb_cars_NA21
        )
    elif estimate_2021:
        V_NONE = (
            dict_betas["ASC_NONE"]
            + dict_betas["B_ACCESSIB_CAR_NONE21"] * boxcox_accessib_car21
        )

        V_GA = (
            dict_betas["ASC_GA"]
            + dict_betas["beta_age21_5_12_GA"] * bioMax(0.0, bioMin((age21 - 5.0), 7.0))
            + dict_betas["beta_age21_12_18_GA"]
            * bioMax(0.0, bioMin((age21 - 12.0), 7.0))
            + dict_betas["B_ACCESSIB_MULTI_GA21"] * accessib_multi_scaled21
            + dict_betas["B_is_swiss_GA21"] * is_swiss21
            + dict_betas["B_LANG_GERMAN_GA21"] * german21
            + dict_betas["b_couple_without_children_GA21"] * couple_without_children21
            + dict_betas["b_couple_with_children_GA21"] * couple_with_children21
            + dict_betas["b_single_parent_house_GA21"] * single_parent_house21
            + dict_betas["b_one_person_household_GA21"] * one_person_household21
            + dict_betas["b_household_type_NA_GA21"] * household_type_NA21
            + dict_betas["B_URBAN_GA21"] * urban21
            + dict_betas["B_FULLTIME_GA21"] * full_time21
            + dict_betas["B_PARTTIME_GA21"] * part_time21
            + dict_betas["B_ACCESSIB_PT_GA21"] * boxcox_accessib_pt21
            + dict_betas["B_ACCESSIB_CAR_GA21"] * boxcox_accessib_car21
            + dict_betas["B_NB_CARS_HH_GA21"] * nb_cars_not_NA21
            + dict_betas["B_NB_CARS_HH_GA_NA21"] * nb_cars_NA21
        )

        V_HT = (
            dict_betas["ASC_HT"]
            + dict_betas["b_age21_HT"] * age21
            + dict_betas["B_ACCESSIB_MULTI_HT21"] * accessib_multi_scaled21
            + dict_betas["B_is_swiss_HT21"] * is_swiss21
            + dict_betas["B_LANG_GERMAN_HT21"] * german21
            + dict_betas["b_couple_without_children_HT21"] * couple_without_children21
            + dict_betas["b_couple_with_children_HT21"] * couple_with_children21
            + dict_betas["b_single_parent_house_HT21"] * single_parent_house21
            + dict_betas["b_one_person_household_HT21"] * one_person_household21
            + dict_betas["b_household_type_NA_HT21"] * household_type_NA21
            + dict_betas["B_URBAN_HT21"] * urban21
            + dict_betas["B_FULLTIME_HT21"] * full_time21
            + dict_betas["B_PARTTIME_HT21"] * part_time21
            + dict_betas["B_ACCESSIB_PT_HT21"] * boxcox_accessib_pt21
            + dict_betas["B_ACCESSIB_CAR_HT21"] * boxcox_accessib_car21
            + dict_betas["B_NB_CARS_HH_HT21"] * nb_cars_not_NA21
            + dict_betas["B_NB_CARS_HH_HT_NA21"] * nb_cars_NA21
        )

        V_V = (
            dict_betas["ASC_V"]
            + dict_betas["b_age21_V"] * age21
            + dict_betas["B_ACCESSIB_MULTI_V21"] * accessib_multi_scaled21
            + dict_betas["B_is_swiss_V21"] * is_swiss21
            + dict_betas["B_LANG_GERMAN_V21"] * german21
            + dict_betas["b_couple_with_children_V21"] * couple_with_children21
            + dict_betas["b_single_parent_house_V21"] * single_parent_house21
            + dict_betas["b_one_person_household_V21"] * one_person_household21
            + dict_betas["b_household_type_NA_V21"] * household_type_NA21
            + dict_betas["b_couple_without_children_V21"] * couple_without_children21
            + dict_betas["B_URBAN_V21"] * urban21
            + dict_betas["B_FULLTIME_V21"] * full_time21
            + dict_betas["B_PARTTIME_V21"] * part_time21
            + dict_betas["B_ACCESSIB_PT_V21"] * boxcox_accessib_pt21
            + dict_betas["B_ACCESSIB_CAR_V21"] * boxcox_accessib_car21
            + dict_betas["B_NB_CARS_HH_V21"] * nb_cars_not_NA21
            + dict_betas["B_NB_CARS_HH_V_NA21"] * nb_cars_NA21
        )

        V_HTV = (
            dict_betas["ASC_HTV"]
            + dict_betas["b_age21_HTV"] * age21
            + dict_betas["B_ACCESSIB_MULTI_HTV21"] * accessib_multi_scaled21
            + dict_betas["b_is_swiss_htv21"] * is_swiss21
            + dict_betas["B_LANG_GERMAN_HTV21"] * german21
            + dict_betas["b_couple_without_children_HTV21"] * couple_without_children21
            + dict_betas["b_couple_with_children_HTV21"] * couple_with_children21
            + dict_betas["b_single_parent_house_HTV21"] * single_parent_house21
            + dict_betas["b_one_person_household_HTV21"] * one_person_household21
            + dict_betas["b_household_type_NA_HTV21"] * household_type_NA21
            + dict_betas["B_URBAN_HTV21"] * urban21
            + dict_betas["B_FULLTIME_HTV21"] * full_time21
            + dict_betas["B_PARTTIME_HTV21"] * part_time21
            + dict_betas["B_ACCESSIB_PT_HTV21"] * boxcox_accessib_pt21
            + dict_betas["B_ACCESSIB_CAR_HTV21"] * boxcox_accessib_car21
            + dict_betas["B_NB_CARS_HH_HTV21"] * nb_cars_not_NA21
            + dict_betas["B_NB_CARS_HH_HTV_NA21"] * nb_cars_NA21
        )
    elif estimate_2015:
        V_NONE = (
            dict_betas["ASC_NONE"]
            + dict_betas["B_ACCESSIB_CAR_NONE15"] * boxcox_accessib_car15
        )

        V_GA = (
            dict_betas["ASC_GA"]
            + dict_betas["beta_age15_5_12_GA"] * bioMax(0.0, bioMin((age15 - 5.0), 7.0))
            + dict_betas["beta_age15_12_18_GA"]
            * bioMax(0.0, bioMin((age15 - 12.0), 7.0))
            + dict_betas["B_ACCESSIB_MULTI_GA15"] * accessib_multi_scaled15
            + dict_betas["B_is_swiss_GA15"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_GA15"] * german15
            + dict_betas["b_couple_without_children_GA15"] * couple_without_children15
            + dict_betas["b_couple_with_children_GA15"] * couple_with_children15
            + dict_betas["b_single_parent_house_GA15"] * single_parent_house15
            + dict_betas["b_one_person_household_GA15"] * one_person_household15
            + dict_betas["b_household_type_NA_GA15"] * household_type_NA15
            + dict_betas["B_URBAN_GA15"] * urban15
            + dict_betas["B_FULLTIME_GA15"] * full_time15
            + dict_betas["B_PARTTIME_GA15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_GA15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_GA15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_GA15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_GA_NA15"] * nb_cars_NA15
        )

        V_HT = (
            dict_betas["ASC_HT"]
            + dict_betas["b_age15_HT"] * age15
            + dict_betas["B_ACCESSIB_MULTI_HT15"] * accessib_multi_scaled15
            + dict_betas["B_is_swiss_HT15"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_HT15"] * german15
            + dict_betas["b_couple_without_children_HT15"] * couple_without_children15
            + dict_betas["b_couple_with_children_HT15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HT15"] * single_parent_house15
            + dict_betas["b_one_person_household_HT15"] * one_person_household15
            + dict_betas["b_household_type_NA_HT15"] * household_type_NA15
            + dict_betas["B_URBAN_HT15"] * urban15
            + dict_betas["B_FULLTIME_HT15"] * full_time15
            + dict_betas["B_PARTTIME_HT15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_HT15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_HT15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_HT15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_HT_NA15"] * nb_cars_NA15
        )

        V_V = (
            dict_betas["ASC_V"]
            + dict_betas["b_age15_V"] * age15
            + dict_betas["B_ACCESSIB_MULTI_V15"] * accessib_multi_scaled15
            + dict_betas["B_is_swiss_V15"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_V15"] * german15
            + dict_betas["b_couple_with_children_V15"] * couple_with_children15
            + dict_betas["b_single_parent_house_V15"] * single_parent_house15
            + dict_betas["b_one_person_household_V15"] * one_person_household15
            + dict_betas["b_household_type_NA_V15"] * household_type_NA15
            + dict_betas["b_couple_without_children_V15"] * couple_without_children15
            + dict_betas["B_URBAN_V15"] * urban15
            + dict_betas["B_FULLTIME_V15"] * full_time15
            + dict_betas["B_PARTTIME_V15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_V15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_V15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_V15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_V_NA15"] * nb_cars_NA15
        )

        V_HTV = (
            dict_betas["ASC_HTV"]
            + dict_betas["b_age15_HTV"] * age15
            + dict_betas["B_ACCESSIB_MULTI_HTV15"] * accessib_multi_scaled15
            + dict_betas["b_is_swiss_htv15"] * is_swiss15
            + dict_betas["B_LANG_GERMAN_HTV15"] * german15
            + dict_betas["b_couple_without_children_HTV15"] * couple_without_children15
            + dict_betas["b_couple_with_children_HTV15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HTV15"] * single_parent_house15
            + dict_betas["b_one_person_household_HTV15"] * one_person_household15
            + dict_betas["b_household_type_NA_HTV15"] * household_type_NA15
            + dict_betas["B_URBAN_HTV15"] * urban15
            + dict_betas["B_FULLTIME_HTV15"] * full_time15
            + dict_betas["B_PARTTIME_HTV15"] * part_time15
            + dict_betas["B_ACCESSIB_PT_HTV15"] * boxcox_accessib_pt15
            + dict_betas["B_ACCESSIB_CAR_HTV15"] * boxcox_accessib_car15
            + dict_betas["B_NB_CARS_HH_HTV15"] * nb_cars_not_NA15
            + dict_betas["B_NB_CARS_HH_HTV_NA15"] * nb_cars_NA15
        )

    V = {1: V_NONE, 2: V_GA, 3: V_HT, 4: V_V, 5: V_HTV}
    av = {1: 1, 2: 1, 3: htv_av, 4: 1, 5: htv_av}

    logprob = models.loglogit(V, av, subscriptions)

    if estimate_2015:
        output_directory_for_a_specific_year = output_directory / "2015"
    elif estimate_2021:
        output_directory_for_a_specific_year = output_directory / "2021"
    elif estimate_2015_2021:
        output_directory_for_a_specific_year = output_directory / "2015_2021"
    if os.path.isdir(output_directory_for_a_specific_year) is False:
        output_directory_for_a_specific_year.mkdir(parents=True, exist_ok=True)
    the_biogeme = bio.BIOGEME(database, logprob)
    the_biogeme.modelName = "dcm_indivPT_minors"

    # Calculate the null log likelihood for reporting.
    the_biogeme.calculateNullLoglikelihood(av)

    results = estimate_in_directory(the_biogeme, output_directory_for_a_specific_year)

    df_parameters = results.getEstimatedParameters()
    df_parameters.to_csv("parameters_dcm_pt_abo_minors.csv")
