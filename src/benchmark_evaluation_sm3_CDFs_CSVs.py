from .baas_utilities import read_csv_to_list
import pprint

import matplotlib.pyplot as plt
import numpy as np
import csv

plt.rcParams.update({'font.size': 14})

pp = pprint.PrettyPrinter(indent=0.5)

#evaluation_names = ["service_model_1_heuristic", "service_model_1_milp"]
#evaluation_names = ["service_model_2_heuristic", "service_model_2_milp"]
#evaluation_names = ["service_model_2_proactive_recovery_heuristic", "service_model_2_proactive_recovery_milp_GOODRESULTS_BACKUP"]
evaluation_names = ["service_model_2_proactive_recovery_heuristic", "service_model_2_proactive_recovery_milp"]


#num_apps_ops = [3, 5, 7, 9, 11, 13, 15]
num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20]
num_list_per_size = 10

sm2_pr_functions_to_test_all = ["sm2_pr_closest_min_sites",
                         "sm2_pr_best_lat_min_sites",
                         "sm2_pr_closest_max_sites",
                         "sm2_pr_best_lat_max_sites",
                         "sm2_pr_milp_max_sites"]

sm2_pr_functions_to_test_min_sites = ["sm2_pr_closest_min_sites",
                         "sm2_pr_best_lat_min_sites",
                         "sm2_pr_milp_max_sites"]

sm2_pr_functions_to_test_max_sites = ["sm2_pr_closest_max_sites",
                         "sm2_pr_best_lat_max_sites",
                         "sm2_pr_milp_max_sites"]

# sm2_pr_functions_to_test_max_sites_meet_lat = ["sm2_pr_closest_max_sites_meet_lat",
#                          "sm2_pr_best_lat_max_sites_meet_lat",
#                          "sm2_pr_milp_max_sites"]

optimal_algo = "sm2_pr_milp_max_sites"

function_sets_to_test = {"all": sm2_pr_functions_to_test_all, 
                         "min_sites": sm2_pr_functions_to_test_min_sites, 
                         "max_sites": sm2_pr_functions_to_test_max_sites}

name_translate = {"sm2_pr_closest_min_sites": "sm3_closest_min_sites",
                    "sm2_pr_best_lat_min_sites": "sm3_best_lat_min_sites",
                    "sm2_pr_closest_max_sites": "sm3_closest_max_sites",
                    "sm2_pr_best_lat_max_sites": "sm3_best_lat_max_sites",
                    "sm2_pr_milp_max_sites": "sm3_milp_max_sites"}


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
                                                                    "num-machines-used": int(x[6]),
                                                                    "min-lat": float(x[7]),
                                                                    "avg-lat": float(x[8]),
                                                                    "max-lat": float(x[9]),
                                                                    "min-lat-from-constraint": float(x[10]),
                                                                    "avg-lat-from-constraint": float(x[11]),
                                                                    "max-lat-from-constraint": float(x[12])}
    return (algo_names, apps_dictionary)


