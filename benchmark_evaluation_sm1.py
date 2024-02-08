from baas_utilities import read_csv_to_list
import pprint

import matplotlib.pyplot as plt
import numpy as np

pp = pprint.PrettyPrinter(indent=0.5)

evaluation_names = ["service_model_1_heuristic", "service_model_1_milp"]
#evaluation_names = ["service_model_2_heuristic", "service_model_2_milp"]

num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30]
#num_apps_ops = [3, 5]
num_list_per_size = 10

def read_benchmark_results(eval_names, aps_ops, amount_per_list):
    apps_dictionary = {}
    algo_names = []
    for eval_name in eval_names:
        for num_apps in aps_ops:
            if num_apps not in apps_dictionary.keys():
                apps_dictionary[num_apps] = {}
            for num_per_app in range(amount_per_list):
                if num_per_app not in apps_dictionary[num_apps].keys():
                    apps_dictionary[num_apps][num_per_app] = {}
                fname = "./data/benchmark_results/"+eval_name+"/res_app_list_"+str(num_apps)+"_"+str(num_per_app)+".csv"
                data = read_csv_to_list(fname)
                for x in data:
                    if x[0] not in algo_names:
                        algo_names.append(x[0])
                    apps_dictionary[num_apps][num_per_app][x[0]] = {"execution-time-ms": float(x[1]), 
                                                                    "verification": int(x[2]), 
                                                                    "comment": x[3],
                                                                    "num-apps-assigned": int(x[4]),
                                                                    "num-replicas-assigned": int(x[5]),
                                                                    "min-lat": float(x[6]),
                                                                    "avg-lat": float(x[7]),
                                                                    "max-lat": float(x[8]),
                                                                    "min-lat-from-constraint": float(x[9]),
                                                                    "avg-lat-from-constraint": float(x[10]),
                                                                    "max-lat-from-constraint": float(x[11])}
    return (algo_names, apps_dictionary)

(algos_tested, benchmark_results) = read_benchmark_results(evaluation_names, num_apps_ops, num_list_per_size)


sm1_functions_to_test_all = ["sm1_round_robin_min_sites", 
                         "sm1_closest_min_sites",
                         "sm1_best_lat_min_sites",
                         "sm1_round_robin_max_sites",
                         "sm1_closest_max_sites",
                         "sm1_best_lat_max_sites",
                         "sm1_closest_max_sites_meet_lat",
                         "sm1_best_lat_max_sites_meet_lat",
                         "sm1_milp_max_sites"]

sm1_functions_to_test_min_sites = ["sm1_round_robin_min_sites", 
                         "sm1_closest_min_sites",
                         "sm1_best_lat_min_sites",
                         "sm1_milp_max_sites"]

sm1_functions_to_test_max_sites = ["sm1_round_robin_max_sites",
                         "sm1_closest_max_sites",
                         "sm1_best_lat_max_sites",
                         "sm1_milp_max_sites"]

sm1_functions_to_test_max_sites_meet_lat = ["sm1_closest_max_sites_meet_lat",
                         "sm1_best_lat_max_sites_meet_lat",
                         "sm1_milp_max_sites"]

optimal_algo = "sm1_milp_max_sites"

function_sets_to_test = {"all": sm1_functions_to_test_all, 
                         "min_sites": sm1_functions_to_test_min_sites, 
                         "max_sites": sm1_functions_to_test_max_sites, 
                         "max_sites_meet_lat": sm1_functions_to_test_max_sites_meet_lat}


fig_apps = plt.figure(figsize=(18, 8), layout="constrained")
fig_apps.suptitle("Service Model 1: Cumulative distributions of Number of Apps (right is better)")
axs_apps = fig_apps.subplots(2, 2, sharex=True, sharey=True)

fig_replicas = plt.figure(figsize=(18, 8), layout="constrained")
fig_replicas.suptitle("Service Model 1: Cumulative distributions of Number of Replicas (left is better)")
axs_replicas = fig_replicas.subplots(2, 2, sharex=True, sharey=True)

