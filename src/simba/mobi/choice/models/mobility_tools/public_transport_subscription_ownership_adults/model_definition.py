import biogeme
from biogeme.expressions import Beta
from biogeme.expressions import bioMax
from biogeme.expressions import Variable


def define_variables(database: biogeme.database.Database) -> None:
    globals().update(database.variables)

    # General variables
    driving_licence = Variable("driving_licence")
    subscriptions = Variable("subscriptions")
    nb_cars = Variable("nb_cars")
    language = Variable("language")
    full_time = Variable("full_time")
    part_time = Variable("part_time")
    accsib_mul = Variable("accsib_mul")
    accsib_pt = Variable("accsib_pt")
    accsib_car = Variable("accsib_car")
    nb_adults = Variable("nb_adults")
    is_swiss = Variable("is_swiss")
    age = Variable("age")
    W_stadt_land_2012 = Variable("W_stadt_land_2012")
    year = Variable("year")
    hhtyp = Variable("hhtyp")

    year15 = database.DefineVariable("year15", year == 2015)
    year21 = database.DefineVariable("year21", year == 2021)

    is_swiss15 = database.DefineVariable("is_swiss15", is_swiss * year15)
    is_swiss21 = database.DefineVariable("is_swiss21", is_swiss * year21)

    full_time15 = database.DefineVariable("full_time15", full_time * year15)
    full_time21 = database.DefineVariable("full_time21", full_time * year21)

    part_time15 = database.DefineVariable("part_time15", part_time * year15)
    part_time21 = database.DefineVariable("part_time21", part_time * year21)

    age15 = database.DefineVariable("age15", age * year15)
    age21 = database.DefineVariable("age21", age * year21)

    driving_licence_not_NA15 = database.DefineVariable(
        "driving_licence_not_NA15", (driving_licence == 1) * year15
    )
    driving_licence_NA15 = database.DefineVariable(
        "driving_licence_NA15", (driving_licence < 0) * year15
    )
    driving_licence_not_NA21 = database.DefineVariable(
        "driving_licence_not_NA21", (driving_licence == 1) * year21
    )
    driving_licence_NA21 = database.DefineVariable(
        "driving_licence_NA21", (driving_licence < 0) * year21
    )

    nb_cars_not_NA15 = database.DefineVariable(
        "nb_cars_not_NA15",
        ((nb_cars >= 0) * nb_cars) * year15
        # "nb_cars_not_NA15", ((nb_cars >= 0) * bioMax(nb_cars, 3)) * year15
    )
    nb_cars_NA15 = database.DefineVariable("nb_cars_NA15", (nb_cars < 0) * year15)
    nb_cars_not_NA21 = database.DefineVariable(
        "nb_cars_not_NA21",
        ((nb_cars >= 0) * nb_cars) * year21
        # "nb_cars_not_NA21", ((nb_cars >= 0) * bioMax(nb_cars, 3)) * year21
    )
    nb_cars_NA21 = database.DefineVariable("nb_cars_NA21", (nb_cars < 0) * year21)

    german15 = database.DefineVariable("german15", (language == 1) * year15)
    german21 = database.DefineVariable("german21", (language == 1) * year21)

    accessib_pt_scaled15 = database.DefineVariable(
        "accessib_pt_scaled15", (accsib_pt / 1000000) * year15
    )
    accessib_car_scaled15 = database.DefineVariable(
        "accessib_car_scaled15", (accsib_car / 1000000) * year15
    )
    accessib_multi_scaled15 = database.DefineVariable(
        "accessib_multi_scaled15", (accsib_mul / 1000000) * year15
    )
    accessib_pt_scaled21 = database.DefineVariable(
        "accessib_pt_scaled21", (accsib_pt / 1000000) * year21
    )
    accessib_car_scaled21 = database.DefineVariable(
        "accessib_car_scaled21", (accsib_car / 1000000) * year21
    )
    accessib_multi_scaled21 = database.DefineVariable(
        "accessib_multi_scaled21", (accsib_mul / 1000000) * year21
    )

    boxcox_accessib_pt15 = database.DefineVariable(
        "boxcox_accessib_pt15", ((accessib_pt_scaled15**0.1552 - 1) / 0.1552) * year15
    )
    boxcox_accessib_car15 = database.DefineVariable(
        "boxcox_accessib_car15",
        ((accessib_car_scaled15**0.1741 - 1) / 0.1741) * year15,
    )
    boxcox_accsib_mul15 = database.DefineVariable(
        "boxcox_accsib_mul15",
        ((accessib_multi_scaled15**0.1973 - 1) / 0.1973) * year15,
    )
    boxcox_accessib_pt21 = database.DefineVariable(
        "boxcox_accessib_pt21", ((accessib_pt_scaled21**0.1552 - 1) / 0.1552) * year21
    )
    boxcox_accessib_car21 = database.DefineVariable(
        "boxcox_accessib_car21",
        ((accessib_car_scaled21**0.1741 - 1) / 0.1741) * year21,
    )
    boxcox_accsib_mul21 = database.DefineVariable(
        "boxcox_accsib_mul21",
        ((accessib_multi_scaled21**0.1973 - 1) / 0.1973) * year21,
    )

    cars_per_adult15 = database.DefineVariable(
        "cars_per_adult15", (nb_cars_not_NA15 / nb_adults) * year15
    )
    cars_per_adult21 = database.DefineVariable(
        "cars_per_adult21", (nb_cars_not_NA21 / nb_adults) * year21
    )

    urban15 = database.DefineVariable("urban15", (W_stadt_land_2012 == 1) * year15)
    urban21 = database.DefineVariable("urban21", (W_stadt_land_2012 == 1) * year21)

    couple_without_children15 = database.DefineVariable(
        "couple_without_children15", (hhtyp == 210) * year15
    )
    couple_without_children21 = database.DefineVariable(
        "couple_without_children21", (hhtyp == 210) * year21
    )

    couple_with_children15 = database.DefineVariable(
        "couple_with_children15", (hhtyp == 220) * year15
    )
    couple_with_children21 = database.DefineVariable(
        "couple_with_children21", (hhtyp == 220) * year21
    )

    single_parent_house15 = database.DefineVariable(
        "single_parent_house15", (hhtyp == 230) * year15
    )
    single_parent_house21 = database.DefineVariable(
        "single_parent_house21", (hhtyp == 230) * year21
    )

    one_person_household15 = database.DefineVariable(
        "one_person_household15", (hhtyp == 10) * year15
    )
    one_person_household21 = database.DefineVariable(
        "one_person_household21", (hhtyp == 10) * year21
    )

    household_type_NA15 = database.DefineVariable(
        "household_type_NA15", (hhtyp < 0) * year15
    )
    household_type_NA21 = database.DefineVariable(
        "household_type_NA21", (hhtyp < 0) * year21
    )