def run():

    (algos_tested, benchmark_results) = read_benchmark_results(evaluation_names, num_apps_ops, num_list_per_size)

    fig_apps = plt.figure(figsize=(18, 8), layout="constrained")
    fig_apps.suptitle("Service Model 3: Cumulative distributions of Number of Apps (right is better)")
    axs_apps = fig_apps.subplots(2, 2, sharex=True, sharey=True)

    fig_replicas = plt.figure(figsize=(18, 8), layout="constrained")
    fig_replicas.suptitle("Service Model 3: Cumulative distributions of Number of Replicas (left is better)")
    axs_replicas = fig_replicas.subplots(2, 2, sharex=True, sharey=True)

    fig_time = plt.figure(figsize=(18, 8), layout="constrained")
    fig_time.suptitle("Service Model 3: Cumulative distributions of Execution Time (left is better)")
    axs_time = fig_time.subplots(2, 2, sharex=True, sharey=True)

    fig_violations = plt.figure(figsize=(18, 8), layout="constrained")
    fig_violations.suptitle("Service Model 3: Cumulative distributions of Number of Verified Placements (right is better)")
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

        data_apps_num_apps = {}
        data_replicas_num_apps = {}
        data_time_num_apps = {}
        data_verified_placements_num_apps = {}
        data_machines_num_apps = {}

        for alg in algos_tested:
            data_apps[alg] = []
            data_replicas[alg] = []
            data_time[alg] = []
            data_lat[alg] = []
            data_verified_placements[alg] = []

            data_time_num_apps[alg] = {}
            data_apps_num_apps[alg] = {}
            data_replicas_num_apps[alg] = {}
            data_verified_placements_num_apps[alg] = {}
            data_machines_num_apps[alg] = {}

            for num_apps in num_apps_ops:
                data_apps_num_apps[alg][num_apps] = []
                data_replicas_num_apps[alg][num_apps] = []
                data_time_num_apps[alg][num_apps] = []
                data_verified_placements_num_apps[alg][num_apps] = []
                data_machines_num_apps[alg][num_apps] = []

        for num_apps in num_apps_ops:
            for num_per_app in range(num_list_per_size):
                for a1 in algos_tested:
                    if benchmark_results[num_apps][num_per_app][a1]["verification"]==1:

                        data_apps[a1].append((benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"])/float(benchmark_results[num_apps][num_per_app][optimal_algo]["num-apps-assigned"]))
                        data_apps_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"])

                        if benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"]==benchmark_results[num_apps][num_per_app][optimal_algo]["num-apps-assigned"]:
                            data_replicas[a1].append((benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"])/float(benchmark_results[num_apps][num_per_app][optimal_algo]["num-replicas-assigned"]))
                            data_replicas_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"])
                            data_machines_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["num-machines-used"])

                    data_time[a1].append((benchmark_results[num_apps][num_per_app][a1]["execution-time-ms"])/float(benchmark_results[num_apps][num_per_app][optimal_algo]["execution-time-ms"]))
                    data_verified_placements[a1].append(benchmark_results[num_apps][num_per_app][a1]["verification"]) #+= 1

                    data_time_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["execution-time-ms"])
                    data_verified_placements_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["verification"])

        for a1 in algos_tested:
            axs_apps[fig_row][fig_col].ecdf(data_apps[a1], label=name_translate[a1])
            axs_replicas[fig_row][fig_col].ecdf(data_replicas[a1], label=name_translate[a1])
            axs_time[fig_row][fig_col].ecdf(data_time[a1], label=name_translate[a1])
            axs_violations[fig_row][fig_col].ecdf(data_verified_placements[a1], label=name_translate[a1])

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

        if function_set == "all":
            fname = "./evaluation_results/SM3_Apps.csv"
            with open(fname, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                header = ["algo_name", "number_of_apps", "Avg", "Min", "Max"]
                writer.writerow(header)
                for num_apps in num_apps_ops:
                    for a1 in algos_tested:      
                        if(len(data_apps_num_apps[a1][num_apps]) > 0):
                            temp_avg = round(sum(data_apps_num_apps[a1][num_apps]) / float(len(data_apps_num_apps[a1][num_apps])), 2)
                            temp_min = min(data_apps_num_apps[a1][num_apps])
                            temp_max = max(data_apps_num_apps[a1][num_apps])
                        else:
                            temp_avg = 0.0
                            temp_min = 0.0
                            temp_max = 0.0
                        
                        
                        to_write = [a1, num_apps, temp_avg, temp_min, temp_max]
                        writer.writerow(to_write)

            fname = "./evaluation_results/SM3_Replicas.csv"
            with open(fname, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                header = ["algo_name", "number_of_apps", "Avg", "Min", "Max"]
                writer.writerow(header)
                for num_apps in num_apps_ops:
                    for a1 in algos_tested:      
                        if(len(data_replicas_num_apps[a1][num_apps]) > 0):
                            temp_avg = round(sum(data_replicas_num_apps[a1][num_apps]) / float(len(data_replicas_num_apps[a1][num_apps])), 2)
                            temp_min = min(data_replicas_num_apps[a1][num_apps])
                            temp_max = max(data_replicas_num_apps[a1][num_apps])
                        else:
                            temp_avg = 0.0
                            temp_min = 0.0
                            temp_max = 0.0
                        
                        to_write = [a1, num_apps, temp_avg, temp_min, temp_max]
                        writer.writerow(to_write)

            fname = "./evaluation_results/SM3_Machines.csv"
            with open(fname, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                header = ["algo_name", "number_of_apps", "Avg", "Min", "Max"]
                writer.writerow(header)
                for num_apps in num_apps_ops:
                    for a1 in algos_tested:      
                        if(len(data_machines_num_apps[a1][num_apps]) > 0):
                            temp_avg = round(sum(data_machines_num_apps[a1][num_apps]) / float(len(data_machines_num_apps[a1][num_apps])), 2)
                            temp_min = min(data_machines_num_apps[a1][num_apps])
                            temp_max = max(data_machines_num_apps[a1][num_apps])
                        else:
                            temp_avg = 0.0
                            temp_min = 0.0
                            temp_max = 0.0
                        
                        to_write = [a1, num_apps, temp_avg, temp_min, temp_max]
                        writer.writerow(to_write)

            fname = "./evaluation_results/SM3_ExecutionTimes.csv"
            with open(fname, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                header = ["algo_name", "number_of_apps", "Avg", "Min", "Max"]
                writer.writerow(header)
                for num_apps in num_apps_ops:
                    for a1 in algos_tested:      
                        if(len(data_time_num_apps[a1][num_apps]) > 0):
                            temp_avg = round(sum(data_time_num_apps[a1][num_apps]) / float(len(data_time_num_apps[a1][num_apps])), 2)
                            temp_min = min(data_time_num_apps[a1][num_apps])
                            temp_max = max(data_time_num_apps[a1][num_apps])
                        else:
                            temp_avg = 0.0
                            temp_min = 0.0
                            temp_max = 0.0
                        
                        to_write = [a1, num_apps, temp_avg, temp_min, temp_max]
                        writer.writerow(to_write)

            fname = "./evaluation_results/SM3_VerifiedPlacements.csv"
            with open(fname, "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                header = ["algo_name", "number_of_apps", "Avg", "Min", "Max"]
                writer.writerow(header)
                for num_apps in num_apps_ops:
                    for a1 in algos_tested:      
                        
                        if(len(data_verified_placements_num_apps[a1][num_apps]) > 0):
                            temp_avg = round(sum(data_verified_placements_num_apps[a1][num_apps]) / float(len(data_verified_placements_num_apps[a1][num_apps])), 2)
                            temp_min = min(data_verified_placements_num_apps[a1][num_apps])
                            temp_max = max(data_verified_placements_num_apps[a1][num_apps])
                        else:
                            temp_avg = 0.0
                            temp_min = 0.0
                            temp_max = 0.0
                        
                        to_write = [a1, num_apps, temp_avg, temp_min, temp_max]
                        writer.writerow(to_write)

    #plt.show()

    plt.savefig('evaluation_results/SM3_VerifiedPlacements_CDF.png', bbox_inches='tight')
    plt.close()

    plt.savefig('evaluation_results/SM3_ExecutionTimes_CDF.png', bbox_inches='tight')
    plt.close()

    plt.savefig('evaluation_results/SM3_Replicas_CDF.png', bbox_inches='tight')
    plt.close()

    plt.savefig('evaluation_results/SM3_Apps_CDF.png', bbox_inches='tight')
    plt.close()