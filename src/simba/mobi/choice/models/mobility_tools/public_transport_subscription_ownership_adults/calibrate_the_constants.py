import math
import pickle
import sys
from pathlib import Path
from typing import Dict

import biogeme.exceptions as excep
import biogeme.results as res
import pandas as pd

from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.descriptive_stats import (
    compute_shares_of_subscriptions_from_microcensus,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.descriptive_stats import (
    compute_shares_of_subscriptions_from_register_data,
)
from simba.mobi.choice.models.mobility_tools.public_transport_subscription_ownership_adults.model_simulation import (
    run_simulation,
)


# def calibrate_the_constant_by_simulating_on_microcensus(input_directory, df_zp):
#     dict_observed_shares_of_subscriptions = compute_shares_of_subscriptions_from_microcensus(
#         input_directory
#     )
#     print("Proportion of subscriptions (MTMC):", dict_observed_shares_of_subscriptions)
#     with open(output_directory / "dict_results_validation.pickle", "rb") as pickle_file:
#         dict_predicted_shares_of_subscriptions = pickle.load(pickle_file)
#     print(
#         "Proportion of subscriptions (synpop):", dict_predicted_shares_of_subscriptions
#     )
#
#     input_data_for_simulation = input_directory / "validation_with_SynPop"
#     data_file_name_for_simulation = "persons_from_SynPop2022.pkl"
#     df_persons = pd.read_pickle(
#         input_data_for_simulation / data_file_name_for_simulation
#     )
#     try:
#         results = res.bioResults(
#             pickleFile=output_directory / "2015_2021/dcm_indivPT.pickle"
#         )
#     except excep.BiogemeError:
#         sys.exit("Could not find estimation results.")
#     betas_values = results.getBetaValues()
#     nb_of_iterations = 0
#     while (
#         abs(
#             dict_predicted_shares_of_subscriptions["Predicted share GA"]
#             - dict_observed_shares_of_subscriptions["Observed share GA"]
#         )
#         > 0.0001
#     ):
#         beta_values = update_constant(
#             betas_values,
#             dict_predicted_shares_of_subscriptions,
#             dict_observed_shares_of_subscriptions,
#         )
#         dict_predicted_shares_of_subscriptions = run_simulation(df_persons, beta_values)
#         nb_of_iterations += 1
#     print("Final alternative specific constant:", beta_values)
#     print("Number of iterations:", nb_of_iterations)
#     # return betas


def calibrate_the_constant_by_simulating_on_synthetic_population(
    input_directory, output_directory
):
    with open(output_directory / "dict_results_validation.pickle", "rb") as pickle_file:
        dict_predicted_shares_of_subscriptions = pickle.load(pickle_file)
    print(
        "Proportion of subscriptions (synpop):", dict_predicted_shares_of_subscriptions
    )
    dict_observed_shares_of_subscriptions = compute_shares_of_subscriptions()
    print(
        "Proportion of subscriptions (register data):",
        dict_observed_shares_of_subscriptions,
    )
    input_data_for_simulation = input_directory / "validation_with_SynPop"
    data_file_name_for_simulation = "persons_from_SynPop2022.pkl"
    df_persons = pd.read_pickle(
        input_data_for_simulation / data_file_name_for_simulation
    )
    try:
        results = res.bioResults(
            pickleFile=output_directory / "2015_2021/dcm_indivPT.pickle"
        )
    except excep.BiogemeError:
        sys.exit("Could not find estimation results.")
    betas_values = results.getBetaValues()
    nb_of_iterations = 0
    while (
        abs(
            dict_predicted_shares_of_subscriptions["Predicted share GA"]
            - dict_observed_shares_of_subscriptions["Observed share GA"]
        )
        > 0.0001
    ):
        beta_values = update_constant(
            betas_values,
            dict_predicted_shares_of_subscriptions,
            dict_observed_shares_of_subscriptions,
        )
        dict_predicted_shares_of_subscriptions = run_simulation(df_persons, beta_values)
        nb_of_iterations += 1
    print("Final alternative specific constant:", beta_values)
    print("Number of iterations:", nb_of_iterations)
    # return betas


def update_constant(
    betas: Dict,
    dict_predicted_shares_of_subscriptions: Dict,
    dict_observed_shares_of_subscriptions: Dict,
) -> Dict:
    for name_alternative_constant, subscription_name in [
        ("ASC_GA", "GA"),
        ("ASC_HT", "HT"),
        ("ASC_V", "V"),
        ("ASC_HTV", "HTV"),
    ]:
        # Get the value of the alternative specific constant
        alternative_specific_constant = betas[name_alternative_constant]
        # print(
        #     "Alternative specific constant", subscription_name, "before update:",
        #     alternative_specific_constant,
        # )
        # Update the value of the alternative specific constant using the heuristic method of Train (2003)
        alternative_specific_constant += math.log(
            dict_observed_shares_of_subscriptions["Observed share " + subscription_name]
        ) - math.log(
            dict_predicted_shares_of_subscriptions[
                "Predicted share " + subscription_name
            ]
        )
        # print(
        #     "Alternative specific constant", subscription_name, "after update:", alternative_specific_constant
        # )
        # Update the list of betas
        betas[name_alternative_constant] = alternative_specific_constant
    return betas
