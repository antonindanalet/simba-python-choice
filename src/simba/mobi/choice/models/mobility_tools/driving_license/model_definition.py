import biogeme
from biogeme.expressions import Beta
from biogeme.expressions import logzero
from biogeme.expressions import Variable


def define_variables(
    database: biogeme.database.Database, estimate_2015_2020_2021: bool
) -> None:
    globals().update(database.variables)

    # General variables
    driving_licence = Variable("driving_licence")
    is_swiss = Variable("is_swiss")
    pc_car = Variable("pc_car")
    age = Variable("age")
    language = Variable("language")
    accessibility_public_transport = Variable("accsib_pt")
    accessibility_multimodal = Variable("accsib_mul")
    parking_cost_car = Variable("pc_car")
    full_time = Variable("full_time")
    part_time = Variable("part_time")
    hhtyp = Variable("hhtyp")
    parking_cost_car_log = database.DefineVariable(
        "parking_cost_car_log", logzero(parking_cost_car) * parking_cost_car
    )

    if estimate_2015_2020_2021:
        year = Variable("year")
        year15 = database.DefineVariable("year15", year == 2015)
        year20 = database.DefineVariable("year20", year == 2020)
        year21 = database.DefineVariable("year21", year == 2021)
        is_swiss15 = database.DefineVariable("is_swiss15", is_swiss * year15)
        is_swiss20 = database.DefineVariable("is_swiss20", is_swiss * year20)
        is_swiss21 = database.DefineVariable("is_swiss21", is_swiss * year21)
        pc_car15 = database.DefineVariable("pc_car15", pc_car * year15)
        pc_car20 = database.DefineVariable("pc_car20", pc_car * year20)
        pc_car21 = database.DefineVariable("pc_car21", pc_car * year21)
        age15 = database.DefineVariable("age15", age * year15)
        age20 = database.DefineVariable("age20", age * year20)
        age21 = database.DefineVariable("age21", age * year21)
        parking_cost_car_log15 = database.DefineVariable(
            "parking_cost_car_log15", parking_cost_car_log * year15
        )
        parking_cost_car_log20 = database.DefineVariable(
            "parking_cost_car_log20", parking_cost_car_log * year20
        )
        parking_cost_car_log21 = database.DefineVariable(
            "parking_cost_car_log21", parking_cost_car_log * year21
        )

        full_time15 = database.DefineVariable("full_time15", full_time * year15)
        full_time20 = database.DefineVariable("full_time20", full_time * year20)
        full_time21 = database.DefineVariable("full_time21", full_time * year21)
        part_time15 = database.DefineVariable("part_time15", part_time * year15)
        part_time20 = database.DefineVariable("part_time20", part_time * year20)
        part_time21 = database.DefineVariable("part_time21", part_time * year21)

        french15 = database.DefineVariable("french15", (language == 2) * year15)
        french20 = database.DefineVariable("french20", (language == 2) * year20)
        french21 = database.DefineVariable("french21", (language == 2) * year21)
        free_parking_car15 = database.DefineVariable(
            "free_parking_car15", (pc_car == 0) * year15
        )
        free_parking_car20 = database.DefineVariable(
            "free_parking_car20", (pc_car == 0) * year20
        )
        free_parking_car21 = database.DefineVariable(
            "free_parking_car21", (pc_car == 0) * year21
        )

        accessib_pt_scaled = database.DefineVariable(
            "accessib_pt_scaled", accessibility_public_transport / 1000000
        )
        accessib_multi_scaled = database.DefineVariable(
            "accessib_multi_scaled", accessibility_multimodal / 1000000
        )

        boxcox_accessib_pt15 = database.DefineVariable(
            "boxcox_accessib_pt15",
            ((accessib_pt_scaled**0.1774 - 1) / 0.1774) * year15,
        )
        boxcox_accessib_pt20 = database.DefineVariable(
            "boxcox_accessib_pt20",
            ((accessib_pt_scaled**0.1774 - 1) / 0.1774) * year20,
        )
        boxcox_accessib_pt21 = database.DefineVariable(
            "boxcox_accessib_pt21",
            ((accessib_pt_scaled**0.1774 - 1) / 0.1774) * year21,
        )

        boxcox_accessib_multi15 = database.DefineVariable(
            "boxcox_accessib_multi15",
            ((accessib_multi_scaled**0.1448 - 1) / 0.1448) * year15,
        )
        boxcox_accessib_multi20 = database.DefineVariable(
            "boxcox_accessib_multi20",
            ((accessib_multi_scaled**0.1448 - 1) / 0.1448) * year20,
        )
        boxcox_accessib_multi21 = database.DefineVariable(
            "boxcox_accessib_multi21",
            ((accessib_multi_scaled**0.1448 - 1) / 0.1448) * year21,
        )

        couple_with_children15 = database.DefineVariable(
            "couple_with_children15", (hhtyp == 220) * year15
        )
        couple_with_children20 = database.DefineVariable(
            "couple_with_children20", (hhtyp == 220) * year20
        )
        couple_with_children21 = database.DefineVariable(
            "couple_with_children21", (hhtyp == 220) * year21
        )

        couple_without_children15 = database.DefineVariable(
            "couple_without_children15", (hhtyp == 210) * year15
        )
        couple_without_children20 = database.DefineVariable(
            "couple_without_children20", (hhtyp == 210) * year20
        )
        couple_without_children21 = database.DefineVariable(
            "couple_without_children21", (hhtyp == 210) * year21
        )

        single_parent_house15 = database.DefineVariable(
            "single_parent_house15", (hhtyp == 230) * year15
        )
        single_parent_house20 = database.DefineVariable(
            "single_parent_house20", (hhtyp == 230) * year20
        )
        single_parent_house21 = database.DefineVariable(
            "single_parent_house21", (hhtyp == 230) * year21
        )

        household_type_NA15 = database.DefineVariable(
            "household_type_NA15", (hhtyp < 0) * year15
        )
        household_type_NA20 = database.DefineVariable(
            "household_type_NA20", (hhtyp < 0) * year20
        )
        household_type_NA21 = database.DefineVariable(
            "household_type_NA21", (hhtyp < 0) * year21
        )
    else:
        french = database.DefineVariable("french", (language == 2))
        free_parking_car = database.DefineVariable("free_parking_car", (pc_car == 0))
        accessib_pt_scaled = database.DefineVariable(
            "accessib_pt_scaled", accessibility_public_transport / 1000000
        )
        accessib_multi_scaled = database.DefineVariable(
            "accessib_multi_scaled", accessibility_multimodal / 1000000
        )

        boxcox_accessib_pt = database.DefineVariable(
            "boxcox_accessib_pt", ((accessib_pt_scaled**0.1774 - 1) / 0.1774)
        )
        boxcox_accessib_multi = database.DefineVariable(
            "boxcox_accessib_multi", ((accessib_multi_scaled**0.1448 - 1) / 0.1448)
        )

        couple_with_children = database.DefineVariable(
            "couple_with_children", hhtyp == 220
        )
        couple_without_children = database.DefineVariable(
            "couple_without_children", hhtyp == 210
        )
        single_parent_house = database.DefineVariable(
            "single_parent_house", hhtyp == 230
        )
        household_type_NA = database.DefineVariable("household_type_NA", hhtyp < 0)


