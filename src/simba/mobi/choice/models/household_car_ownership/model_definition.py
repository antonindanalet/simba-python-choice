import biogeme
from biogeme.expressions import Beta
from biogeme.expressions import log


def define_variables(database: biogeme.database.Database) -> None:
    globals().update(database.variables)

    year15 = database.DefineVariable("year15", year == 2015)
    year21 = database.DefineVariable("year21", year == 2021)

    nb_adults15 = database.DefineVariable("nb_adults15", nb_adults * year15)
    nb_adults21 = database.DefineVariable("nb_adults21", nb_adults * year21)

    nb_children15 = database.DefineVariable("nb_children15", nb_children * year15)
    nb_children21 = database.DefineVariable("nb_children21", nb_children * year21)

    pc_car15 = database.DefineVariable("pc_car15", pc_car * year15)
    pc_car21 = database.DefineVariable("pc_car21", pc_car * year21)

    german15 = database.DefineVariable("german15", (language == 1) * year15)
    german21 = database.DefineVariable("german21", (language == 1) * year21)

    urban15 = database.DefineVariable("urban15", (W_stadt_land_2012 == 1) * year15)
    urban21 = database.DefineVariable("urban21", (W_stadt_land_2012 == 1) * year21)
    rural15 = database.DefineVariable("rural15", (W_stadt_land_2012 == 3) * year15)
    rural21 = database.DefineVariable("rural21", (W_stadt_land_2012 == 3) * year21)

    nb_driving_licences_not_na15 = database.DefineVariable(
        "nb_driving_licences_not_na15",
        year15 * nb_driving_licences * (nb_driving_licences >= 0),
    )
    nb_driving_licences_na15 = database.DefineVariable(
        "nb_driving_licences_na15", year15 * nb_driving_licences < 0
    )
    nb_driving_licences_not_na21 = database.DefineVariable(
        "nb_driving_licences_not_na21",
        year21 * nb_driving_licences * (nb_driving_licences >= 0),
    )
    nb_driving_licences_na21 = database.DefineVariable(
        "nb_driving_licences_na21", year21 * nb_driving_licences < 0
    )

    accessib_multi_scaled15 = database.DefineVariable(
        "accessib_multi_scaled15", year15 * accsib_mul / 1000000
    )
    accessib_multi_scaled21 = database.DefineVariable(
        "accessib_multi_scaled21", year21 * accsib_mul / 1000000
    )

    boxcox_accessib_car15 = database.DefineVariable(
        "boxcox_accessib_car15",
        year15 * (((accsib_car / 1000000) ** 0.066215299 - 1) / 0.066215299),
    )
    boxcox_accessib_car21 = database.DefineVariable(
        "boxcox_accessib_car21",
        year21 * (((accsib_car / 1000000) ** 0.066215299 - 1) / 0.066215299),
    )

    log_accessib_pt15 = database.DefineVariable(
        "log_accessib_pt15", log(accsib_pt) * year15
    )
    log_accessib_pt21 = database.DefineVariable(
        "log_accessib_pt21", log(accsib_pt) * year21
    )

    dls_per_adult15 = database.DefineVariable(
        "dls_per_adult15",
        (nb_adults > 0)
        * (nb_driving_licences >= 0)
        * year15
        * nb_driving_licences
        / nb_adults,
    )
    dls_per_adult21 = database.DefineVariable(
        "dls_per_adult21",
        (nb_adults > 0)
        * (nb_driving_licences >= 0)
        * year21
        * nb_driving_licences
        / nb_adults,
    )

    free_parking15 = database.DefineVariable("free_parking15", (pc_car == 0) * year15)
    free_parking21 = database.DefineVariable("free_parking21", (pc_car == 0) * year21)

    pcost_log15 = database.DefineVariable("pcost_log15", pc_car * log(pc_car) * year15)
    pcost_log21 = database.DefineVariable("pcost_log21", pc_car * log(pc_car) * year21)

    couple_with_children15 = database.DefineVariable(
        "couple_with_children15", (hhtyp == 220) * year15
    )
    couple_with_children21 = database.DefineVariable(
        "couple_with_children21", (hhtyp == 220) * year21
    )

    couple_without_children15 = database.DefineVariable(
        "couple_without_children15", (hhtyp == 210) * year15
    )
    couple_without_children21 = database.DefineVariable(
        "couple_without_children21", (hhtyp == 210) * year21
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


def get_dict_betas() -> dict:
    dict_betas = {}
    ASC_0 = Beta("ASC_0", 0, None, None, 1)
    dict_betas["ASC_0"] = ASC_0
    dict_betas["ASC_1"] = Beta("ASC_1", 0, None, None, 0)
    dict_betas["ASC_2"] = Beta("ASC_2", 0, None, None, 0)
    dict_betas["ASC_3"] = Beta("ASC_3", 0, None, None, 0)
    dict_betas["B_LANG_GERMAN_1_21"] = Beta("B_LANG_GERMAN_1_21", 0, None, None, 0)
    dict_betas["B_LANG_GERMAN_2_21"] = Beta("B_LANG_GERMAN_2_21", 0, None, None, 0)
    dict_betas["B_LANG_GERMAN_3_21"] = Beta("B_LANG_GERMAN_3_21", 0, None, None, 0)

    dict_betas["B_NB_ADULTS_1_21"] = Beta("B_NB_ADULTS_1_21", 0, None, None, 0)
    dict_betas["B_NB_ADULTS_2_21"] = Beta("B_NB_ADULTS_2_21", 0, None, None, 0)
    dict_betas["B_NB_ADULTS_3_21"] = Beta("B_NB_ADULTS_3_21", 0, None, None, 0)

    dict_betas["b_nb_children_1_21"] = Beta(
        "b_nb_children_1_21", 0, None, None, 1
    )  # Not significantly different from zero
    dict_betas["b_nb_children_2_21"] = Beta(
        "b_nb_children_2_21", 0, None, None, 1
    )  # Not significantly different from zero
    dict_betas["b_nb_children_3_21"] = Beta("b_nb_children_3_21", 0, None, None, 0)

    dict_betas["b_nb_dl_1_21"] = Beta("b_nb_dl_1_21", 0, None, None, 0)
    dict_betas["b_nb_dl_3_21"] = Beta("b_nb_dl_3_21", 0, None, None, 0)

    dict_betas["b_nb_dl_na_1_21"] = Beta("b_nb_dl_na_1_21", 0, None, None, 0)

    dict_betas["B_URBAN_1_21"] = Beta("B_URBAN_1_21", 0, None, None, 0)
    dict_betas["B_URBAN_2_21"] = Beta("B_URBAN_2_21", 0, None, None, 0)
    dict_betas["B_URBAN_3_21"] = Beta("B_URBAN_3_21", 0, None, None, 0)

    dict_betas["B_ACCESSIB_PT_1_21"] = Beta("B_ACCESSIB_PT_1_21", 0, None, None, 0)
    dict_betas["B_ACCESSIB_PT_2_21"] = Beta("B_ACCESSIB_PT_2_21", 0, None, None, 0)
    dict_betas["B_ACCESSIB_PT_3_21"] = Beta("B_ACCESSIB_PT_3_21", 0, None, None, 0)

    dict_betas["B_ACCESSIB_CAR_1_21"] = Beta("B_ACCESSIB_CAR_1_21", 0, None, None, 0)
    dict_betas["B_ACCESSIB_CAR_2_21"] = Beta("B_ACCESSIB_CAR_2_21", 0, None, None, 0)
    dict_betas["B_ACCESSIB_CAR_3_21"] = Beta("B_ACCESSIB_CAR_3_21", 0, None, None, 0)

    dict_betas["B_ACCESSIB_MULTI_1_21"] = Beta(
        "B_ACCESSIB_MULTI_1_21", 0, None, None, 0
    )
    dict_betas["B_ACCESSIB_MULTI_2_21"] = Beta(
        "B_ACCESSIB_MULTI_2_21", 0, None, None, 0
    )
    dict_betas["B_ACCESSIB_MULTI_3_21"] = Beta(
        "B_ACCESSIB_MULTI_3_21", 0, None, None, 0
    )

    dict_betas["B_DLS_PER_ADULT_1_21"] = Beta("B_DLS_PER_ADULT_1_21", 0, None, None, 0)
    dict_betas["B_DLS_PER_ADULT_2_21"] = Beta("B_DLS_PER_ADULT_2_21", 0, None, None, 0)
    dict_betas["B_DLS_PER_ADULT_3_21"] = Beta("B_DLS_PER_ADULT_3_21", 0, None, None, 0)

    dict_betas["B_PCOST_1_21"] = Beta("B_PCOST_1_21", 0, None, None, 0)
    dict_betas["B_PCOST_2_21"] = Beta("B_PCOST_2_21", 0, None, None, 0)
    dict_betas["B_PCOST_3_21"] = Beta("B_PCOST_3_21", 0, None, None, 0)

    dict_betas["B_PCOST_LOG_1_21"] = Beta("B_PCOST_LOG_1_21", 0, None, None, 0)
    dict_betas["B_PCOST_LOG_2_21"] = Beta("B_PCOST_LOG_2_21", 0, None, None, 0)
    dict_betas["B_PCOST_LOG_3_21"] = Beta("B_PCOST_LOG_3_21", 0, None, None, 0)

    dict_betas["B_PCOST_FREE_1_21"] = Beta("B_PCOST_FREE_1_21", 0, None, None, 0)
    dict_betas["B_PCOST_FREE_2_21"] = Beta("B_PCOST_FREE_2_21", 0, None, None, 0)
    dict_betas["B_PCOST_FREE_3_21"] = Beta("B_PCOST_FREE_3_21", 0, None, None, 0)

    dict_betas["B_COUPLE_CHILDREN_1_21"] = Beta(
        "B_COUPLE_CHILDREN_1_21", 0, None, None, 0
    )
    dict_betas["B_COUPLE_WITHOUT_CHILDREN_1_21"] = Beta(
        "B_COUPLE_WITHOUT_CHILDREN_1_21", 0, None, None, 0
    )

    dict_betas["B_COUPLE_CHILDREN_2_21"] = Beta(
        "B_COUPLE_CHILDREN_2_21", 0, None, None, 0
    )
    dict_betas["B_COUPLE_WITHOUT_CHILDREN_2_21"] = Beta(
        "B_COUPLE_WITHOUT_CHILDREN_2_21", 0, None, None, 0
    )

    dict_betas["B_COUPLE_CHILDREN_3_21"] = Beta(
        "B_COUPLE_CHILDREN_3_21", 0, None, None, 0
    )
    dict_betas["B_COUPLE_WITHOUT_CHILDREN_3_21"] = Beta(
        "B_COUPLE_WITHOUT_CHILDREN_3_21", 0, None, None, 0
    )

    dict_betas["B_SINGLE_PARENT_1_21"] = Beta("B_SINGLE_PARENT_1_21", 0, None, None, 0)
    dict_betas["B_ONE_PERSON_1_21"] = Beta(
        "B_ONE_PERSON_1_21", 0, None, None, 1
    )  # Not significantly different from zero
    dict_betas["B_HH_NA_1_21"] = Beta("B_HH_NA_1_21", 0, None, None, 0)

    dict_betas["B_SINGLE_PARENT_2_21"] = Beta(
        "B_SINGLE_PARENT_2_21", 0, None, None, 1
    )  # Not significantly different from zero
    dict_betas["B_ONE_PERSON_2_21"] = Beta("B_ONE_PERSON_2_21", 0, None, None, 0)
    dict_betas["B_HH_NA_2_21"] = Beta("B_HH_NA_2_21", 0, None, None, 0)

    dict_betas["B_SINGLE_PARENT_3_21"] = Beta(
        "B_SINGLE_PARENT_3_21", 0, None, None, 1
    )  # Not significantly different from zero
    dict_betas["B_ONE_PERSON_3_21"] = Beta("B_ONE_PERSON_3_21", 0, None, None, 0)
    dict_betas["B_HH_NA_3_21"] = Beta("B_HH_NA_3_21", 0, None, None, 0)

    dict_betas["B_RURAL_1_21"] = Beta("B_RURAL_1_21", 0, None, None, 1)
    dict_betas["B_RURAL_2_21"] = Beta("B_RURAL_2_21", 0, None, None, 1)
    dict_betas["B_RURAL_3_21"] = Beta("B_RURAL_3_21", 0, None, None, 1)

    dict_betas["b_nb_dl_2_21"] = Beta(
        "b_nb_dl_2_21", 0, None, None, 0
    )  # Stays 1, not significantly different from 0
    dict_betas["b_nb_dl_na_2_21"] = Beta(
        "b_nb_dl_na_2_21", 0, None, None, 1
    )  # Stays 1, since non na not significantly different from 0

    dict_betas["b_nb_dl_na_3_21"] = Beta("b_nb_dl_na_3_21", 0, None, None, 0)
    return dict_betas
