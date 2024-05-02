import biogeme
from biogeme.expressions import Beta
from biogeme.expressions import Variable


def define_variables(database: biogeme.database.Database) -> None:
    globals().update(database.variables)

    subscriptions = Variable("subscriptions")
    nb_cars = Variable("nb_cars")
    language = Variable("language")
    full_time = Variable("full_time")
    part_time = Variable("part_time")
    accsib_mul = Variable("accsib_mul")
    accsib_pt = Variable("accsib_pt")
    accsib_car = Variable("accsib_car")
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

    nb_cars_not_NA15 = database.DefineVariable(
        "nb_cars_not_NA15", ((nb_cars >= 0) * nb_cars) * year15
    )
    nb_cars_NA15 = database.DefineVariable("nb_cars_NA15", (nb_cars < 0) * year15)
    nb_cars_not_NA21 = database.DefineVariable(
        "nb_cars_not_NA21", ((nb_cars >= 0) * nb_cars) * year21
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
    boxcox_accessib_pt21 = database.DefineVariable(
        "boxcox_accessib_pt21", ((accessib_pt_scaled21**0.1552 - 1) / 0.1552) * year21
    )
    boxcox_accessib_car21 = database.DefineVariable(
        "boxcox_accessib_car21",
        ((accessib_car_scaled21**0.1741 - 1) / 0.1741) * year21,
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

    htv_av = database.DefineVariable("htv_av", age > 15)


def get_dict_betas(
    estimate_2015: bool, estimate_2021: bool, estimate_2015_2021: bool
) -> dict:
    # General betas
    dict_betas = {
        "ASC_NONE": Beta("ASC_NONE", 0, None, None, 1),
        "ASC_GA": Beta("ASC_GA", 0, None, None, 0),
        "ASC_HT": Beta("ASC_HT", 0, None, None, 0),
        "ASC_V": Beta("ASC_V", 0, None, None, 0),
        "ASC_HTV": Beta("ASC_HTV", 0, None, None, 0),
    }
    if estimate_2021:
        print("Using 2021 betas...")
        dict_betas["B_NB_CARS_HH_HT15"] = Beta("B_NB_CARS_HH_HT15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HT_NA15"] = Beta(
            "B_NB_CARS_HH_HT_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_V15"] = Beta("B_NB_CARS_HH_V15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_V_NA15"] = Beta(
            "B_NB_CARS_HH_V_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_GA15"] = Beta("B_NB_CARS_HH_GA15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_GA_NA15"] = Beta(
            "B_NB_CARS_HH_GA_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_HTV15"] = Beta("B_NB_CARS_HH_HTV15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HTV_NA15"] = Beta(
            "B_NB_CARS_HH_HTV_NA15", 0, None, None, 1
        )

        dict_betas["B_LANG_GERMAN_GA15"] = Beta("B_LANG_GERMAN_GA15", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HT15"] = Beta("B_LANG_GERMAN_HT15", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_V15"] = Beta("B_LANG_GERMAN_V15", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HTV15"] = Beta(
            "B_LANG_GERMAN_HTV15", 0, None, None, 1
        )

        dict_betas["B_ACCESSIB_CAR_GA15"] = Beta(
            "B_ACCESSIB_CAR_GA15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HT15"] = Beta(
            "B_ACCESSIB_CAR_HT15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HTV15"] = Beta(
            "B_ACCESSIB_CAR_HTV15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_V15"] = Beta("B_ACCESSIB_CAR_V15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_CAR_NONE15"] = Beta(
            "B_ACCESSIB_CAR_NONE15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_HT15"] = Beta("B_ACCESSIB_PT_HT15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_HTV15"] = Beta(
            "B_ACCESSIB_PT_HTV15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_GA15"] = Beta("B_ACCESSIB_PT_GA15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_V15"] = Beta("B_ACCESSIB_PT_V15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_MULTI_GA15"] = Beta(
            "B_ACCESSIB_MULTI_GA15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HT15"] = Beta(
            "B_ACCESSIB_MULTI_HT15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_V15"] = Beta(
            "B_ACCESSIB_MULTI_V15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HTV15"] = Beta(
            "B_ACCESSIB_MULTI_HTV15", 0, None, None, 1
        )

        dict_betas["B_is_swiss_GA15"] = Beta("B_is_swiss_GA15", 0, None, None, 1)
        dict_betas["B_is_swiss_HT15"] = Beta("B_is_swiss_HT15", 0, None, None, 1)
        dict_betas["B_is_swiss_V15"] = Beta("B_is_swiss_V15", 0, None, None, 1)
        dict_betas["b_is_swiss_htv15"] = Beta("b_is_swiss_htv15", 0, None, None, 1)

        dict_betas["B_URBAN_V15"] = Beta("B_URBAN_V15", 0, None, None, 1)
        dict_betas["B_URBAN_HTV15"] = Beta("B_URBAN_HTV15", 0, None, None, 1)
        dict_betas["B_URBAN_HT15"] = Beta("B_URBAN_HT15", 0, None, None, 1)
        dict_betas["B_URBAN_GA15"] = Beta("B_URBAN_GA15", 0, None, None, 1)

        dict_betas["B_FULLTIME_GA15"] = Beta("B_FULLTIME_GA15", 0, None, None, 1)
        dict_betas["B_FULLTIME_HT15"] = Beta("B_FULLTIME_HT15", 0, None, None, 1)
        dict_betas["B_FULLTIME_HTV15"] = Beta("B_FULLTIME_HTV15", 0, None, None, 1)
        dict_betas["B_FULLTIME_V15"] = Beta("B_FULLTIME_V15", 0, None, None, 1)

        dict_betas["B_PARTTIME_GA15"] = Beta("B_PARTTIME_GA15", 0, None, None, 1)
        dict_betas["B_PARTTIME_HT15"] = Beta("B_PARTTIME_HT15", 0, None, None, 1)
        dict_betas["B_PARTTIME_V15"] = Beta("B_PARTTIME_V15", 0, None, None, 1)
        dict_betas["B_PARTTIME_HTV15"] = Beta("B_PARTTIME_HTV15", 0, None, None, 1)

        dict_betas["beta_age15_5_12_GA"] = Beta("beta_age15_5_12_GA", 0, None, None, 1)
        dict_betas["beta_age15_12_18_GA"] = Beta(
            "beta_age15_12_18_GA", 0, None, None, 1
        )
        dict_betas["b_age15_HT"] = Beta("b_age15_HT", 0, None, None, 1)
        dict_betas["b_age15_HTV"] = Beta("b_age15_HTV", 0, None, None, 1)
        dict_betas["b_age15_V"] = Beta("b_age15_V", 0, None, None, 1)

        dict_betas["b_couple_with_children_GA15"] = Beta(
            "b_couple_with_children_GA15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_GA15"] = Beta(
            "b_couple_without_children_GA15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HT15"] = Beta(
            "b_couple_with_children_HT15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HT15"] = Beta(
            "b_couple_without_children_HT15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_V15"] = Beta(
            "b_couple_with_children_V15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_V15"] = Beta(
            "b_couple_without_children_V15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HTV15"] = Beta(
            "b_couple_with_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HTV15"] = Beta(
            "b_couple_without_children_HTV15", 0, None, None, 1
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

        dict_betas["B_NB_CARS_HH_HT21"] = Beta("B_NB_CARS_HH_HT21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HT_NA21"] = Beta(
            "B_NB_CARS_HH_HT_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_V21"] = Beta("B_NB_CARS_HH_V21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_V_NA21"] = Beta(
            "B_NB_CARS_HH_V_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_GA21"] = Beta("B_NB_CARS_HH_GA21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_GA_NA21"] = Beta(
            "B_NB_CARS_HH_GA_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_HTV21"] = Beta("B_NB_CARS_HH_HTV21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HTV_NA21"] = Beta(
            "B_NB_CARS_HH_HTV_NA21", 0, None, None, 1
        )

        dict_betas["B_LANG_GERMAN_GA21"] = Beta("B_LANG_GERMAN_GA21", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HT21"] = Beta("B_LANG_GERMAN_HT21", 0, None, None, 0)
        dict_betas["B_LANG_GERMAN_V21"] = Beta("B_LANG_GERMAN_V21", 0, None, None, 0)
        dict_betas["B_LANG_GERMAN_HTV21"] = Beta(
            "B_LANG_GERMAN_HTV21", 0, None, None, 1
        )

        dict_betas["B_ACCESSIB_CAR_GA21"] = Beta(
            "B_ACCESSIB_CAR_GA21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HT21"] = Beta(
            "B_ACCESSIB_CAR_HT21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HTV21"] = Beta(
            "B_ACCESSIB_CAR_HTV21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_V21"] = Beta("B_ACCESSIB_CAR_V21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_CAR_NONE21"] = Beta(
            "B_ACCESSIB_CAR_NONE21", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_PT_HT21"] = Beta("B_ACCESSIB_PT_HT21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_HTV21"] = Beta(
            "B_ACCESSIB_PT_HTV21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_GA21"] = Beta("B_ACCESSIB_PT_GA21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_V21"] = Beta("B_ACCESSIB_PT_V21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_MULTI_GA21"] = Beta(
            "B_ACCESSIB_MULTI_GA21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HT21"] = Beta(
            "B_ACCESSIB_MULTI_HT21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_V21"] = Beta(
            "B_ACCESSIB_MULTI_V21", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_MULTI_HTV21"] = Beta(
            "B_ACCESSIB_MULTI_HTV21", 0, None, None, 1
        )

        dict_betas["B_is_swiss_GA21"] = Beta("B_is_swiss_GA21", 0, None, None, 0)
        dict_betas["B_is_swiss_HT21"] = Beta("B_is_swiss_HT21", 0, None, None, 0)
        dict_betas["B_is_swiss_V21"] = Beta("B_is_swiss_V21", 0, None, None, 1)
        dict_betas["b_is_swiss_htv21"] = Beta("b_is_swiss_htv21", 0, None, None, 1)

        dict_betas["B_URBAN_V21"] = Beta("B_URBAN_V21", 0, None, None, 1)
        dict_betas["B_URBAN_HTV21"] = Beta("B_URBAN_HTV21", 0, None, None, 1)
        dict_betas["B_URBAN_HT21"] = Beta("B_URBAN_HT21", 0, None, None, 1)
        dict_betas["B_URBAN_GA21"] = Beta("B_URBAN_GA21", 0, None, None, 1)

        dict_betas["B_FULLTIME_GA21"] = Beta("B_FULLTIME_GA21", 0, None, None, 1)
        dict_betas["B_FULLTIME_HT21"] = Beta("B_FULLTIME_HT21", 0, None, None, 1)
        dict_betas["B_FULLTIME_HTV21"] = Beta("B_FULLTIME_HTV21", 0, None, None, 0)
        dict_betas["B_FULLTIME_V21"] = Beta("B_FULLTIME_V21", 0, None, None, 1)

        dict_betas["B_PARTTIME_GA21"] = Beta("B_PARTTIME_GA21", 0, None, None, 1)
        dict_betas["B_PARTTIME_HT21"] = Beta("B_PARTTIME_HT21", 0, None, None, 1)
        dict_betas["B_PARTTIME_V21"] = Beta("B_PARTTIME_V21", 0, None, None, 1)
        dict_betas["B_PARTTIME_HTV21"] = Beta("B_PARTTIME_HTV21", 0, None, None, 1)

        dict_betas["beta_age21_5_12_GA"] = Beta("beta_age21_5_12_GA", 0, None, None, 0)
        dict_betas["beta_age21_12_18_GA"] = Beta(
            "beta_age21_12_18_GA", 0, None, None, 0
        )
        dict_betas["b_age21_HT"] = Beta("b_age21_HT", 0, None, None, 0)
        dict_betas["b_age21_HTV"] = Beta("b_age21_HTV", 0, None, None, 0)
        dict_betas["b_age21_V"] = Beta("b_age21_V", 0, None, None, 0)

        dict_betas["b_couple_with_children_GA21"] = Beta(
            "b_couple_with_children_GA21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_GA21"] = Beta(
            "b_couple_without_children_GA21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HT21"] = Beta(
            "b_couple_with_children_HT21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HT21"] = Beta(
            "b_couple_without_children_HT21", 0, None, None, 0
        )
        dict_betas["b_single_parent_house_HT21"] = Beta(
            "b_single_parent_house_HT21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HT21"] = Beta(
            "b_one_person_household_HT21", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HT21"] = Beta(
            "b_household_type_NA_HT21", 0, None, None, 0
        )

        dict_betas["b_couple_with_children_V21"] = Beta(
            "b_couple_with_children_V21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_V21"] = Beta(
            "b_couple_without_children_V21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HTV21"] = Beta(
            "b_couple_with_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HTV21"] = Beta(
            "b_couple_without_children_HTV21", 0, None, None, 0
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
    elif estimate_2015:
        dict_betas["B_NB_CARS_HH_HT15"] = Beta("B_NB_CARS_HH_HT15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HT_NA15"] = Beta(
            "B_NB_CARS_HH_HT_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_V15"] = Beta("B_NB_CARS_HH_V15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_V_NA15"] = Beta(
            "B_NB_CARS_HH_V_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_GA15"] = Beta("B_NB_CARS_HH_GA15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_GA_NA15"] = Beta(
            "B_NB_CARS_HH_GA_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_HTV15"] = Beta("B_NB_CARS_HH_HTV15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HTV_NA15"] = Beta(
            "B_NB_CARS_HH_HTV_NA15", 0, None, None, 1
        )

        dict_betas["B_LANG_GERMAN_GA15"] = Beta("B_LANG_GERMAN_GA15", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HT15"] = Beta("B_LANG_GERMAN_HT15", 0, None, None, 0)
        dict_betas["B_LANG_GERMAN_V15"] = Beta("B_LANG_GERMAN_V15", 0, None, None, 0)
        dict_betas["B_LANG_GERMAN_HTV15"] = Beta(
            "B_LANG_GERMAN_HTV15", 0, None, None, 1
        )

        dict_betas["B_ACCESSIB_CAR_GA15"] = Beta(
            "B_ACCESSIB_CAR_GA15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HT15"] = Beta(
            "B_ACCESSIB_CAR_HT15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HTV15"] = Beta(
            "B_ACCESSIB_CAR_HTV15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_V15"] = Beta("B_ACCESSIB_CAR_V15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_CAR_NONE15"] = Beta(
            "B_ACCESSIB_CAR_NONE15", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_PT_HT15"] = Beta("B_ACCESSIB_PT_HT15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_HTV15"] = Beta(
            "B_ACCESSIB_PT_HTV15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_GA15"] = Beta("B_ACCESSIB_PT_GA15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_V15"] = Beta("B_ACCESSIB_PT_V15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_MULTI_GA15"] = Beta(
            "B_ACCESSIB_MULTI_GA15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HT15"] = Beta(
            "B_ACCESSIB_MULTI_HT15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_V15"] = Beta(
            "B_ACCESSIB_MULTI_V15", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_MULTI_HTV15"] = Beta(
            "B_ACCESSIB_MULTI_HTV15", 0, None, None, 1
        )

        dict_betas["B_is_swiss_GA15"] = Beta("B_is_swiss_GA15", 0, None, None, 0)
        dict_betas["B_is_swiss_HT15"] = Beta("B_is_swiss_HT15", 0, None, None, 0)
        dict_betas["B_is_swiss_V15"] = Beta("B_is_swiss_V15", 0, None, None, 1)
        dict_betas["b_is_swiss_htv15"] = Beta("b_is_swiss_htv15", 0, None, None, 1)

        dict_betas["B_URBAN_V15"] = Beta("B_URBAN_V15", 0, None, None, 1)
        dict_betas["B_URBAN_HTV15"] = Beta("B_URBAN_HTV15", 0, None, None, 1)
        dict_betas["B_URBAN_HT15"] = Beta("B_URBAN_HT15", 0, None, None, 1)
        dict_betas["B_URBAN_GA15"] = Beta("B_URBAN_GA15", 0, None, None, 1)

        dict_betas["B_FULLTIME_GA15"] = Beta("B_FULLTIME_GA15", 0, None, None, 1)
        dict_betas["B_FULLTIME_HT15"] = Beta("B_FULLTIME_HT15", 0, None, None, 1)
        dict_betas["B_FULLTIME_HTV15"] = Beta("B_FULLTIME_HTV15", 0, None, None, 0)
        dict_betas["B_FULLTIME_V15"] = Beta("B_FULLTIME_V15", 0, None, None, 1)

        dict_betas["B_PARTTIME_GA15"] = Beta("B_PARTTIME_GA15", 0, None, None, 1)
        dict_betas["B_PARTTIME_HT15"] = Beta("B_PARTTIME_HT15", 0, None, None, 1)
        dict_betas["B_PARTTIME_V15"] = Beta("B_PARTTIME_V15", 0, None, None, 1)
        dict_betas["B_PARTTIME_HTV15"] = Beta("B_PARTTIME_HTV15", 0, None, None, 1)

        dict_betas["beta_age15_5_12_GA"] = Beta("beta_age15_5_12_GA", 0, None, None, 0)
        dict_betas["beta_age15_12_18_GA"] = Beta(
            "beta_age15_12_18_GA", 0, None, None, 0
        )
        dict_betas["b_age15_HT"] = Beta("b_age15_HT", 0, None, None, 0)
        dict_betas["b_age15_HTV"] = Beta("b_age15_HTV", 0, None, None, 0)
        dict_betas["b_age15_V"] = Beta("b_age15_V", 0, None, None, 0)

        dict_betas["b_couple_with_children_GA15"] = Beta(
            "b_couple_with_children_GA15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_GA15"] = Beta(
            "b_couple_without_children_GA15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HT15"] = Beta(
            "b_couple_with_children_HT15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HT15"] = Beta(
            "b_couple_without_children_HT15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT15"] = Beta(
            "b_single_parent_house_HT15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HT15"] = Beta(
            "b_one_person_household_HT15", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HT15"] = Beta(
            "b_household_type_NA_HT15", 0, None, None, 0
        )

        dict_betas["b_couple_with_children_V15"] = Beta(
            "b_couple_with_children_V15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_V15"] = Beta(
            "b_couple_without_children_V15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HTV15"] = Beta(
            "b_couple_with_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HTV15"] = Beta(
            "b_couple_without_children_HTV15", 0, None, None, 1
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

        # 2021
        dict_betas["B_NB_CARS_HH_HT21"] = Beta("B_NB_CARS_HH_HT21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HT_NA21"] = Beta(
            "B_NB_CARS_HH_HT_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_V21"] = Beta("B_NB_CARS_HH_V21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_V_NA21"] = Beta(
            "B_NB_CARS_HH_V_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_GA21"] = Beta("B_NB_CARS_HH_GA21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_GA_NA21"] = Beta(
            "B_NB_CARS_HH_GA_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_HTV21"] = Beta("B_NB_CARS_HH_HTV21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HTV_NA21"] = Beta(
            "B_NB_CARS_HH_HTV_NA21", 0, None, None, 1
        )

        dict_betas["B_LANG_GERMAN_GA21"] = Beta("B_LANG_GERMAN_GA21", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HT21"] = Beta("B_LANG_GERMAN_HT21", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_V21"] = Beta("B_LANG_GERMAN_V21", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HTV21"] = Beta(
            "B_LANG_GERMAN_HTV21", 0, None, None, 1
        )

        dict_betas["B_ACCESSIB_CAR_GA21"] = Beta(
            "B_ACCESSIB_CAR_GA21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HT21"] = Beta(
            "B_ACCESSIB_CAR_HT21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HTV21"] = Beta(
            "B_ACCESSIB_CAR_HTV21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_V21"] = Beta("B_ACCESSIB_CAR_V21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_CAR_NONE21"] = Beta(
            "B_ACCESSIB_CAR_NONE21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_HT21"] = Beta("B_ACCESSIB_PT_HT21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_HTV21"] = Beta(
            "B_ACCESSIB_PT_HTV21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_GA21"] = Beta("B_ACCESSIB_PT_GA21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_V21"] = Beta("B_ACCESSIB_PT_V21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_MULTI_GA21"] = Beta(
            "B_ACCESSIB_MULTI_GA21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HT21"] = Beta(
            "B_ACCESSIB_MULTI_HT21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_V21"] = Beta(
            "B_ACCESSIB_MULTI_V21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HTV21"] = Beta(
            "B_ACCESSIB_MULTI_HTV21", 0, None, None, 1
        )

        dict_betas["B_is_swiss_GA21"] = Beta("B_is_swiss_GA21", 0, None, None, 1)
        dict_betas["B_is_swiss_HT21"] = Beta("B_is_swiss_HT21", 0, None, None, 1)
        dict_betas["B_is_swiss_V21"] = Beta("B_is_swiss_V21", 0, None, None, 1)
        dict_betas["b_is_swiss_htv21"] = Beta("b_is_swiss_htv21", 0, None, None, 1)

        dict_betas["B_URBAN_V21"] = Beta("B_URBAN_V21", 0, None, None, 1)
        dict_betas["B_URBAN_HTV21"] = Beta("B_URBAN_HTV21", 0, None, None, 1)
        dict_betas["B_URBAN_HT21"] = Beta("B_URBAN_HT21", 0, None, None, 1)
        dict_betas["B_URBAN_GA21"] = Beta("B_URBAN_GA21", 0, None, None, 1)

        dict_betas["B_FULLTIME_GA21"] = Beta("B_FULLTIME_GA21", 0, None, None, 1)
        dict_betas["B_FULLTIME_HT21"] = Beta("B_FULLTIME_HT21", 0, None, None, 1)
        dict_betas["B_FULLTIME_HTV21"] = Beta("B_FULLTIME_HTV21", 0, None, None, 1)
        dict_betas["B_FULLTIME_V21"] = Beta("B_FULLTIME_V21", 0, None, None, 1)

        dict_betas["B_PARTTIME_GA21"] = Beta("B_PARTTIME_GA21", 0, None, None, 1)
        dict_betas["B_PARTTIME_HT21"] = Beta("B_PARTTIME_HT21", 0, None, None, 1)
        dict_betas["B_PARTTIME_V21"] = Beta("B_PARTTIME_V21", 0, None, None, 1)
        dict_betas["B_PARTTIME_HTV21"] = Beta("B_PARTTIME_HTV21", 0, None, None, 1)

        dict_betas["beta_age21_5_12_GA"] = Beta("beta_age21_5_12_GA", 0, None, None, 1)
        dict_betas["beta_age21_12_18_GA"] = Beta(
            "beta_age21_12_18_GA", 0, None, None, 1
        )
        dict_betas["b_age21_HT"] = Beta("b_age21_HT", 0, None, None, 1)
        dict_betas["b_age21_HTV"] = Beta("b_age21_HTV", 0, None, None, 1)
        dict_betas["b_age21_V"] = Beta("b_age21_V", 0, None, None, 1)

        dict_betas["b_couple_with_children_GA21"] = Beta(
            "b_couple_with_children_GA21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_GA21"] = Beta(
            "b_couple_without_children_GA21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HT21"] = Beta(
            "b_couple_with_children_HT21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HT21"] = Beta(
            "b_couple_without_children_HT21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_V21"] = Beta(
            "b_couple_with_children_V21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_V21"] = Beta(
            "b_couple_without_children_V21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HTV21"] = Beta(
            "b_couple_with_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HTV21"] = Beta(
            "b_couple_without_children_HTV21", 0, None, None, 1
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
    elif estimate_2015_2021:
        dict_betas["mu_2021"] = Beta("mu_2021", 1, 0.00001, None, 0)
        dict_betas["B_NB_CARS_HH_HT21"] = Beta("B_NB_CARS_HH_HT21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HT_NA21"] = Beta(
            "B_NB_CARS_HH_HT_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_V21"] = Beta("B_NB_CARS_HH_V21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_V_NA21"] = Beta(
            "B_NB_CARS_HH_V_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_GA21"] = Beta("B_NB_CARS_HH_GA21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_GA_NA21"] = Beta(
            "B_NB_CARS_HH_GA_NA21", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_HTV21"] = Beta("B_NB_CARS_HH_HTV21", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HTV_NA21"] = Beta(
            "B_NB_CARS_HH_HTV_NA21", 0, None, None, 1
        )

        dict_betas["B_LANG_GERMAN_GA21"] = Beta("B_LANG_GERMAN_GA21", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HT1521"] = Beta(
            "B_LANG_GERMAN_HT1521", 0, None, None, 0
        )
        dict_betas["B_LANG_GERMAN_V1521"] = Beta(
            "B_LANG_GERMAN_V1521", 0, None, None, 0
        )
        dict_betas["B_LANG_GERMAN_HTV21"] = Beta(
            "B_LANG_GERMAN_HTV21", 0, None, None, 1
        )

        dict_betas["B_ACCESSIB_CAR_GA21"] = Beta(
            "B_ACCESSIB_CAR_GA21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HT21"] = Beta(
            "B_ACCESSIB_CAR_HT21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HTV21"] = Beta(
            "B_ACCESSIB_CAR_HTV21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_V21"] = Beta("B_ACCESSIB_CAR_V21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_CAR_NONE1521"] = Beta(
            "B_ACCESSIB_CAR_NONE1521", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_PT_HT21"] = Beta("B_ACCESSIB_PT_HT21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_HTV21"] = Beta(
            "B_ACCESSIB_PT_HTV21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_GA21"] = Beta("B_ACCESSIB_PT_GA21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_V21"] = Beta("B_ACCESSIB_PT_V21", 0, None, None, 1)
        dict_betas["B_ACCESSIB_MULTI_GA21"] = Beta(
            "B_ACCESSIB_MULTI_GA21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HT21"] = Beta(
            "B_ACCESSIB_MULTI_HT21", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_V1521"] = Beta(
            "B_ACCESSIB_MULTI_V1521", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_MULTI_HTV21"] = Beta(
            "B_ACCESSIB_MULTI_HTV21", 0, None, None, 1
        )

        dict_betas["B_is_swiss_GA1521"] = Beta("B_is_swiss_GA1521", 0, None, None, 0)
        dict_betas["B_is_swiss_HT1521"] = Beta("B_is_swiss_HT1521", 0, None, None, 0)
        dict_betas["B_is_swiss_V21"] = Beta("B_is_swiss_V21", 0, None, None, 1)
        dict_betas["b_is_swiss_htv21"] = Beta("b_is_swiss_htv21", 0, None, None, 1)

        dict_betas["B_URBAN_V21"] = Beta("B_URBAN_V21", 0, None, None, 1)
        dict_betas["B_URBAN_HTV21"] = Beta("B_URBAN_HTV21", 0, None, None, 1)
        dict_betas["B_URBAN_HT21"] = Beta("B_URBAN_HT21", 0, None, None, 1)
        dict_betas["B_URBAN_GA21"] = Beta("B_URBAN_GA21", 0, None, None, 1)

        dict_betas["B_FULLTIME_GA21"] = Beta("B_FULLTIME_GA21", 0, None, None, 1)
        dict_betas["B_FULLTIME_HT21"] = Beta("B_FULLTIME_HT21", 0, None, None, 1)
        dict_betas["B_FULLTIME_HTV21"] = Beta("B_FULLTIME_HTV21", 0, None, None, 0)
        dict_betas["B_FULLTIME_V21"] = Beta("B_FULLTIME_V21", 0, None, None, 1)

        dict_betas["B_PARTTIME_GA21"] = Beta("B_PARTTIME_GA21", 0, None, None, 1)
        dict_betas["B_PARTTIME_HT21"] = Beta("B_PARTTIME_HT21", 0, None, None, 1)
        dict_betas["B_PARTTIME_V21"] = Beta("B_PARTTIME_V21", 0, None, None, 1)
        dict_betas["B_PARTTIME_HTV21"] = Beta("B_PARTTIME_HTV21", 0, None, None, 1)

        dict_betas["beta_age21_5_12_GA"] = Beta("beta_age21_5_12_GA", 0, None, None, 1)
        dict_betas["beta_age1521_12_18_GA"] = Beta(
            "beta_age1521_12_18_GA", 0, None, None, 0
        )
        dict_betas["b_age21_HT"] = Beta("b_age21_HT", 0, None, None, 0)
        dict_betas["b_age21_HTV"] = Beta("b_age21_HTV", 0, None, None, 0)
        dict_betas["b_age21_V"] = Beta("b_age21_V", 0, None, None, 0)

        dict_betas["b_couple_with_children_GA21"] = Beta(
            "b_couple_with_children_GA21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_GA21"] = Beta(
            "b_couple_without_children_GA21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HT21"] = Beta(
            "b_couple_with_children_HT21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HT21"] = Beta(
            "b_couple_without_children_HT21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT21"] = Beta(
            "b_single_parent_house_HT21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HT21"] = Beta(
            "b_one_person_household_HT21", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HT1521"] = Beta(
            "b_household_type_NA_HT1521", 0, None, None, 0
        )

        dict_betas["b_couple_with_children_V21"] = Beta(
            "b_couple_with_children_V21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_V21"] = Beta(
            "b_couple_without_children_V21", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HTV21"] = Beta(
            "b_couple_with_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HTV21"] = Beta(
            "b_couple_without_children_HTV21", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV21"] = Beta(
            "b_single_parent_house_HTV21", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HTV1521"] = Beta(
            "b_one_person_household_HTV1521", 0, None, None, 0
        )
        dict_betas["b_household_type_NA_HTV1521"] = Beta(
            "b_household_type_NA_HTV1521", 0, None, None, 0
        )

        # 2015
        dict_betas["B_NB_CARS_HH_HT15"] = Beta("B_NB_CARS_HH_HT15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HT_NA15"] = Beta(
            "B_NB_CARS_HH_HT_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_V15"] = Beta("B_NB_CARS_HH_V15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_V_NA15"] = Beta(
            "B_NB_CARS_HH_V_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_GA15"] = Beta("B_NB_CARS_HH_GA15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_GA_NA15"] = Beta(
            "B_NB_CARS_HH_GA_NA15", 0, None, None, 1
        )
        dict_betas["B_NB_CARS_HH_HTV15"] = Beta("B_NB_CARS_HH_HTV15", 0, None, None, 1)
        dict_betas["B_NB_CARS_HH_HTV_NA15"] = Beta(
            "B_NB_CARS_HH_HTV_NA15", 0, None, None, 1
        )

        dict_betas["B_LANG_GERMAN_GA15"] = Beta("B_LANG_GERMAN_GA15", 0, None, None, 1)
        dict_betas["B_LANG_GERMAN_HTV15"] = Beta(
            "B_LANG_GERMAN_HTV15", 0, None, None, 1
        )

        dict_betas["B_ACCESSIB_CAR_GA15"] = Beta(
            "B_ACCESSIB_CAR_GA15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HT15"] = Beta(
            "B_ACCESSIB_CAR_HT15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_HTV15"] = Beta(
            "B_ACCESSIB_CAR_HTV15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_CAR_V15"] = Beta("B_ACCESSIB_CAR_V15", 0, None, None, 1)

        dict_betas["B_ACCESSIB_PT_HT15"] = Beta("B_ACCESSIB_PT_HT15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_HTV15"] = Beta(
            "B_ACCESSIB_PT_HTV15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_PT_GA15"] = Beta("B_ACCESSIB_PT_GA15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_PT_V15"] = Beta("B_ACCESSIB_PT_V15", 0, None, None, 1)
        dict_betas["B_ACCESSIB_MULTI_GA15"] = Beta(
            "B_ACCESSIB_MULTI_GA15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HT15"] = Beta(
            "B_ACCESSIB_MULTI_HT15", 0, None, None, 1
        )
        dict_betas["B_ACCESSIB_MULTI_HTV15"] = Beta(
            "B_ACCESSIB_MULTI_HTV15", 0, None, None, 1
        )

        dict_betas["B_is_swiss_V15"] = Beta("B_is_swiss_V15", 0, None, None, 1)
        dict_betas["b_is_swiss_htv15"] = Beta("b_is_swiss_htv15", 0, None, None, 1)

        dict_betas["B_URBAN_V15"] = Beta("B_URBAN_V15", 0, None, None, 1)
        dict_betas["B_URBAN_HTV15"] = Beta("B_URBAN_HTV15", 0, None, None, 1)
        dict_betas["B_URBAN_HT15"] = Beta("B_URBAN_HT15", 0, None, None, 1)
        dict_betas["B_URBAN_GA15"] = Beta("B_URBAN_GA15", 0, None, None, 1)

        dict_betas["B_FULLTIME_GA15"] = Beta("B_FULLTIME_GA15", 0, None, None, 1)
        dict_betas["B_FULLTIME_HT15"] = Beta("B_FULLTIME_HT15", 0, None, None, 1)
        dict_betas["B_FULLTIME_HTV15"] = Beta("B_FULLTIME_HTV15", 0, None, None, 1)
        dict_betas["B_FULLTIME_V15"] = Beta("B_FULLTIME_V15", 0, None, None, 1)

        dict_betas["B_PARTTIME_GA15"] = Beta("B_PARTTIME_GA15", 0, None, None, 1)
        dict_betas["B_PARTTIME_HT15"] = Beta("B_PARTTIME_HT15", 0, None, None, 1)
        dict_betas["B_PARTTIME_V15"] = Beta("B_PARTTIME_V15", 0, None, None, 1)
        dict_betas["B_PARTTIME_HTV15"] = Beta("B_PARTTIME_HTV15", 0, None, None, 1)

        dict_betas["beta_age15_5_12_GA"] = Beta("beta_age15_5_12_GA", 0, None, None, 0)
        dict_betas["b_age15_HT"] = Beta("b_age15_HT", 0, None, None, 0)
        dict_betas["b_age15_HTV"] = Beta("b_age15_HTV", 0, None, None, 0)
        dict_betas["b_age15_V"] = Beta("b_age15_V", 0, None, None, 0)

        dict_betas["b_couple_with_children_GA15"] = Beta(
            "b_couple_with_children_GA15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_GA15"] = Beta(
            "b_couple_without_children_GA15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HT15"] = Beta(
            "b_couple_with_children_HT15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HT15"] = Beta(
            "b_couple_without_children_HT15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HT15"] = Beta(
            "b_single_parent_house_HT15", 0, None, None, 1
        )
        dict_betas["b_one_person_household_HT15"] = Beta(
            "b_one_person_household_HT15", 0, None, None, 1
        )

        dict_betas["b_couple_with_children_V15"] = Beta(
            "b_couple_with_children_V15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_V15"] = Beta(
            "b_couple_without_children_V15", 0, None, None, 1
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

        dict_betas["b_couple_with_children_HTV15"] = Beta(
            "b_couple_with_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_couple_without_children_HTV15"] = Beta(
            "b_couple_without_children_HTV15", 0, None, None, 1
        )
        dict_betas["b_single_parent_house_HTV15"] = Beta(
            "b_single_parent_house_HTV15", 0, None, None, 1
        )

    return dict_betas
