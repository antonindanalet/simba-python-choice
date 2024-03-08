import pandas as pd
from biogeme.expressions import Beta


def define_telecommuting_variable(row):
    """Defines a choice variable with value 1 if the person is allowed to telecommute
    (answer "yes" - 1 - or answer "sometimes" - 2)"""
    telecommuting = 0
    if (row["telecommuting_is_possible"] == 1) or (
        row["telecommuting_is_possible"] == 2
    ):
        telecommuting = 1
    return telecommuting


def define_variables(database: pd.DataFrame) -> None:
    globals().update(database.variables)

    #  Utility
    single_parent_with_children = database.DefineVariable(
        "single_parent_with_children", hh_type == 230
    )
    # Definition of new variables
    executives_1520 = database.DefineVariable(
        "executives_1520", (work_position == 1) * ((year == 2020) + (year == 2015))
    )
    german = database.DefineVariable("german", language == 1)

    # household attributes
    single_household = database.DefineVariable("single_household", hh_type == 10)
    number_of_children_NA = database.DefineVariable(
        "number_of_children_NA", number_of_children_less_than_21 == -999
    )
    number_of_children_not_NA = database.DefineVariable(
        "number_of_children_not_NA",
        (number_of_children_less_than_21 != -999) * number_of_children_less_than_21,
    )

    hh_income_na = database.DefineVariable("hh_income_na", hh_income < 0)
    hh_income_less_than_2000 = database.DefineVariable(
        "hh_income_less_than_2000", hh_income == 1
    )
    hh_income_2000_to_4000 = database.DefineVariable(
        "hh_income_2000_to_4000", hh_income == 2
    )
    hh_income_4001_to_6000 = database.DefineVariable(
        "hh_income_4001_to_6000", hh_income == 3
    )
    hh_income_6001_to_8000 = database.DefineVariable(
        "hh_income_6001_to_8000", hh_income == 4
    )

    # mobility tools
    general_abo_halbtax = database.DefineVariable(
        "general_abo_halbtax", (GA_ticket == 1) | (halbtax_ticket == 1)
    )

    is_falc_id_6to9_1520 = database.DefineVariable(
        "is_falc_id_6to9_1520",
        (
            business_sector_finance
            + business_sector_services_fc
            + business_sector_other_services
            + business_sector_non_movers
        )
        * ((year == 2020) + (year == 2015)),
    )
    # spatial attributes
    rural_work_1520 = database.DefineVariable(
        "rural_work_1520",
        (urban_typology_work == 3) * ((year == 2020) + (year == 2015)),
    )

    home_work_distance_car = database.DefineVariable(
        "home_work_distance_car",
        car_network_distance * (car_network_distance >= 0.0) / 1000.0,
    )
    home_work_distance_car_NA = database.DefineVariable(
        "home_work_distance_car_NA", car_network_distance < 0.0
    )

    falc_id_NA = database.DefineVariable(
        "falc_id_NA",
        (
            business_sector_agriculture
            + business_sector_retail
            + business_sector_gastronomy
            + business_sector_finance
            + business_sector_production
            + business_sector_wholesale
            + business_sector_services_fc
            + business_sector_other_services
            + business_sector_others
            + business_sector_non_movers
        )
        == 0,
    )
    accsib_home_not_NA_1520 = database.DefineVariable(
        "accsib_home_not_NA_1520",
        (accsib_mul_home * (accsib_mul_home >= 0) / 100000.0)
        * ((year == 2020) + (year == 2015)),
    )

    ### 2021 ###
    executives_21 = database.DefineVariable(
        "executives_21", (work_position == 1) * (year == 2021)
    )
    is_falc_id_6to9_21 = database.DefineVariable(
        "is_falc_id_6to9_21",
        (
            business_sector_finance
            + business_sector_services_fc
            + business_sector_other_services
            + business_sector_non_movers
        )
        * (year == 2021),
    )
    accsib_home_not_NA_21 = database.DefineVariable(
        "accsib_home_not_NA_21",
        (accsib_mul_home * (accsib_mul_home >= 0) / 100000.0) * (year == 2021),
    )

    work_percentage_15 = database.DefineVariable(
        "work_percentage_15", work_percentage * (year == 2015)
    )
    business_sector_agriculture_15 = database.DefineVariable(
        "business_sector_agriculture_15", business_sector_agriculture * (year == 2015)
    )

    work_percentage_20 = database.DefineVariable(
        "work_percentage_20", work_percentage * (year == 2020)
    )

    business_sector_agriculture_21 = database.DefineVariable(
        "business_sector_agriculture_21", business_sector_agriculture * (year == 2021)
    )
    business_sector_production_21 = database.DefineVariable(
        "business_sector_production_21", business_sector_production * (year == 2021)
    )
    business_sector_wholesale_21 = database.DefineVariable(
        "business_sector_wholesale_21", business_sector_wholesale * (year == 2021)
    )
    work_percentage_21 = database.DefineVariable(
        "work_percentage_21", work_percentage * (year == 2021)
    )
    work_percentage_20_21 = database.DefineVariable(
        "work_percentage_20_21", work_percentage * ((year == 2021) + (year == 2020))
    )
    age_21 = database.DefineVariable("age_21", age * (year == 2021))

    age_1520 = database.DefineVariable(
        "age_1520", age * ((year == 2015) + (year == 2020))
    )
    business_sector_production_1520 = database.DefineVariable(
        "business_sector_production_1520",
        business_sector_production * ((year == 2015) + (year == 2020)),
    )
    business_sector_wholesale_1520 = database.DefineVariable(
        "business_sector_wholesale_1520",
        business_sector_wholesale * ((year == 2015) + (year == 2020)),
    )