def get_dict_betas(
    estimate_2015: bool, estimate_2021: bool, estimate_2015_2021: bool
) -> dict:
    # General betas
    dict_betas = {
        "ASC_NONE": Beta("ASC_NONE", 0, None, None, 1),
        "ASC_GA": Beta("ASC_GA", 1.53, None, None, 0),
        "ASC_HT": Beta("ASC_HT", 2.06, None, None, 0),
        "ASC_V": Beta("ASC_V", 6.68, None, None, 0),
        "ASC_HTV": Beta("ASC_HTV", 5.65, None, None, 0),
    }
    if estimate_2015:
        print("Using 2015 betas...")
        dict_betas["b_CARS_PER_ADULT_GA15"] = Beta(
            "B_CARS_PER_ADULT_GA15", 0, None, None, 0
        )
        dict_betas["b_CARS_PER_ADULT_V15"] = Beta(
            "B_CARS_PER_ADULT_V15", 0, None, None, 0
        )
        dict_betas["b_CARS_PER_ADULT_HTV15"] = Beta(
            "B_CARS_PER_ADULT_HTV15", 0, None, None, 0
        )

        dict_betas["b_OWNS_DL_NONE15"] = Beta("B_OWNS_DL_NONE15", 0, None, None, 0)
        dict_betas["b_OWNS_DL_NONE_NA15"] = Beta(
            "B_OWNS_DL_NONE_NA15", 0, None, None, 0
        )

        dict_betas["b_NB_CARS_HH_HT_ALL15"] = Beta(
            "B_NB_CARS_HH_HT_ALL15", 0, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_HT_ALL_NA15"] = Beta(
            "B_NB_CARS_HH_HT_ALL_NA15", 0, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_V15"] = Beta("B_NB_CARS_HH_V15", 0, None, None, 1)
        dict_betas["b_NB_CARS_HH_V_NA15"] = Beta(
            "B_NB_CARS_HH_V_NA15", 0, None, None, 1
        )

        dict_betas["b_LANG_GERMAN_GA15"] = Beta("B_LANG_GERMAN_GA15", 0, None, None, 0)
        dict_betas["b_LANG_GERMAN_HT15"] = Beta("B_LANG_GERMAN_HT15", 0, None, None, 0)
        dict_betas["b_LANG_GERMAN_V15"] = Beta("B_LANG_GERMAN_V15", 0, None, None, 0)
        dict_betas["b_LANG_GERMAN_HTV15"] = Beta(
            "B_LANG_GERMAN_HTV15", 0, None, None, 0
        )

        dict_betas["b_ACCESSIB_CAR_NONE15"] = Beta(
            "B_ACCESSIB_CAR_NONE15", 0, None, None, 0
        )
        dict_betas["b_ACCESSIB_MULTI_NONE15"] = Beta(
            "B_ACCESSIB_MULTI_NONE15", 0, None, None, 0
        )
        dict_betas["b_ACCESSIB_PT_HT15"] = Beta("B_ACCESSIB_PT_HT15", 0, None, None, 0)
        dict_betas["b_ACCESSIB_PT_HTV15"] = Beta(
            "B_ACCESSIB_PT_HTV15", 0, None, None, 0
        )

        dict_betas["b_is_swiss_GA15"] = Beta("B_is_swiss_GA15", 0, None, None, 0)
        dict_betas["b_is_swiss_HT15"] = Beta("B_is_swiss_HT15", 0, None, None, 0)
        dict_betas["b_is_swiss_V15"] = Beta("B_is_swiss_V15", 0, None, None, 1)
        dict_betas["b_is_swiss_htv15"] = Beta("b_is_swiss_htv15", 0, None, None, 0)

        dict_betas["b_URBAN_V_ALL15"] = Beta("B_URBAN_V_ALL15", 0, None, None, 0)

        dict_betas["b_FULLTIME_GA15"] = Beta("B_FULLTIME_GA15", 0, None, None, 0)
        dict_betas["b_FULLTIME_HTV15"] = Beta("B_FULLTIME_HTV15", 0, None, None, 0)

        dict_betas["b_PARTTIME_GA15"] = Beta("B_PARTTIME_GA15", 0, None, None, 0)
        dict_betas["b_PARTTIME_HT_ALL15"] = Beta(
            "B_TYPE_2_PARTTIME_HT15", 0, None, None, 0
        )
        dict_betas["b_PARTTIME_V15"] = Beta("B_PARTTIME_V15", 0, None, None, 0)

        dict_betas["b_AGE_18_22_GA15"] = Beta("B_AGE_18_22_GA15", 0, None, None, 0)
        dict_betas["b_AGE_23_26_GA15"] = Beta("B_AGE_23_26_GA15", 0, None, None, 0)
        dict_betas["b_AGE_27_69_GA15"] = Beta("B_AGE_27_69_GA15", 0, None, None, 0)
        dict_betas["b_AGE_70_89_GA15"] = Beta("B_AGE_70_89_GA15", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_GA15"] = Beta("B_AGE_90_plus_GA15", 0, None, None, 0)
        dict_betas["b_AGE_18_22_HT15"] = Beta("B_AGE_18_22_HT15", 0, None, None, 0)
        dict_betas["b_AGE_23_26_HT15"] = Beta("B_AGE_23_26_HT15", 0, None, None, 0)
        dict_betas["b_AGE_27_69_HT15"] = Beta("B_AGE_27_69_HT15", 0, None, None, 0)
        dict_betas["b_AGE_70_89_HT15"] = Beta("B_AGE_70_89_HT15", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_HT15"] = Beta("B_AGE_90_plus_HT15", 0, None, None, 0)
        dict_betas["b_AGE_18_22_V15"] = Beta("B_AGE_18_22_V15", 0, None, None, 0)
        dict_betas["b_AGE_23_26_V15"] = Beta("B_AGE_23_26_V15", 0, None, None, 0)
        dict_betas["b_AGE_27_69_V15"] = Beta("B_AGE_27_69_V15", 0, None, None, 0)
        dict_betas["b_AGE_70_89_V15"] = Beta("B_AGE_70_89_V15", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_V15"] = Beta("B_AGE_90_plus_V15", 0, None, None, 0)
        dict_betas["b_AGE_18_22_HTV15"] = Beta("B_AGE_18_22_HTV15", 0, None, None, 0)
        dict_betas["b_AGE_23_26_HTV15"] = Beta("B_AGE_23_26_HTV15", 0, None, None, 0)
        dict_betas["b_AGE_27_69_HTV15"] = Beta("B_AGE_27_69_HTV15", 0, None, None, 0)
        dict_betas["b_AGE_70_89_HTV15"] = Beta("B_AGE_70_89_HTV15", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_HTV15"] = Beta(
            "B_AGE_90_plus_HTV15", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_GA15"] = Beta(
            "b_couple_without_children_GA15", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_GA15"] = Beta(
            "b_couple_with_children_GA15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_GA15"] = Beta(
            "b_single_parent_house_GA15", 0, None, None, 0
        )
        dict_betas["b_one_person_household_GA15"] = Beta(
            "b_one_person_household_GA15", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_GA15"] = Beta(
            "b_household_type_NA_GA15", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_HT15"] = Beta(
            "b_couple_without_children_HT15", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_HT15"] = Beta(
            "b_couple_with_children_HT15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT15"] = Beta(
            "b_single_parent_house_HT15", 0, None, None, 0
        )
        dict_betas["b_one_person_household_HT15"] = Beta(
            "b_one_person_household_HT15", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HT15"] = Beta(
            "b_household_type_NA_HT15", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_V15"] = Beta(
            "b_couple_without_children_V15", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_V15"] = Beta(
            "b_couple_with_children_V15", 0, None, None, 0
        )
        dict_betas["b_single_parent_house_V15"] = Beta(
            "b_single_parent_house_V15", 0, None, None, 0
        )
        dict_betas["b_one_person_household_V15"] = Beta(
            "b_one_person_household_V15", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_V15"] = Beta(
            "b_household_type_NA_V15", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_HTV15"] = Beta(
            "b_couple_without_children_HTV15", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_HTV15"] = Beta(
            "b_couple_with_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV15"] = Beta(
            "b_single_parent_house_HTV15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HTV15"] = Beta(
            "b_one_person_household_HTV15", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HTV15"] = Beta(
            "b_household_type_NA_HTV15", 0, None, None, 0
        )

        dict_betas["b_CARS_PER_ADULT_GA21"] = Beta(
            "B_CARS_PER_ADULT_GA21", 0, None, None, 1
        )
        dict_betas["b_CARS_PER_ADULT_V21"] = Beta(
            "B_CARS_PER_ADULT_V21", 0, None, None, 1
        )
        dict_betas["b_CARS_PER_ADULT_HTV21"] = Beta(
            "B_CARS_PER_ADULT_HTV21", 0, None, None, 1
        )

        dict_betas["b_OWNS_DL_NONE21"] = Beta("B_OWNS_DL_NONE21", 0, None, None, 1)
        dict_betas["b_OWNS_DL_NONE_NA21"] = Beta(
            "B_OWNS_DL_NONE_NA21", 0, None, None, 1
        )

        dict_betas["b_NB_CARS_HH_HT_ALL21"] = Beta(
            "B_NB_CARS_HH_HT_ALL21", 0, None, None, 1
        )
        dict_betas["b_NB_CARS_HH_HT_ALL_NA21"] = Beta(
            "B_NB_CARS_HH_HT_ALL_NA21", 0, None, None, 1
        )
        dict_betas["b_NB_CARS_HH_V21"] = Beta("B_NB_CARS_HH_V21", 0, None, None, 1)
        dict_betas["b_NB_CARS_HH_V_NA21"] = Beta(
            "B_NB_CARS_HH_V_NA21", 0, None, None, 1
        )

        dict_betas["b_LANG_GERMAN_GA21"] = Beta("B_LANG_GERMAN_GA21", 0, None, None, 1)
        dict_betas["b_LANG_GERMAN_HT21"] = Beta("B_LANG_GERMAN_HT21", 0, None, None, 1)
        dict_betas["b_LANG_GERMAN_V21"] = Beta("B_LANG_GERMAN_V21", 0, None, None, 1)
        dict_betas["b_LANG_GERMAN_HTV21"] = Beta(
            "B_LANG_GERMAN_HTV21", 0, None, None, 1
        )

        dict_betas["b_ACCESSIB_CAR_NONE21"] = Beta("B_ACCESSIB_CAR21", 0, None, None, 1)
        dict_betas["b_ACCESSIB_MULTI_NONE21"] = Beta(
            "B_ACCESSIB_MULTI_NONE21", 0, None, None, 1
        )
        dict_betas["b_ACCESSIB_PT_HT21"] = Beta("B_ACCESSIB_PT_HT21", 0, None, None, 1)
        dict_betas["b_ACCESSIB_PT_HTV21"] = Beta(
            "B_ACCESSIB_PT_HTV21", 0, None, None, 1
        )

        dict_betas["b_is_swiss_GA21"] = Beta("B_is_swiss_GA21", 0, None, None, 1)
        dict_betas["b_is_swiss_HT21"] = Beta("B_is_swiss_HT21", 0, None, None, 1)
        dict_betas["b_is_swiss_V21"] = Beta("B_is_swiss_V21", 0, None, None, 1)
        dict_betas["b_is_swiss_htv21"] = Beta("b_is_swiss_htv21", 0, None, None, 1)

        dict_betas["b_URBAN_V_ALL21"] = Beta("B_URBAN_V_ALL21", 0, None, None, 1)

        dict_betas["b_FULLTIME_GA21"] = Beta("B_FULLTIME_GA21", 0, None, None, 1)
        dict_betas["b_FULLTIME_HTV21"] = Beta("B_FULLTIME_HTV21", 0, None, None, 1)

        dict_betas["b_PARTTIME_GA21"] = Beta("B_PARTTIME_GA21", 0, None, None, 1)
        dict_betas["b_PARTTIME_HT_ALL21"] = Beta(
            "B_TYPE_2_PARTTIME_HT21", 0, None, None, 1
        )
        dict_betas["b_PARTTIME_V21"] = Beta("B_PARTTIME_V21", 0, None, None, 1)

        dict_betas["b_AGE_18_22_GA21"] = Beta("B_AGE_18_22_GA21", 0, None, None, 1)
        dict_betas["b_AGE_23_26_GA21"] = Beta("B_AGE_23_26_GA21", 0, None, None, 1)
        dict_betas["b_AGE_27_69_GA21"] = Beta("B_AGE_27_69_GA21", 0, None, None, 1)
        dict_betas["b_AGE_70_89_GA21"] = Beta("B_AGE_70_89_GA21", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_GA21"] = Beta("B_AGE_90_plus_GA21", 0, None, None, 1)
        dict_betas["b_AGE_18_22_HT21"] = Beta("B_AGE_18_22_HT21", 0, None, None, 1)
        dict_betas["b_AGE_23_26_HT21"] = Beta("B_AGE_23_26_HT21", 0, None, None, 1)
        dict_betas["b_AGE_27_69_HT21"] = Beta("B_AGE_27_69_HT21", 0, None, None, 1)
        dict_betas["b_AGE_70_89_HT21"] = Beta("B_AGE_70_89_HT21", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_HT21"] = Beta("B_AGE_90_plus_HT21", 0, None, None, 1)
        dict_betas["b_AGE_18_22_V21"] = Beta("B_AGE_18_22_V21", 0, None, None, 1)
        dict_betas["b_AGE_23_26_V21"] = Beta("B_AGE_23_26_V21", 0, None, None, 1)
        dict_betas["b_AGE_27_69_V21"] = Beta("B_AGE_27_69_V21", 0, None, None, 1)
        dict_betas["b_AGE_70_89_V21"] = Beta("B_AGE_70_89_V21", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_V21"] = Beta("B_AGE_90_plus_V21", 0, None, None, 1)
        dict_betas["b_AGE_18_22_HTV21"] = Beta("B_AGE_18_22_HTV21", 0, None, None, 1)
        dict_betas["b_AGE_23_26_HTV21"] = Beta("B_AGE_23_26_HTV21", 0, None, None, 1)
        dict_betas["b_AGE_27_69_HTV21"] = Beta("B_AGE_27_69_HTV21", 0, None, None, 1)
        dict_betas["b_AGE_70_89_HTV21"] = Beta("B_AGE_70_89_HTV21", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_HTV21"] = Beta(
            "B_AGE_90_plus_HTV21", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_GA21"] = Beta(
            "b_couple_without_children_GA21", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_GA21"] = Beta(
            "b_couple_with_children_GA21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_GA21"] = Beta(
            "b_single_parent_house_GA21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_GA21"] = Beta(
            "b_one_person_household_GA21", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_GA21"] = Beta(
            "b_household_type_NA_GA21", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_HT21"] = Beta(
            "b_couple_without_children_HT21", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_HT21"] = Beta(
            "b_couple_with_children_HT21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT21"] = Beta(
            "b_single_parent_house_HT21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HT21"] = Beta(
            "b_one_person_household_HT21", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_HT21"] = Beta(
            "b_household_type_NA_HT21", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_V21"] = Beta(
            "b_couple_without_children_V21", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_V21"] = Beta(
            "b_couple_with_children_V21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_V21"] = Beta(
            "b_single_parent_house_V21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_V21"] = Beta(
            "b_one_person_household_V21", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_V21"] = Beta(
            "b_household_type_NA_V21", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_HTV21"] = Beta(
            "b_couple_without_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_HTV21"] = Beta(
            "b_couple_with_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV21"] = Beta(
            "b_single_parent_house_HTV21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HTV21"] = Beta(
            "b_one_person_household_HTV21", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_HTV21"] = Beta(
            "b_household_type_NA_HTV21", 0, None, None, 1
        )

        dict_betas["mu_2021"] = Beta("mu_2021", 0, None, None, 1)
    elif estimate_2021:
        print("Using 2021 betas...")
        dict_betas["b_CARS_PER_ADULT_GA15"] = Beta(
            "B_CARS_PER_ADULT_GA15", 0, None, None, 1
        )
        dict_betas["b_CARS_PER_ADULT_V15"] = Beta(
            "B_CARS_PER_ADULT_V15", 0, None, None, 1
        )
        dict_betas["b_CARS_PER_ADULT_HTV15"] = Beta(
            "B_CARS_PER_ADULT_HTV15", 0, None, None, 1
        )

        dict_betas["b_OWNS_DL_NONE15"] = Beta("B_OWNS_DL_NONE15", 0, None, None, 1)
        dict_betas["b_OWNS_DL_NONE_NA15"] = Beta(
            "B_OWNS_DL_NONE_NA15", 0, None, None, 1
        )

        dict_betas["b_NB_CARS_HH_HT_ALL15"] = Beta(
            "B_NB_CARS_HH_HT_ALL15", 0, None, None, 1
        )
        dict_betas["b_NB_CARS_HH_HT_ALL_NA15"] = Beta(
            "B_NB_CARS_HH_HT_ALL_NA15", 0, None, None, 1
        )
        dict_betas["b_NB_CARS_HH_V15"] = Beta("B_NB_CARS_HH_V15", 0, None, None, 1)
        dict_betas["b_NB_CARS_HH_V_NA15"] = Beta(
            "B_NB_CARS_HH_V_NA15", 0, None, None, 1
        )

        dict_betas["b_LANG_GERMAN_GA15"] = Beta("B_LANG_GERMAN_GA15", 0, None, None, 1)
        dict_betas["b_LANG_GERMAN_HT15"] = Beta("B_LANG_GERMAN_HT15", 0, None, None, 1)
        dict_betas["b_LANG_GERMAN_V15"] = Beta("B_LANG_GERMAN_V15", 0, None, None, 1)
        dict_betas["b_LANG_GERMAN_HTV15"] = Beta(
            "B_LANG_GERMAN_HTV15", 0, None, None, 1
        )

        dict_betas["b_ACCESSIB_CAR_NONE15"] = Beta("B_ACCESSIB_CAR15", 0, None, None, 1)
        dict_betas["b_ACCESSIB_MULTI_NONE15"] = Beta(
            "B_ACCESSIB_MULTI_NONE15", 0, None, None, 1
        )
        dict_betas["b_ACCESSIB_PT_HT15"] = Beta("B_ACCESSIB_PT_HT15", 0, None, None, 1)
        dict_betas["b_ACCESSIB_PT_HTV15"] = Beta(
            "B_ACCESSIB_PT_HTV15", 0, None, None, 1
        )

        dict_betas["b_is_swiss_GA15"] = Beta("B_is_swiss_GA15", 0, None, None, 1)
        dict_betas["b_is_swiss_HT15"] = Beta("B_is_swiss_HT15", 0, None, None, 1)
        dict_betas["b_is_swiss_V15"] = Beta("B_is_swiss_V15", 0, None, None, 1)
        dict_betas["b_is_swiss_htv15"] = Beta("b_is_swiss_htv15", 0, None, None, 1)

        dict_betas["b_URBAN_V_ALL15"] = Beta("B_URBAN_V_ALL15", 0, None, None, 1)

        dict_betas["b_FULLTIME_GA15"] = Beta("B_FULLTIME_GA15", 0, None, None, 1)
        dict_betas["b_FULLTIME_HTV15"] = Beta("B_FULLTIME_HTV15", 0, None, None, 1)

        dict_betas["b_PARTTIME_GA15"] = Beta("B_PARTTIME_GA15", 0, None, None, 1)
        dict_betas["b_PARTTIME_HT_ALL15"] = Beta("B_PARTTIME_HT15", 0, None, None, 1)
        dict_betas["b_PARTTIME_V15"] = Beta("B_PARTTIME_V15", 0, None, None, 1)

        dict_betas["b_AGE_18_22_GA15"] = Beta("B_AGE_18_22_GA15", 0, None, None, 1)
        dict_betas["b_AGE_23_26_GA15"] = Beta("B_AGE_23_26_GA15", 0, None, None, 1)
        dict_betas["b_AGE_27_69_GA15"] = Beta("B_AGE_27_69_GA15", 0, None, None, 1)
        dict_betas["b_AGE_70_89_GA15"] = Beta("B_AGE_70_89_GA15", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_GA15"] = Beta("B_AGE_90_plus_GA15", 0, None, None, 1)
        dict_betas["b_AGE_18_22_HT15"] = Beta("B_AGE_18_22_HT15", 0, None, None, 1)
        dict_betas["b_AGE_23_26_HT15"] = Beta("B_AGE_23_26_HT15", 0, None, None, 1)
        dict_betas["b_AGE_27_69_HT15"] = Beta("B_AGE_27_69_HT15", 0, None, None, 1)
        dict_betas["b_AGE_70_89_HT15"] = Beta("B_AGE_70_89_HT15", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_HT15"] = Beta("B_AGE_90_plus_HT15", 0, None, None, 1)
        dict_betas["b_AGE_18_22_V15"] = Beta("B_AGE_18_22_V15", 0, None, None, 1)
        dict_betas["b_AGE_23_26_V15"] = Beta("B_AGE_23_26_V15", 0, None, None, 1)
        dict_betas["b_AGE_27_69_V15"] = Beta("B_AGE_27_69_V15", 0, None, None, 1)
        dict_betas["b_AGE_70_89_V15"] = Beta("B_AGE_70_89_V15", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_V15"] = Beta("B_AGE_90_plus_V15", 0, None, None, 1)
        dict_betas["b_AGE_18_22_HTV15"] = Beta("B_AGE_18_22_HTV15", 0, None, None, 1)
        dict_betas["b_AGE_23_26_HTV15"] = Beta("B_AGE_23_26_HTV15", 0, None, None, 1)
        dict_betas["b_AGE_27_69_HTV15"] = Beta("B_AGE_27_69_HTV15", 0, None, None, 1)
        dict_betas["b_AGE_70_89_HTV15"] = Beta("B_AGE_70_89_HTV15", 0, None, None, 1)
        dict_betas["b_AGE_90_plus_HTV15"] = Beta(
            "B_AGE_90_plus_HTV15", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_GA15"] = Beta(
            "b_couple_without_children_GA15", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_GA15"] = Beta(
            "b_couple_with_children_GA15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_GA15"] = Beta(
            "b_single_parent_house_GA15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_GA15"] = Beta(
            "b_one_person_household_GA15", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_GA15"] = Beta(
            "b_household_type_NA_GA15", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_HT15"] = Beta(
            "b_couple_without_children_HT15", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_HT15"] = Beta(
            "b_couple_with_children_HT15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT15"] = Beta(
            "b_single_parent_house_HT15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HT15"] = Beta(
            "b_one_person_household_HT15", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_HT15"] = Beta(
            "b_household_type_NA_HT15", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_V15"] = Beta(
            "b_couple_without_children_V15", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_V15"] = Beta(
            "b_couple_with_children_V15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_V15"] = Beta(
            "b_single_parent_house_V15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_V15"] = Beta(
            "b_one_person_household_V15", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_V15"] = Beta(
            "b_household_type_NA_V15", 0, None, None, 1
        )

        dict_betas["b_couple_without_children_HTV15"] = Beta(
            "b_couple_without_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_couple_with_children_HTV15"] = Beta(
            "b_couple_with_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV15"] = Beta(
            "b_single_parent_house_HTV15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HTV15"] = Beta(
            "b_one_person_household_HTV15", 0, None, None, 1
        )
        dict_betas["b_household_type_NA_HTV15"] = Beta(
            "b_household_type_NA_HTV15", 0, None, None, 1
        )

        dict_betas["b_CARS_PER_ADULT_GA21"] = Beta(
            "B_CARS_PER_ADULT_GA21", 0, None, None, 0
        )
        dict_betas["b_CARS_PER_ADULT_V21"] = Beta(
            "B_CARS_PER_ADULT_V21", 0, None, None, 0
        )
        dict_betas["b_CARS_PER_ADULT_HTV21"] = Beta(
            "B_CARS_PER_ADULT_HTV21", 0, None, None, 0
        )

        dict_betas["b_OWNS_DL_NONE21"] = Beta("B_OWNS_DL_NONE21", 0, None, None, 0)
        dict_betas["b_OWNS_DL_NONE_NA21"] = Beta(
            "B_OWNS_DL_NONE_NA21", 0, None, None, 0
        )

        dict_betas["b_NB_CARS_HH_HT_ALL21"] = Beta(
            "B_NB_CARS_HH_HT_ALL21", 0, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_HT_ALL_NA21"] = Beta(
            "B_NB_CARS_HH_HT_ALL_NA21", 0, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_V21"] = Beta("B_NB_CARS_HH_V21", 0, None, None, 0)
        dict_betas["b_NB_CARS_HH_V_NA21"] = Beta(
            "B_NB_CARS_HH_V_NA21", 0, None, None, 0
        )

        dict_betas["b_LANG_GERMAN_GA21"] = Beta("B_LANG_GERMAN_GA21", 0, None, None, 0)
        dict_betas["b_LANG_GERMAN_HT21"] = Beta("B_LANG_GERMAN_HT21", 0, None, None, 0)
        dict_betas["b_LANG_GERMAN_V21"] = Beta("B_LANG_GERMAN_V21", 0, None, None, 0)
        dict_betas["b_LANG_GERMAN_HTV21"] = Beta(
            "B_LANG_GERMAN_HTV21", 0, None, None, 0
        )

        dict_betas["b_ACCESSIB_CAR_NONE21"] = Beta(
            "B_ACCESSIB_CAR_NONE21", 0, None, None, 0
        )
        dict_betas["b_ACCESSIB_MULTI_NONE21"] = Beta(
            "B_ACCESSIB_MULTI_NONE21", 0, None, None, 0
        )
        dict_betas["b_ACCESSIB_PT_HT21"] = Beta("B_ACCESSIB_PT_HT21", 0, None, None, 0)
        dict_betas["b_ACCESSIB_PT_HTV21"] = Beta(
            "B_ACCESSIB_PT_HTV21", 0, None, None, 0
        )

        dict_betas["b_is_swiss_GA21"] = Beta("B_is_swiss_GA21", 0, None, None, 0)
        dict_betas["b_is_swiss_HT21"] = Beta("B_is_swiss_HT21", 0, None, None, 0)
        dict_betas["b_is_swiss_V21"] = Beta("B_is_swiss_V21", 0, None, None, 1)
        dict_betas["b_is_swiss_htv21"] = Beta("b_is_swiss_htv21", 0, None, None, 0)

        dict_betas["b_URBAN_V_ALL21"] = Beta("B_URBAN_V_ALL21", 0, None, None, 0)

        dict_betas["b_FULLTIME_GA21"] = Beta("B_FULLTIME_GA21", 0, None, None, 0)
        dict_betas["b_FULLTIME_HTV21"] = Beta("B_FULLTIME_HTV21", 0, None, None, 0)

        dict_betas["b_PARTTIME_GA21"] = Beta("B_PARTTIME_GA21", 0, None, None, 0)
        dict_betas["b_PARTTIME_HT_ALL21"] = Beta(
            "B_PARTTIME_HT_ALL21", 0, None, None, 0
        )
        dict_betas["b_PARTTIME_V21"] = Beta("B_PARTTIME_V21", 0, None, None, 0)

        dict_betas["b_AGE_18_22_GA21"] = Beta("B_AGE_18_22_GA21", 0, None, None, 0)
        dict_betas["b_AGE_23_26_GA21"] = Beta("B_AGE_23_26_GA21", 0, None, None, 0)
        dict_betas["b_AGE_27_69_GA21"] = Beta("B_AGE_27_69_GA21", 0, None, None, 0)
        dict_betas["b_AGE_70_89_GA21"] = Beta("B_AGE_70_89_GA21", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_GA21"] = Beta("B_AGE_90_plus_GA21", 0, None, None, 0)
        dict_betas["b_AGE_18_22_HT21"] = Beta("B_AGE_18_22_HT21", 0, None, None, 0)
        dict_betas["b_AGE_23_26_HT21"] = Beta("B_AGE_23_26_HT21", 0, None, None, 0)
        dict_betas["b_AGE_27_69_HT21"] = Beta("B_AGE_27_69_HT21", 0, None, None, 0)
        dict_betas["b_AGE_70_89_HT21"] = Beta("B_AGE_70_89_HT21", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_HT21"] = Beta("B_AGE_90_plus_HT21", 0, None, None, 0)
        dict_betas["b_AGE_18_22_V21"] = Beta("B_AGE_18_22_V21", 0, None, None, 0)
        dict_betas["b_AGE_23_26_V21"] = Beta("B_AGE_23_26_V21", 0, None, None, 0)
        dict_betas["b_AGE_27_69_V21"] = Beta("B_AGE_27_69_V21", 0, None, None, 0)
        dict_betas["b_AGE_70_89_V21"] = Beta("B_AGE_70_89_V21", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_V21"] = Beta("B_AGE_90_plus_V21", 0, None, None, 0)
        dict_betas["b_AGE_18_22_HTV21"] = Beta("B_AGE_18_22_HTV21", 0, None, None, 0)
        dict_betas["b_AGE_23_26_HTV21"] = Beta("B_AGE_23_26_HTV21", 0, None, None, 0)
        dict_betas["b_AGE_27_69_HTV21"] = Beta("B_AGE_27_69_HTV21", 0, None, None, 0)
        dict_betas["b_AGE_70_89_HTV21"] = Beta("B_AGE_70_89_HTV21", 0, None, None, 0)
        dict_betas["b_AGE_90_plus_HTV21"] = Beta(
            "B_AGE_90_plus_HTV21", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_GA21"] = Beta(
            "b_couple_without_children_GA21", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_GA21"] = Beta(
            "b_couple_with_children_GA21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_GA21"] = Beta(
            "b_single_parent_house_GA21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_GA21"] = Beta(
            "b_one_person_household_GA21", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_GA21"] = Beta(
            "b_household_type_NA_GA21", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_HT21"] = Beta(
            "b_couple_without_children_HT21", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_HT21"] = Beta(
            "b_couple_with_children_HT21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT21"] = Beta(
            "b_single_parent_house_HT21", 0, None, None, 0
        )
        dict_betas["b_one_person_household_HT21"] = Beta(
            "b_one_person_household_HT21", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HT21"] = Beta(
            "b_household_type_NA_HT21", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_V21"] = Beta(
            "b_couple_without_children_V21", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_V21"] = Beta(
            "b_couple_with_children_V21", 0, None, None, 0
        )
        dict_betas["b_single_parent_house_V21"] = Beta(
            "b_single_parent_house_V21", 0, None, None, 0
        )
        dict_betas["b_one_person_household_V21"] = Beta(
            "b_one_person_household_V21", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_V21"] = Beta(
            "b_household_type_NA_V21", 0, None, None, 0
        )

        dict_betas["b_couple_without_children_HTV21"] = Beta(
            "b_couple_without_children_HTV21", 0, None, None, 0
        )
        dict_betas["b_couple_with_children_HTV21"] = Beta(
            "b_couple_with_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV21"] = Beta(
            "b_single_parent_house_HTV21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HTV21"] = Beta(
            "b_one_person_household_HTV21", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HTV21"] = Beta(
            "b_household_type_NA_HTV21", 0, None, None, 0
        )

        dict_betas["mu_2021"] = Beta("mu_2021", 1, None, None, 1)
    elif estimate_2015_2021:
        dict_betas["mu_2021"] = Beta("mu_2021", 1.03, None, None, 0)

        dict_betas["b_CARS_PER_ADULT_GA1521"] = Beta(
            "B_CARS_PER_ADULT_GA1521", -1.75, None, None, 0
        )
        dict_betas["b_CARS_PER_ADULT_V1521"] = Beta(
            "B_CARS_PER_ADULT_V1521", -1.51, None, None, 0
        )
        dict_betas["b_CARS_PER_ADULT_HTV1521"] = Beta(
            "B_CARS_PER_ADULT_HTV1521", -1.39, None, None, 0
        )

        dict_betas["b_OWNS_DL_NONE1521"] = Beta(
            "B_OWNS_DL_NONE1521", 0.215, None, None, 0
        )
        dict_betas["b_OWNS_DL_NONE_NA1521"] = Beta(
            "B_OWNS_DL_NONE_NA1521", 0.522, None, None, 0
        )

        dict_betas["b_NB_CARS_HH_HT_ALL1521"] = Beta(
            "B_NB_CARS_HH_HT_ALL1521", -0.243, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_HT_ALL_NA1521"] = Beta(
            "B_NB_CARS_HH_HT_ALL_NA1521", -0.801, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_GA_V1521"] = Beta(
            "B_NB_CARS_HH_GA_V1521", -0.133, None, None, 0
        )
        dict_betas["b_NB_CARS_HH_GA_V_NA1521"] = Beta(
            "B_NB_CARS_HH_GA_V_NA1521", -0.142, None, None, 0
        )

        dict_betas["b_LANG_GERMAN_GA1521"] = Beta(
            "B_LANG_GERMAN_GA1521", 0.887, None, None, 0
        )
        dict_betas["b_LANG_GERMAN_HT1521"] = Beta(
            "B_LANG_GERMAN_HT1521", 0.838, None, None, 0
        )
        dict_betas["b_LANG_GERMAN_V1521"] = Beta(
            "B_LANG_GERMAN_V1521", -0.208, None, None, 0
        )
        dict_betas["b_LANG_GERMAN_HTV15"] = Beta(
            "B_LANG_GERMAN_HTV15", 0.891, None, None, 0
        )

        dict_betas["b_ACCESSIB_CAR_NONE15"] = Beta(
            "B_ACCESSIB_CAR_NONE15", 1.41, None, None, 0
        )
        dict_betas["b_ACCESSIB_MULTI_NONE15"] = Beta(
            "B_ACCESSIB_MULTI_NONE15", -1.98, None, None, 0
        )
        dict_betas["b_ACCESSIB_PT_HT1521"] = Beta(
            "B_ACCESSIB_PT_HT1521", 0, None, None, 0
        )
        dict_betas["b_ACCESSIB_PT_HTV15"] = Beta(
            "B_ACCESSIB_PT_HTV15", -0.332, None, None, 0
        )

        dict_betas["b_is_swiss_GA1521"] = Beta("B_is_swiss_GA1521", 1.16, None, None, 0)
        dict_betas["b_is_swiss_HT15"] = Beta("B_is_swiss_HT15", 0.833, None, None, 0)
        dict_betas["b_is_swiss_V15"] = Beta("B_is_swiss_V15", 0, None, None, 1)
        dict_betas["b_is_swiss_htv1521"] = Beta(
            "b_is_swiss_htv1521", 0.913, None, None, 0
        )

        dict_betas["b_URBAN_V_ALL1521"] = Beta(
            "B_URBAN_V_ALL1521", 0.201, None, None, 0
        )

        dict_betas["b_FULLTIME_GA1521"] = Beta(
            "B_FULLTIME_GA1521", 0.172, None, None, 0
        )
        dict_betas["b_FULLTIME_HTV1521"] = Beta(
            "B_FULLTIME_HTV1521", 0.19, None, None, 0
        )

        dict_betas["b_PARTTIME_GA1521"] = Beta("B_PARTTIME_GA1521", 0.19, None, None, 0)
        dict_betas["b_PARTTIME_HT_ALL1521"] = Beta(
            "B_PARTTIME_HT_ALL1521", 0.335, None, None, 0
        )
        dict_betas["b_PARTTIME_V1521"] = Beta("B_PARTTIME_V1521", 0.281, None, None, 0)

        dict_betas["b_AGE_18_22_GA1521"] = Beta(
            "B_AGE_18_22_GA1521", -0.0945, None, None, 0
        )
        dict_betas["b_AGE_23_26_GA1521"] = Beta(
            "B_AGE_23_26_GA1521", -0.346, None, None, 0
        )
        dict_betas["b_AGE_27_69_GA1521"] = Beta(
            "B_AGE_27_69_GA1521", -0.00619, None, None, 0
        )
        dict_betas["b_AGE_70_89_GA1521"] = Beta(
            "B_AGE_70_89_GA1521", -0.0336, None, None, 0
        )
        dict_betas["b_AGE_90_plus_GA1521"] = Beta(
            "B_AGE_90_plus_GA1521", -0.202, None, None, 0
        )
        dict_betas["b_AGE_18_22_HT1521"] = Beta(
            "B_AGE_18_22_HT1521", -0.168, None, None, 0
        )
        dict_betas["b_AGE_23_26_HT15"] = Beta(
            "B_AGE_23_26_HT15", -0.0419, None, None, 0
        )
        dict_betas["b_AGE_27_69_HT15"] = Beta("B_AGE_27_69_HT15", 0.0101, None, None, 0)
        dict_betas["b_AGE_70_89_HT1521"] = Beta(
            "B_AGE_70_89_HT1521", -0.0393, None, None, 0
        )
        dict_betas["b_AGE_90_plus_HT1521"] = Beta(
            "B_AGE_90_plus_HT1521", -0.331, None, None, 0
        )
        dict_betas["b_AGE_18_22_V1521"] = Beta("B_AGE_18_22_V1521", -0.3, None, None, 0)
        dict_betas["b_AGE_23_26_V1521"] = Beta(
            "B_AGE_23_26_V1521", -0.208, None, None, 0
        )
        dict_betas["b_AGE_27_69_V15"] = Beta("B_AGE_27_69_V15", -0.0149, None, None, 0)
        dict_betas["b_AGE_70_89_V1521"] = Beta(
            "B_AGE_70_89_V1521", -0.0134, None, None, 0
        )
        dict_betas["b_AGE_90_plus_V1521"] = Beta(
            "B_AGE_90_plus_V1521", -0.154, None, None, 0
        )
        dict_betas["b_AGE_18_22_HTV1521"] = Beta(
            "B_AGE_18_22_HTV1521", -0.315, None, None, 0
        )
        dict_betas["b_AGE_23_26_HTV1521"] = Beta(
            "B_AGE_23_26_HTV1521", -0.209, None, None, 0
        )
        dict_betas["b_AGE_27_69_HTV15"] = Beta(
            "B_AGE_27_69_HTV15", -0.00423, None, None, 0
        )
        dict_betas["b_AGE_70_89_HTV15"] = Beta(
            "B_AGE_70_89_HTV15", -0.0309, None, None, 0
        )
        dict_betas["b_AGE_90_plus_HTV1521"] = Beta(
            "B_AGE_90_plus_HTV1521", -0.184, None, None, 0
        )

        dict_betas["b_couple_without_children_GA1521"] = Beta(
            "b_couple_without_children_GA1521", 0.259, None, None, 0
        )
        dict_betas["b_couple_with_children_GA15"] = Beta(
            "b_couple_with_children_GA15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_GA1521"] = Beta(
            "b_single_parent_house_GA1521", -0.193, None, None, 0
        )
        dict_betas["b_one_person_household_GA1521"] = Beta(
            "b_one_person_household_GA1521", 0.388, None, None, 0
        )
        dict_betas["b_household_type_NA_GA1521"] = Beta(
            "b_household_type_NA_GA1521", -0.701, None, None, 0
        )

        dict_betas["b_couple_without_children_HT1521"] = Beta(
            "b_couple_without_children_HT1521", 0.218, None, None, 0
        )
        dict_betas["b_couple_with_children_HT15"] = Beta(
            "b_couple_with_children_HT15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT1521"] = Beta(
            "b_single_parent_house_HT1521", -0.208, None, None, 0
        )
        dict_betas["b_one_person_household_HT1521"] = Beta(
            "b_one_person_household_HT1521", 0.0815, None, None, 0
        )
        dict_betas["b_household_type_NA_HT1521"] = Beta(
            "b_household_type_NA_HT1521", -0.0872, None, None, 0
        )

        dict_betas["b_couple_without_children_V1521"] = Beta(
            "b_couple_without_children_V1521", 0.268, None, None, 0
        )
        dict_betas["b_couple_with_children_V1521"] = Beta(
            "b_couple_with_children_V1521", 0.286, None, None, 0
        )
        dict_betas["b_single_parent_house_V1521"] = Beta(
            "b_single_parent_house_V1521", 0.261, None, None, 0
        )
        dict_betas["b_one_person_household_V1521"] = Beta(
            "b_one_person_household_V1521", 0.553, None, None, 0
        )
        dict_betas["b_household_type_NA_V1521"] = Beta(
            "b_household_type_NA_V1521", 0.268, None, None, 0
        )

        dict_betas["b_couple_without_children_HTV1521"] = Beta(
            "b_couple_without_children_HTV1521", 0.432, None, None, 0
        )
        dict_betas["b_couple_with_children_HTV15"] = Beta(
            "b_couple_with_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV1521"] = Beta(
            "b_single_parent_house_HTV1521", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HTV1521"] = Beta(
            "b_one_person_household_HTV1521", 0.686, None, None, 0
        )