def get_dict_betas(estimate_2015_2020_2021: bool) -> dict:
    # General betas
    dict_betas = {
        "ASC_DL": Beta("ASC_DL", 0, None, None, 0),
        "B_PARTTIME152021": Beta("B_PARTTIME152021", 0, None, None, 0),
        "B_FULLTIME152021": Beta("B_FULLTIME152021", 0, None, None, 0),
        "B_ACCESSIB_PT152021": Beta("B_ACCESSIB_PT152021", 0, None, None, 0),
        "B_ACCESSIB_MULTI152021": Beta("B_ACCESSIB_MULTI152021", 0, None, None, 0),
        "B_parking_cost_car152021": Beta("B_parking_cost_car152021", 0, None, None, 0),
        "B_parking_cost_car_log152021": Beta(
            "B_parking_cost_car_log152021", 0, None, None, 0
        ),
        "B_free_parking_car152021": Beta("B_free_parking_car152021", 0, None, None, 0),
        "B_is_swiss152021": Beta("B_is_swiss152021", 0, None, None, 0),
        "B_LANG_FRENCH152021": Beta("B_LANG_FRENCH152021", 0, None, None, 0),
    }

    if estimate_2015_2020_2021:
        dict_betas["B_PARTTIME152021"] = Beta("B_PARTTIME152021", 0, None, None, 0)
        dict_betas["B_FULLTIME152021"] = Beta("B_FULLTIME152021", 0, None, None, 0)

        dict_betas["B_ACCESSIB_PT152021"] = Beta(
            "B_ACCESSIB_PT152021", 0, None, None, 0
        )
        dict_betas["B_ACCESSIB_MULTI152021"] = Beta(
            "B_ACCESSIB_MULTI152021", 0, None, None, 0
        )

        dict_betas["B_parking_cost_car152021"] = Beta(
            "B_parking_cost_car152021", 0, None, None, 0
        )
        dict_betas["B_parking_cost_car_log152021"] = Beta(
            "B_parking_cost_car_log152021", 0, None, None, 0
        )
        dict_betas["B_free_parking_car152021"] = Beta(
            "B_free_parking_car152021", 0, None, None, 0
        )

        dict_betas["B_is_swiss152021"] = Beta("B_is_swiss152021", 0, None, None, 0)

        dict_betas["B_LANG_FRENCH152021"] = Beta(
            "B_LANG_FRENCH152021", 0, None, None, 0
        )

        dict_betas["beta_age152021_0_22"] = Beta(
            "beta_age152021_0_22", 0, None, None, 0
        )
        dict_betas["beta_age1520_23_26"] = Beta("beta_age1520_23_26", 0, None, None, 0)
        dict_betas["beta_age1520_27_69"] = Beta("beta_age1520_27_69", 0, None, None, 0)
        dict_betas["beta_age1520_70_89"] = Beta("beta_age1520_70_89", 0, None, None, 0)
        dict_betas["beta_age152021_90_120"] = Beta(
            "beta_age152021_90_120", 0, None, None, 0
        )

        dict_betas["beta_age21_23_26"] = Beta("beta_age21_23_26", 0, None, None, 1)
        dict_betas["beta_age21_27_69"] = Beta("beta_age21_27_69", 0, None, None, 0)
        dict_betas["beta_age21_70_89"] = Beta("beta_age21_70_89", 0, None, None, 0)

        dict_betas["beta_couple_with_children152021"] = Beta(
            "beta_couple_with_children152021", 0, None, None, 0
        )

        dict_betas["beta_couple_without_children152021"] = Beta(
            "beta_couple_without_children152021", 0, None, None, 0
        )

        dict_betas["beta_single_parent_house15"] = Beta(
            "beta_single_parent_house15", 0, None, None, 1
        )
        dict_betas["beta_single_parent_house20"] = Beta(
            "beta_single_parent_house20", 0, None, None, 1
        )
        dict_betas["beta_single_parent_house21"] = Beta(
            "beta_single_parent_house21", 0, None, None, 1
        )

        # dict_betas["beta_one_person_household15"] = Beta('beta_one_person_household15', 0, None, None, 1)
        # dict_betas["beta_one_person_household20"] = Beta('beta_one_person_household20', 0, None, None, 1)
        # dict_betas["beta_one_person_household21"] = Beta('beta_one_person_household21', 0, None, None, 1)

        dict_betas["beta_household_type_NA15"] = Beta(
            "beta_household_type_NA15", 0, None, None, 0
        )
        dict_betas["beta_household_type_NA20"] = Beta(
            "beta_household_type_NA20", 0, None, None, 0
        )
        dict_betas["beta_household_type_NA21"] = Beta(
            "beta_household_type_NA21", 0, None, None, 0
        )

        dict_betas["mu_2020"] = Beta("mu_2020", 1, 0.001, None, 0)
        dict_betas["mu_2021"] = Beta("mu_2021", 1, 0.001, None, 0)
    else:
        dict_betas["beta_couple_with_children"] = Beta(
            "beta_couple_with_children", 0, None, None, 0
        )
        dict_betas["beta_couple_without_children"] = Beta(
            "beta_couple_without_children", 0, None, None, 0
        )
        dict_betas["beta_single_parent_house"] = Beta(
            "beta_single_parent_house", 0, None, None, 1
        )
        # dict_betas["beta_one_person_household"] = Beta('beta_one_person_household', 0, None, None, 1)
        dict_betas["beta_household_type_NA"] = Beta(
            "beta_household_type_NA", 0, None, None, 0
        )

        dict_betas["beta_age_0_22"] = Beta("beta_age_0_22", 0, None, None, 0)
        dict_betas["beta_age_23_26"] = Beta("beta_age_23_26", 0, None, None, 0)
        dict_betas["beta_age_27_69"] = Beta("beta_age_27_69", 0, None, None, 0)
        dict_betas["beta_age_70_89"] = Beta("beta_age_70_89", 0, None, None, 0)
        dict_betas["beta_age_90_120"] = Beta("beta_age_90_120", 0, None, None, 0)
    return dict_betas
