import os

import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
from biogeme.expressions import bioMax
from biogeme.expressions import bioMin

from simba.mobi.choice.models.public_transport_subscription_ownership.model_definition import (
    define_variables,
)
from simba.mobi.choice.models.public_transport_subscription_ownership.model_definition import (
    get_dict_betas,
)


def estimate_model(df, output_directory) -> None:
    estimate_2015 = False
    estimate_2021 = False
    estimate_2015_2021 = True
    if estimate_2015:
        df = df.loc[
            df["year"] == 2015,
        ].copy()
    elif estimate_2021:
        df = df.loc[
            df["year"] == 2021,
        ].copy()

    database = db.Database("indivPT", df)
    define_variables(database)
    globals().update(database.variables)

    dict_betas = get_dict_betas(estimate_2015, estimate_2021, estimate_2015_2021)

    if estimate_2015_2021:
        V_NONE = (
            dict_betas["ASC_NONE"]
            + dict_betas["b_OWNS_DL_NONE1521"] * driving_licence_not_NA15
            + dict_betas["b_OWNS_DL_NONE_NA1521"] * driving_licence_NA15
            + dict_betas["b_ACCESSIB_CAR_NONE15"] * boxcox_accessib_car15
            + dict_betas["b_ACCESSIB_MULTI_NONE15"] * boxcox_accsib_mul15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_OWNS_DL_NONE1521"] * driving_licence_not_NA21
                + dict_betas["b_OWNS_DL_NONE_NA1521"] * driving_licence_NA21
                + dict_betas["b_ACCESSIB_CAR_NONE21"] * boxcox_accessib_car21
                + dict_betas["b_ACCESSIB_MULTI_NONE21"] * boxcox_accsib_mul21
            )
        )

        V_GA = (
            dict_betas["ASC_GA"]
            + dict_betas["b_CARS_PER_ADULT_GA1521"] * cars_per_adult15
            + dict_betas["b_LANG_GERMAN_GA1521"] * german15
            + dict_betas["b_is_swiss_GA1521"] * is_swiss15
            + dict_betas["b_FULLTIME_GA1521"] * full_time15
            + dict_betas["b_PARTTIME_GA1521"] * part_time15
            + dict_betas["b_AGE_18_22_GA1521"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_GA1521"]
            * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_GA1521"]
            * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_GA1521"]
            * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_GA1521"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_GA1521"] * couple_without_children15
            + dict_betas["b_couple_with_children_GA15"] * couple_with_children15
            + dict_betas["b_single_parent_house_GA1521"] * single_parent_house15
            + dict_betas["b_one_person_household_GA1521"] * one_person_household15
            + dict_betas["b_household_type_NA_GA1521"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_CARS_PER_ADULT_GA1521"] * cars_per_adult21
                + dict_betas["b_LANG_GERMAN_GA1521"] * german21
                + dict_betas["b_is_swiss_GA1521"] * is_swiss21
                + dict_betas["b_FULLTIME_GA1521"] * full_time21
                + dict_betas["b_PARTTIME_GA1521"] * part_time21
                + dict_betas["b_AGE_18_22_GA1521"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_GA1521"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_GA1521"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_GA1521"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_GA1521"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_GA1521"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_GA21"] * couple_with_children21
                + dict_betas["b_single_parent_house_GA1521"] * single_parent_house21
                + dict_betas["b_one_person_household_GA1521"] * one_person_household21
                + dict_betas["b_household_type_NA_GA1521"] * household_type_NA21
            )
        )

        V_HT = (
            dict_betas["ASC_HT"]
            + dict_betas["b_NB_CARS_HH_HT_ALL1521"] * nb_cars_not_NA15
            + dict_betas["b_NB_CARS_HH_HT_ALL_NA1521"] * nb_cars_NA15
            + dict_betas["b_LANG_GERMAN_HT1521"] * german15
            + dict_betas["b_is_swiss_HT15"] * is_swiss
            + dict_betas["b_ACCESSIB_PT_HT1521"] * boxcox_accessib_pt15
            + dict_betas["b_PARTTIME_HT_ALL1521"] * part_time15
            + dict_betas["b_AGE_18_22_HT1521"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_HT15"] * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_HT15"] * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_HT1521"]
            * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_HT1521"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_HT1521"] * couple_without_children15
            + dict_betas["b_couple_with_children_HT15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HT1521"] * single_parent_house15
            + dict_betas["b_one_person_household_HT1521"] * one_person_household15
            + dict_betas["b_household_type_NA_HT1521"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_NB_CARS_HH_HT_ALL1521"] * nb_cars_not_NA21
                + dict_betas["b_NB_CARS_HH_HT_ALL_NA1521"] * nb_cars_NA21
                + dict_betas["b_LANG_GERMAN_HT1521"] * german21
                + dict_betas["b_is_swiss_HT21"] * is_swiss21
                + dict_betas["b_ACCESSIB_PT_HT1521"] * boxcox_accessib_pt21
                + dict_betas["b_PARTTIME_HT_ALL1521"] * part_time21
                + dict_betas["b_AGE_18_22_HT1521"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_HT21"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_HT21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_HT1521"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_HT1521"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_HT1521"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_HT21"] * couple_with_children21
                + dict_betas["b_single_parent_house_HT1521"] * single_parent_house21
                + dict_betas["b_one_person_household_HT1521"] * one_person_household21
                + dict_betas["b_household_type_NA_HT1521"] * household_type_NA21
            )
        )

        V_V = (
            dict_betas["ASC_V"]
            + dict_betas["b_CARS_PER_ADULT_V1521"] * cars_per_adult15
            + dict_betas["b_NB_CARS_HH_V1521"] * nb_cars_not_NA15
            + dict_betas["b_NB_CARS_HH_V_NA1521"] * nb_cars_NA15
            + dict_betas["b_PARTTIME_V1521"] * part_time15
            + dict_betas["b_LANG_GERMAN_V1521"] * german15
            + dict_betas["b_is_swiss_V15"] * is_swiss15
            + dict_betas["b_URBAN_V_ALL1521"] * urban15
            + dict_betas["b_AGE_18_22_V1521"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_V1521"] * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_V15"] * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_V1521"]
            * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_V1521"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_V1521"] * couple_without_children15
            + dict_betas["b_couple_with_children_V1521"] * couple_with_children15
            + dict_betas["b_single_parent_house_V1521"] * single_parent_house15
            + dict_betas["b_one_person_household_V1521"] * one_person_household15
            + dict_betas["b_household_type_NA_V1521"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_CARS_PER_ADULT_V1521"] * cars_per_adult21
                + dict_betas["b_NB_CARS_HH_V1521"] * nb_cars_not_NA21
                + dict_betas["b_NB_CARS_HH_V_NA1521"] * nb_cars_NA21
                + dict_betas["b_PARTTIME_V1521"] * part_time21
                + dict_betas["b_LANG_GERMAN_V1521"] * german21
                + dict_betas["b_is_swiss_V21"] * is_swiss21
                + dict_betas["b_URBAN_V_ALL1521"] * urban21
                + dict_betas["b_AGE_18_22_V1521"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_V1521"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_V21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_V1521"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_V1521"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_V1521"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_V1521"] * couple_with_children21
                + dict_betas["b_single_parent_house_V1521"] * single_parent_house21
                + dict_betas["b_one_person_household_V1521"] * one_person_household21
                + dict_betas["b_household_type_NA_V1521"] * household_type_NA21
            )
        )

        V_HTV = (
            dict_betas["ASC_HTV"]
            + dict_betas["b_CARS_PER_ADULT_HTV1521"] * cars_per_adult15
            + dict_betas["b_NB_CARS_HH_HT_ALL1521"] * nb_cars_not_NA15
            + dict_betas["b_NB_CARS_HH_HT_ALL_NA1521"] * nb_cars_NA15
            + dict_betas["b_LANG_GERMAN_HTV15"] * german15
            + dict_betas["b_is_swiss_htv1521"] * is_swiss15
            + dict_betas["b_ACCESSIB_PT_HTV15"] * boxcox_accessib_pt15
            + dict_betas["b_FULLTIME_HTV1521"] * full_time15
            + dict_betas["b_PARTTIME_HT_ALL1521"] * part_time15
            + dict_betas["b_URBAN_V_ALL1521"] * urban15
            + dict_betas["b_AGE_18_22_HTV1521"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_HTV1521"]
            * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_HTV15"]
            * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_HTV15"]
            * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_HTV1521"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_HTV1521"]
            * couple_without_children15
            + dict_betas["b_couple_with_children_HTV15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HTV1521"] * single_parent_house15
            + dict_betas["b_one_person_household_HTV1521"] * one_person_household15
            + dict_betas["b_household_type_NA_HTV1521"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_CARS_PER_ADULT_HTV1521"] * cars_per_adult21
                + dict_betas["b_NB_CARS_HH_HT_ALL1521"] * nb_cars_not_NA21
                + dict_betas["b_NB_CARS_HH_HT_ALL_NA1521"] * nb_cars_NA21
                + dict_betas["b_LANG_GERMAN_HTV21"] * german21
                + dict_betas["b_is_swiss_htv1521"] * is_swiss21
                + dict_betas["b_ACCESSIB_PT_HTV21"] * boxcox_accessib_pt21
                + dict_betas["b_FULLTIME_HTV1521"] * full_time21
                + dict_betas["b_PARTTIME_HT_ALL1521"] * part_time21
                + dict_betas["b_URBAN_V_ALL1521"] * urban21
                + dict_betas["b_AGE_18_22_HTV1521"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_HTV1521"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_HTV21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_HTV21"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_HTV1521"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_HTV1521"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_HTV21"] * couple_with_children21
                + dict_betas["b_single_parent_house_HTV1521"] * single_parent_house21
                + dict_betas["b_one_person_household_HTV1521"] * one_person_household21
                + dict_betas["b_household_type_NA_HTV1521"] * household_type_NA21
            )
        )
    else:
        V_NONE = (
            dict_betas["ASC_NONE"]
            + dict_betas["b_OWNS_DL_NONE15"] * driving_licence_not_NA15
            + dict_betas["b_OWNS_DL_NONE_NA15"] * driving_licence_NA15
            + dict_betas["b_ACCESSIB_CAR_NONE15"] * boxcox_accessib_car15
            + dict_betas["b_ACCESSIB_MULTI_NONE15"] * boxcox_accsib_mul15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_OWNS_DL_NONE21"] * driving_licence_not_NA21
                + dict_betas["b_OWNS_DL_NONE_NA21"] * driving_licence_NA21
                + dict_betas["b_ACCESSIB_CAR_NONE21"] * boxcox_accessib_car21
                + dict_betas["b_ACCESSIB_MULTI_NONE21"] * boxcox_accsib_mul21
            )
        )

        V_GA = (
            dict_betas["ASC_GA"]
            + dict_betas["b_CARS_PER_ADULT_GA15"] * cars_per_adult15
            + dict_betas["b_LANG_GERMAN_GA15"] * german15
            + dict_betas["b_is_swiss_GA15"] * is_swiss15
            + dict_betas["b_FULLTIME_GA15"] * full_time15
            + dict_betas["b_PARTTIME_GA15"] * part_time15
            + dict_betas["b_AGE_18_22_GA15"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_GA15"] * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_GA15"] * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_GA15"] * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_GA15"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_GA15"] * couple_without_children15
            + dict_betas["b_couple_with_children_GA15"] * couple_with_children15
            + dict_betas["b_single_parent_house_GA15"] * single_parent_house15
            + dict_betas["b_one_person_household_GA15"] * one_person_household15
            + dict_betas["b_household_type_NA_GA15"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_CARS_PER_ADULT_GA21"] * cars_per_adult21
                + dict_betas["b_LANG_GERMAN_GA21"] * german21
                + dict_betas["b_is_swiss_GA21"] * is_swiss21
                + dict_betas["b_FULLTIME_GA21"] * full_time21
                + dict_betas["b_PARTTIME_GA21"] * part_time21
                + dict_betas["b_AGE_18_22_GA21"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_GA21"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_GA21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_GA21"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_GA21"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_GA21"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_GA21"] * couple_with_children21
                + dict_betas["b_single_parent_house_GA21"] * single_parent_house21
                + dict_betas["b_one_person_household_GA21"] * one_person_household21
                + dict_betas["b_household_type_NA_GA21"] * household_type_NA21
            )
        )

        V_HT = (
            dict_betas["ASC_HT"]
            + dict_betas["b_NB_CARS_HH_HT_ALL15"] * nb_cars_not_NA15
            + dict_betas["b_NB_CARS_HH_HT_ALL_NA15"] * nb_cars_NA15
            + dict_betas["b_LANG_GERMAN_HT15"] * german15
            + dict_betas["b_is_swiss_HT15"] * is_swiss
            + dict_betas["b_ACCESSIB_PT_HT15"] * boxcox_accessib_pt15
            + dict_betas["b_PARTTIME_HT_ALL15"] * part_time15
            + dict_betas["b_AGE_18_22_HT15"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_HT15"] * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_HT15"] * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_HT15"] * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_HT15"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_HT15"] * couple_without_children15
            + dict_betas["b_couple_with_children_HT15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HT15"] * single_parent_house15
            + dict_betas["b_one_person_household_HT15"] * one_person_household15
            + dict_betas["b_household_type_NA_HT15"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_NB_CARS_HH_HT_ALL21"] * nb_cars_not_NA21
                + dict_betas["b_NB_CARS_HH_HT_ALL_NA21"] * nb_cars_NA21
                + dict_betas["b_LANG_GERMAN_HT21"] * german21
                + dict_betas["b_is_swiss_HT21"] * is_swiss21
                + dict_betas["b_ACCESSIB_PT_HT21"] * boxcox_accessib_pt21
                + dict_betas["b_PARTTIME_HT_ALL21"] * part_time21
                + dict_betas["b_AGE_18_22_HT21"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_HT21"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_HT21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_HT21"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_HT21"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_HT21"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_HT21"] * couple_with_children21
                + dict_betas["b_single_parent_house_HT21"] * single_parent_house21
                + dict_betas["b_one_person_household_HT21"] * one_person_household21
                + dict_betas["b_household_type_NA_HT21"] * household_type_NA21
            )
        )

        V_V = (
            dict_betas["ASC_V"]
            + dict_betas["b_CARS_PER_ADULT_V15"] * cars_per_adult15
            + dict_betas["b_NB_CARS_HH_V15"] * nb_cars_not_NA15
            + dict_betas["b_NB_CARS_HH_V_NA15"] * nb_cars_NA15
            + dict_betas["b_PARTTIME_V15"] * part_time15
            + dict_betas["b_LANG_GERMAN_V15"] * german15
            + dict_betas["b_is_swiss_V15"] * is_swiss15
            + dict_betas["b_URBAN_V_ALL15"] * urban15
            + dict_betas["b_AGE_18_22_V15"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_V15"] * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_V15"] * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_V15"] * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_V15"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_V15"] * couple_without_children15
            + dict_betas["b_couple_with_children_V15"] * couple_with_children15
            + dict_betas["b_single_parent_house_V15"] * single_parent_house15
            + dict_betas["b_one_person_household_V15"] * one_person_household15
            + dict_betas["b_household_type_NA_V15"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_CARS_PER_ADULT_V21"] * cars_per_adult21
                + dict_betas["b_NB_CARS_HH_V21"] * nb_cars_not_NA21
                + dict_betas["b_NB_CARS_HH_V_NA21"] * nb_cars_NA21
                + dict_betas["b_PARTTIME_V21"] * part_time21
                + dict_betas["b_LANG_GERMAN_V21"] * german21
                + dict_betas["b_is_swiss_V21"] * is_swiss21
                + dict_betas["b_URBAN_V_ALL21"] * urban21
                + dict_betas["b_AGE_18_22_V21"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_V21"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_V21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_V21"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_V21"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_V21"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_V21"] * couple_with_children21
                + dict_betas["b_single_parent_house_V21"] * single_parent_house21
                + dict_betas["b_one_person_household_V21"] * one_person_household21
                + dict_betas["b_household_type_NA_V21"] * household_type_NA21
            )
        )

        V_HTV = (
            dict_betas["ASC_HTV"]
            + dict_betas["b_CARS_PER_ADULT_HTV15"] * cars_per_adult15
            + dict_betas["b_NB_CARS_HH_HT_ALL15"] * nb_cars_not_NA15
            + dict_betas["b_NB_CARS_HH_HT_ALL_NA15"] * nb_cars_NA15
            + dict_betas["b_LANG_GERMAN_HTV15"] * german15
            + dict_betas["b_is_swiss_htv15"] * is_swiss15
            + dict_betas["b_ACCESSIB_PT_HTV15"] * boxcox_accessib_pt15
            + dict_betas["b_FULLTIME_HTV15"] * full_time15
            + dict_betas["b_PARTTIME_HT_ALL15"] * part_time15
            + dict_betas["b_URBAN_V_ALL15"] * urban15
            + dict_betas["b_AGE_18_22_HTV15"] * bioMax(0.0, bioMin(age15, 22.5))
            + dict_betas["b_AGE_23_26_HTV15"] * bioMax(0.0, bioMin((age15 - 22.5), 4.0))
            + dict_betas["b_AGE_27_69_HTV15"]
            * bioMax(0.0, bioMin((age15 - 26.5), 43.0))
            + dict_betas["b_AGE_70_89_HTV15"]
            * bioMax(0.0, bioMin((age15 - 69.5), 20.0))
            + dict_betas["b_AGE_90_plus_HTV15"]
            * bioMax(0.0, bioMin((age15 - 89.5), 30.5))
            + dict_betas["b_couple_without_children_HTV15"] * couple_without_children15
            + dict_betas["b_couple_with_children_HTV15"] * couple_with_children15
            + dict_betas["b_single_parent_house_HTV15"] * single_parent_house15
            + dict_betas["b_one_person_household_HTV15"] * one_person_household15
            + dict_betas["b_household_type_NA_HTV15"] * household_type_NA15
            + dict_betas["mu_2021"]
            * (
                dict_betas["b_CARS_PER_ADULT_HTV21"] * cars_per_adult21
                + dict_betas["b_NB_CARS_HH_HT_ALL21"] * nb_cars_not_NA21
                + dict_betas["b_NB_CARS_HH_HT_ALL_NA21"] * nb_cars_NA21
                + dict_betas["b_LANG_GERMAN_HTV21"] * german21
                + dict_betas["b_is_swiss_htv21"] * is_swiss21
                + dict_betas["b_ACCESSIB_PT_HTV21"] * boxcox_accessib_pt21
                + dict_betas["b_FULLTIME_HTV21"] * full_time21
                + dict_betas["b_PARTTIME_HT_ALL21"] * part_time21
                + dict_betas["b_URBAN_V_ALL21"] * urban21
                + dict_betas["b_AGE_18_22_HTV21"] * bioMax(0.0, bioMin(age21, 22.5))
                + dict_betas["b_AGE_23_26_HTV21"]
                * bioMax(0.0, bioMin((age21 - 22.5), 4.0))
                + dict_betas["b_AGE_27_69_HTV21"]
                * bioMax(0.0, bioMin((age21 - 26.5), 43.0))
                + dict_betas["b_AGE_70_89_HTV21"]
                * bioMax(0.0, bioMin((age21 - 69.5), 20.0))
                + dict_betas["b_AGE_90_plus_HTV21"]
                * bioMax(0.0, bioMin((age21 - 89.5), 30.5))
                + dict_betas["b_couple_without_children_HTV21"]
                * couple_without_children21
                + dict_betas["b_couple_with_children_HTV21"] * couple_with_children21
                + dict_betas["b_single_parent_house_HTV21"] * single_parent_house21
                + dict_betas["b_one_person_household_HTV21"] * one_person_household21
                + dict_betas["b_household_type_NA_HTV21"] * household_type_NA21
            )
        )

    V = {1: V_NONE, 2: V_GA, 3: V_HT, 4: V_V, 5: V_HTV}
    av = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}

    logprob = models.loglogit(V, av, subscriptions)

    # Change the working directory, so that biogeme writes in the correct folder
    standard_directory = os.getcwd()
    if estimate_2015:
        output_directory_for_a_specific_year = output_directory / "2015"
    elif estimate_2021:
        output_directory_for_a_specific_year = output_directory / "2021"
    elif estimate_2015_2021:
        output_directory_for_a_specific_year = output_directory / "2015_2021"
    if os.path.isdir(output_directory_for_a_specific_year) is False:
        output_directory_for_a_specific_year.mkdir(parents=True, exist_ok=True)
    os.chdir(output_directory_for_a_specific_year)

    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = "dcm_indivPT"
    results = biogeme.estimate()
    df_parameters = results.getEstimatedParameters()
    df_parameters.to_csv("parameters_dcm_pt_abo.csv")

    # Go back to the normal working directory
    os.chdir(standard_directory)