def get_dict_betas() -> dict:
    # Parameters to be estimated (global)
    dict_betas = {
        "alternative_specific_constant": Beta(
            "alternative_specific_constant", 0, None, None, 0
        ),
        "scale_2020": Beta("scale_2020", 1, 0.001, None, 0),
        "scale_2021": Beta("scale_2021", 1, 0.001, None, 0),
        # person attributes
        "b_executives_1520": Beta("b_executives_1520", 0, None, None, 0),
        "b_german": Beta("b_german", 0, None, None, 0),
        "b_no_post_school_education": Beta(
            "b_no_post_school_education", 0, None, None, 0
        ),
        "b_secondary_education": Beta("b_secondary_education", 0, None, None, 0),
        "b_tertiary_education": Beta("b_tertiary_education", 0, None, None, 0),
        # household attributes
        "b_number_of_children": Beta("b_number_of_children", 0, None, None, 0),
        "b_number_of_children_NA": Beta("b_number_of_children_NA", 0, None, None, 0),
        "b_single_household": Beta("b_single_houshold", 0, None, None, 0),
        "b_hh_income_na": Beta("b_hh_income_na", 0, None, None, 0),
        "b_hh_income_8000_or_less": Beta("b_hh_income_8000_or_less", 0, None, None, 0),
        # mobility tools
        "b_general_abo_halbtax": Beta("b_general_abo_halbtax", 0, None, None, 0),
        # work-place attributes
        "b_is_agriculture_1_15": Beta("b_is_agriculture_1_15", 0, None, None, 0),
        "b_is_production_1520": Beta("b_is_production_1520", 0, None, None, 0),
        "b_is_wohlesale_1520": Beta("b_is_wohlesale_1520", 0, None, None, 0),
        "b_is_falc_id_6to9_1520": Beta("b_is_falc_id_6to9_1", 0, None, None, 0),
        "b_falc_id_NA": Beta("b_falc_id_NA", 0, None, None, 0),
        # spatial attributes
        "b_rural_work_1520": Beta("b_rural_work_1520", 0, None, None, 0),
        "b_home_work_distance_car_NA": Beta(
            "b_home_work_distance_car_NA", 0, None, None, 0
        ),
        "b_executives_21": Beta("b_executives_21", 0, None, None, 0),
        # work-place attributes
        "b_is_agriculture_1_21": Beta("b_is_agriculture_1_21", 0, None, None, 1),
        "b_is_production_1_21": Beta("b_is_production_1_21", 0, None, None, 0),
        "b_is_wohlesale_1_21": Beta("b_is_wohlesale_1_21", 0, None, None, 0),
        "b_is_falc_id_6to9_1_21": Beta("b_is_falc_id_6to9_1_21", 0, None, None, 0),
        "beta_work_percentage_0_95_21": Beta(
            "beta_work_percentage_0_95_21", 0, None, None, 1
        ),
        "beta_work_percentage_95_101_20_21": Beta(
            "beta_work_percentage_95_101_20_21", 0, None, None, 0
        ),
        "beta_work_percentage_0_95_20": Beta(
            "beta_work_percentage_0_95_20", 0, None, None, 0
        ),
        "beta_accsib_home_not_NA_5_10_1520": Beta(
            "beta_accsib_home_not_NA_5_10_1520", 0, None, None, 0
        ),
        "beta_accsib_home_not_NA_10_24_1520": Beta(
            "beta_accsib_home_not_NA_10_24_1520", 0, None, None, 0
        ),
        "beta_accsib_home_not_NA_5_10_21": Beta(
            "beta_accsib_home_not_NA_5_10_21", 0, None, None, 0
        ),
        "beta_accsib_home_not_NA_10_24_21": Beta(
            "beta_accsib_home_not_NA_10_24_21", 0, None, None, 1
        ),
    }
    return dict_betas
