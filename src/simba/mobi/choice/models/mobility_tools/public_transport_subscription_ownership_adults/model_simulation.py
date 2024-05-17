from typing import Dict

import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.models as models
import pandas as pd
from biogeme.expressions import bioMax
from biogeme.expressions import bioMin

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.model_definition import (
    get_dict_betas,
)


def run_simulation(df_persons: pd.DataFrame, beta_values: Dict) -> Dict:
    dict_betas = get_dict_betas(
        estimate_2015=False, estimate_2021=False, estimate_2015_2021=True
    )
    not_needed_betas = [
        "mu_2021",
        "b_OWNS_DL_NONE_NA1521",
        "b_NB_CARS_HH_HT_ALL_NA1521",
        "b_NB_CARS_HH_GA_V_NA1521",
        "b_household_type_NA_GA1521",
        "b_household_type_NA_HT1521",
        "b_household_type_NA_V1521",
        "b_household_type_NA_HTV1521",
        "b_couple_with_children_GA21",
        "b_ACCESSIB_CAR_NONE21",
        "b_ACCESSIB_MULTI_NONE21",
        "b_ACCESSIB_PT_HTV21",
        "b_is_swiss_HT21",
        "b_is_swiss_V21",
        "b_AGE_23_26_HT21",
        "b_AGE_27_69_HT21",
        "b_AGE_27_69_V21",
        "b_AGE_27_69_HTV21",
        "b_AGE_70_89_HTV21",
        "b_couple_with_children_HT21",
        "b_couple_with_children_HTV21",
    ]
    for beta_key in not_needed_betas:
        dict_betas.pop(beta_key)

    # Read the data
    database = db.Database("persons", df_persons)
    globals().update(database.variables)

    V_NONE = (
        dict_betas["ASC_NONE"]
        + dict_betas["b_OWNS_DL_NONE1521"] * driving_licence
        + dict_betas["b_ACCESSIB_CAR_NONE15"] * boxcox_accessib_car
        + dict_betas["b_ACCESSIB_MULTI_NONE15"] * boxcox_accsib_mul
    )

    V_GA = (
        dict_betas["ASC_GA"]
        + dict_betas["b_CARS_PER_ADULT_GA1521"] * cars_per_adult
        + dict_betas["b_NB_CARS_HH_GA_V1521"] * hcar_ownership
        + dict_betas["b_LANG_GERMAN_GA1521"] * german
        + dict_betas["b_is_swiss_GA1521"] * is_swiss
        + dict_betas["b_FULLTIME_GA1521"] * full_time
        + dict_betas["b_PARTTIME_GA1521"] * part_time
        + dict_betas["b_AGE_18_22_GA1521"] * bioMax(0.0, bioMin(age, 22.5))
        + dict_betas["b_AGE_23_26_GA1521"] * bioMax(0.0, bioMin((age - 22.5), 4.0))
        + dict_betas["b_AGE_27_69_GA1521"] * bioMax(0.0, bioMin((age - 26.5), 43.0))
        + dict_betas["b_AGE_70_89_GA1521"] * bioMax(0.0, bioMin((age - 69.5), 20.0))
        + dict_betas["b_AGE_90_plus_GA1521"] * bioMax(0.0, bioMin((age - 89.5), 30.5))
        + dict_betas["b_couple_without_children_GA1521"] * couple_without_children
        + dict_betas["b_couple_with_children_GA15"] * couple_with_children
        + dict_betas["b_single_parent_house_GA1521"] * single_parent_house
        + dict_betas["b_one_person_household_GA1521"] * one_person_household
    )

    V_HT = (
        dict_betas["ASC_HT"]
        + dict_betas["b_NB_CARS_HH_HT_ALL1521"] * hcar_ownership
        + dict_betas["b_LANG_GERMAN_HT1521"] * german
        + dict_betas["b_is_swiss_HT15"] * is_swiss
        + dict_betas["b_ACCESSIB_PT_HT1521"] * boxcox_accessib_pt
        + dict_betas["b_PARTTIME_HT_ALL1521"] * part_time
        + dict_betas["b_AGE_18_22_HT1521"] * bioMax(0.0, bioMin(age, 22.5))
        + dict_betas["b_AGE_23_26_HT15"] * bioMax(0.0, bioMin((age - 22.5), 4.0))
        + dict_betas["b_AGE_27_69_HT15"] * bioMax(0.0, bioMin((age - 26.5), 43.0))
        + dict_betas["b_AGE_70_89_HT1521"] * bioMax(0.0, bioMin((age - 69.5), 20.0))
        + dict_betas["b_AGE_90_plus_HT1521"] * bioMax(0.0, bioMin((age - 89.5), 30.5))
        + dict_betas["b_couple_without_children_HT1521"] * couple_without_children
        + dict_betas["b_couple_with_children_HT15"] * couple_with_children
        + dict_betas["b_single_parent_house_HT1521"] * single_parent_house
        + dict_betas["b_one_person_household_HT1521"] * one_person_household
    )

    V_V = (
        dict_betas["ASC_V"]
        + dict_betas["b_CARS_PER_ADULT_V1521"] * cars_per_adult
        + dict_betas["b_NB_CARS_HH_GA_V1521"] * hcar_ownership
        + dict_betas["b_PARTTIME_V1521"] * part_time
        + dict_betas["b_LANG_GERMAN_V1521"] * german
        + dict_betas["b_is_swiss_V15"] * is_swiss
        + dict_betas["b_URBAN_V_ALL1521"] * urban
        + dict_betas["b_AGE_18_22_V1521"] * bioMax(0.0, bioMin(age, 22.5))
        + dict_betas["b_AGE_23_26_V1521"] * bioMax(0.0, bioMin((age - 22.5), 4.0))
        + dict_betas["b_AGE_27_69_V15"] * bioMax(0.0, bioMin((age - 26.5), 43.0))
        + dict_betas["b_AGE_70_89_V1521"] * bioMax(0.0, bioMin((age - 69.5), 20.0))
        + dict_betas["b_AGE_90_plus_V1521"] * bioMax(0.0, bioMin((age - 89.5), 30.5))
        + dict_betas["b_couple_without_children_V1521"] * couple_without_children
        + dict_betas["b_couple_with_children_V1521"] * couple_with_children
        + dict_betas["b_single_parent_house_V1521"] * single_parent_house
        + dict_betas["b_one_person_household_V1521"] * one_person_household
    )

    V_HTV = (
        dict_betas["ASC_HTV"]
        + dict_betas["b_CARS_PER_ADULT_HTV1521"] * cars_per_adult
        + dict_betas["b_NB_CARS_HH_HT_ALL1521"] * hcar_ownership
        + dict_betas["b_LANG_GERMAN_HTV15"] * german
        + dict_betas["b_is_swiss_htv1521"] * is_swiss
        + dict_betas["b_ACCESSIB_PT_HTV15"] * boxcox_accessib_pt
        + dict_betas["b_FULLTIME_HTV1521"] * full_time
        + dict_betas["b_PARTTIME_HT_ALL1521"] * part_time
        + dict_betas["b_URBAN_V_ALL1521"] * urban
        + dict_betas["b_AGE_18_22_HTV1521"] * bioMax(0.0, bioMin(age, 22.5))
        + dict_betas["b_AGE_23_26_HTV1521"] * bioMax(0.0, bioMin((age - 22.5), 4.0))
        + dict_betas["b_AGE_27_69_HTV15"] * bioMax(0.0, bioMin((age - 26.5), 43.0))
        + dict_betas["b_AGE_70_89_HTV15"] * bioMax(0.0, bioMin((age - 69.5), 20.0))
        + dict_betas["b_AGE_90_plus_HTV1521"] * bioMax(0.0, bioMin((age - 89.5), 30.5))
        + dict_betas["b_couple_without_children_HTV1521"] * couple_without_children
        + dict_betas["b_couple_with_children_HTV15"] * couple_with_children
        + dict_betas["b_single_parent_house_HTV1521"] * single_parent_house
        + dict_betas["b_one_person_household_HTV1521"] * one_person_household
    )

    # Associate utility functions with the numbering of alternatives
    utility_functions_with_numbering_of_alternatives = {
        1: V_NONE,
        2: V_GA,
        3: V_HT,
        4: V_V,
        5: V_HTV,
    }

    # The choice model is a logit, with availability conditions
    prob_none = models.logit(utility_functions_with_numbering_of_alternatives, None, 1)
    prob_GA = models.logit(utility_functions_with_numbering_of_alternatives, None, 2)
    prob_HT = models.logit(utility_functions_with_numbering_of_alternatives, None, 3)
    prob_V = models.logit(utility_functions_with_numbering_of_alternatives, None, 4)
    prob_HTV = models.logit(utility_functions_with_numbering_of_alternatives, None, 5)

    simulate = {
        "Prob. none": prob_none,
        "Prob. GA": prob_GA,
        "Prob. HT": prob_HT,
        "Prob. V": prob_V,
        "Prob. HTV": prob_HTV,
    }
    the_biogeme = bio.BIOGEME(database, simulate, skip_audit=True)

    not_needed_betas = [
        "mu_2021",
        "B_OWNS_DL_NONE_NA1521",
        "B_NB_CARS_HH_HT_ALL_NA1521",
        "B_NB_CARS_HH_GA_V_NA1521",
        "b_household_type_NA_GA1521",
        "b_household_type_NA_HT1521",
        "b_household_type_NA_V1521",
        "b_household_type_NA_HTV1521",
        "B_ACCESSIB_CAR_NONE21",
        "B_LANG_GERMAN_HTV21",
        "B_ACCESSIB_MULTI_NONE21",
        "B_ACCESSIB_PT_HTV21",
        "B_is_swiss_HT21",
        "B_AGE_23_26_HT21",
        "B_AGE_27_69_HT21",
        "B_AGE_27_69_V21",
        "B_AGE_27_69_HTV21",
        "B_AGE_70_89_HTV21",
    ]
    for beta_key in not_needed_betas:
        beta_values.pop(beta_key, None)
    biogeme_simulation = the_biogeme.simulate(beta_values)
    predicted_share_none = biogeme_simulation["Prob. none"].mean()
    predicted_share_ga = biogeme_simulation["Prob. GA"].mean()
    predicted_share_ht = biogeme_simulation["Prob. HT"].mean()
    predicted_share_v = biogeme_simulation["Prob. V"].mean()
    predicted_share_htv = biogeme_simulation["Prob. HTV"].mean()
    return {
        "Predicted share none": predicted_share_none,
        "Predicted share GA": predicted_share_ga,
        "Predicted share HT": predicted_share_ht,
        "Predicted share V": predicted_share_v,
        "Predicted share HTV": predicted_share_htv,
    }