fig_time = plt.figure(figsize=(18, 8), layout="constrained")
fig_time.suptitle("Service Model 1: Cumulative distributions of Execution Time (left is better)")
axs_time = fig_time.subplots(2, 2, sharex=True, sharey=True)

fig_violations = plt.figure(figsize=(18, 8), layout="constrained")
fig_violations.suptitle("Service Model 1: Cumulative distributions of Number of Verified Placements (right is better)")
axs_violations = fig_violations.subplots(2, 2, sharex=True, sharey=True)

fig_row = 0
fig_col = 0

for function_set in function_sets_to_test.keys():

    algos_tested = function_sets_to_test[function_set]

    data_apps = {}
    data_replicas = {}
    data_time = {}
    data_lat = {}
    data_verified_placements = {}

    for alg in algos_tested:
        data_apps[alg] = []
        data_replicas[alg] = []
        data_time[alg] = []
        data_lat[alg] = []
        data_verified_placements[alg] = []

    for num_apps in num_apps_ops:
        for num_per_app in range(num_list_per_size):
            for a1 in algos_tested:
                if benchmark_results[num_apps][num_per_app][a1]["verification"]==1:

                    data_apps[a1].append((benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"])/float(benchmark_results[num_apps][num_per_app][optimal_algo]["num-apps-assigned"]))

                    data_time[a1].append((benchmark_results[num_apps][num_per_app][a1]["execution-time-ms"])/float(benchmark_results[num_apps][num_per_app][optimal_algo]["execution-time-ms"]))

                    if benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"]==benchmark_results[num_apps][num_per_app][optimal_algo]["num-apps-assigned"]:
                        data_replicas[a1].append((benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"])/float(benchmark_results[num_apps][num_per_app][optimal_algo]["num-replicas-assigned"]))
                
                data_verified_placements[a1].append(benchmark_results[num_apps][num_per_app][a1]["verification"]) #+= 1

    for a1 in algos_tested:
        axs_apps[fig_row][fig_col].ecdf(data_apps[a1], label=a1)
        axs_replicas[fig_row][fig_col].ecdf(data_replicas[a1], label=a1)
        axs_time[fig_row][fig_col].ecdf(data_time[a1], label=a1)
        axs_violations[fig_row][fig_col].ecdf(data_verified_placements[a1], label=a1)

    axs_apps[fig_row][fig_col].set_title(function_set)
    axs_apps[fig_row][fig_col].grid(True)
    axs_apps[fig_row][fig_col].legend()
    axs_apps[fig_row][fig_col].set_xlabel("Relative Performance")
    axs_apps[fig_row][fig_col].set_ylabel("Probability of Occurrence")
    axs_apps[fig_row][fig_col].label_outer()

    axs_replicas[fig_row][fig_col].set_title(function_set)
    axs_replicas[fig_row][fig_col].grid(True)
    axs_replicas[fig_row][fig_col].legend()
    axs_replicas[fig_row][fig_col].set_xlabel("Relative Performance")
    axs_replicas[fig_row][fig_col].set_ylabel("Probability of Occurrence")
    axs_replicas[fig_row][fig_col].label_outer()

    axs_time[fig_row][fig_col].set_title(function_set)
    axs_time[fig_row][fig_col].grid(True)
    axs_time[fig_row][fig_col].legend()
    axs_time[fig_row][fig_col].set_xlabel("Relative Performance")
    axs_time[fig_row][fig_col].set_ylabel("Probability of Occurrence")
    axs_time[fig_row][fig_col].label_outer()

    axs_violations[fig_row][fig_col].set_title(function_set)
    axs_violations[fig_row][fig_col].grid(True)
    axs_violations[fig_row][fig_col].legend()
    axs_violations[fig_row][fig_col].set_xlabel("Relative Performance")
    axs_violations[fig_row][fig_col].set_ylabel("Probability of Occurrence")
    axs_violations[fig_row][fig_col].label_outer()

    fig_col += 1
    if fig_col >= 2:
        fig_row += 1
        fig_col = 0

plt.show()