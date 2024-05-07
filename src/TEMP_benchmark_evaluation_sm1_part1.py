from .baas_utilities import read_csv_to_list, read_csv_to_list_with_header
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import os.path

plt.rcParams.update({'font.size': 14})

evaluation_names = ["service_model_1_heuristic", "service_model_1_milp"]
#evaluation_names = ["service_model_2_heuristic", "service_model_2_milp"]

num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30, 50, 100]
num_apps_ops_milp = [3, 5, 7, 9, 11, 13, 15, 20, 30]

#num_apps_ops = [30]
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
                if(os.path.isfile(fname)):
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

algos_tested = function_sets_to_test["all"]

data_apps_num_apps = {}
data_replicas_num_apps = {}
data_time_num_apps = {}
data_verified_placements_num_apps = {}

for alg in algos_tested:

    data_time_num_apps[alg] = {}
    data_apps_num_apps[alg] = {}
    data_replicas_num_apps[alg] = {}
    data_verified_placements_num_apps[alg] = {}

    for num_apps in num_apps_ops:
        data_apps_num_apps[alg][num_apps] = []
        data_replicas_num_apps[alg][num_apps] = []
        data_time_num_apps[alg][num_apps] = []
        data_verified_placements_num_apps[alg][num_apps] = []

for num_apps in num_apps_ops:
    for num_per_app in range(num_list_per_size):
        for a1 in algos_tested:
            if a1 in benchmark_results[num_apps][num_per_app].keys():
                if benchmark_results[num_apps][num_per_app][a1]["verification"]==1:
                    data_apps_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"])

                    if optimal_algo in benchmark_results[num_apps][num_per_app].keys():
                        if benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"]==benchmark_results[num_apps][num_per_app][optimal_algo]["num-apps-assigned"]:
                            data_replicas_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"])
                    else:
                        data_replicas_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"])

                data_time_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["execution-time-ms"])
                data_verified_placements_num_apps[a1][num_apps].append(benchmark_results[num_apps][num_per_app][a1]["verification"])

fname = "./evaluation_results/SM1_Apps.csv"
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

fname = "./evaluation_results/SM1_Replicas.csv"
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

fname = "./evaluation_results/SM1_ExecutionTimes.csv"
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

fname = "./evaluation_results/SM1_VerifiedPlacements.csv"
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


#Create the plots
fig_apps = plt.figure(figsize=(18, 8), layout="constrained")
fig_apps.suptitle("Service Model 1: Average Number of Apps (higher is better)")
axs_apps = fig_apps.subplots(2, 2, sharex=True, sharey=True)

fig_replicas = plt.figure(figsize=(18, 8), layout="constrained")
fig_replicas.suptitle("Service Model 1: Average Number of Replicas (lower is better)")
axs_replicas = fig_replicas.subplots(2, 2, sharex=True, sharey=True)

fig_time = plt.figure(figsize=(18, 8), layout="constrained")
fig_time.suptitle("Service Model 1: Average Execution Time (lower is better)")
axs_time = fig_time.subplots(2, 2, sharex=True, sharey=True)

fig_violations = plt.figure(figsize=(18, 8), layout="constrained")
fig_violations.suptitle("Service Model 1: Average Verification Score (higher is better)")
axs_violations = fig_violations.subplots(2, 2, sharex=True, sharey=True)

fig_row = 0
fig_col = 0


#Read data
fname = "./evaluation_results/SM1_Apps.csv"
data = read_csv_to_list_with_header(fname)
df_apps = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df_apps['number_of_apps'] = pd.to_numeric(df_apps['number_of_apps'])
df_apps['Avg'] = pd.to_numeric(df_apps['Avg'])
df_apps['Min'] = pd.to_numeric(df_apps['Min'])
df_apps['Max'] = pd.to_numeric(df_apps['Max'])

# Pivot the data so that each algorithm is a separate column
pivot_df_apps = df_apps.pivot(index='number_of_apps', columns='algo_name', values='Avg')
pivot_df_apps.replace(0, np.nan, inplace=True)


#Read data
fname = "./evaluation_results/SM1_Replicas.csv"
data = read_csv_to_list_with_header(fname)
df_replicas = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df_replicas['number_of_apps'] = pd.to_numeric(df_replicas['number_of_apps'])
df_replicas['Avg'] = pd.to_numeric(df_replicas['Avg'])
df_replicas['Min'] = pd.to_numeric(df_replicas['Min'])
df_replicas['Max'] = pd.to_numeric(df_replicas['Max'])

# Pivot the data so that each algorithm is a separate column
pivot_df_replicas = df_replicas.pivot(index='number_of_apps', columns='algo_name', values='Avg')
pivot_df_replicas.replace(0, np.nan, inplace=True)


#Read data
fname = "./evaluation_results/SM1_ExecutionTimes.csv"
data = read_csv_to_list_with_header(fname)
df_time = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df_time['number_of_apps'] = pd.to_numeric(df_time['number_of_apps'])
df_time['Avg'] = pd.to_numeric(df_time['Avg'])
df_time['Min'] = pd.to_numeric(df_time['Min'])
df_time['Max'] = pd.to_numeric(df_time['Max'])

# Pivot the data so that each algorithm is a separate column
pivot_df_time = df_time.pivot(index='number_of_apps', columns='algo_name', values='Avg')
pivot_df_time.replace(0, np.nan, inplace=True)


#Read data
fname = "./evaluation_results/SM1_VerifiedPlacements.csv"
data = read_csv_to_list_with_header(fname)
df_verifications = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df_verifications['number_of_apps'] = pd.to_numeric(df_verifications['number_of_apps'])
df_verifications['Avg'] = pd.to_numeric(df_verifications['Avg'])
df_verifications['Min'] = pd.to_numeric(df_verifications['Min'])
df_verifications['Max'] = pd.to_numeric(df_verifications['Max'])

# Pivot the data so that each algorithm is a separate column
pivot_df_verifications = df_verifications.pivot(index='number_of_apps', columns='algo_name', values='Avg')
# pivot_df_verifications.replace(0, np.nan, inplace=True)


for function_set in function_sets_to_test.keys():

    algos_tested = function_sets_to_test[function_set]

    for i in range(len(algos_tested)):
        a1 = algos_tested[i]
        lw=5-3.5*i/len(algos_tested)
        ls=['-','--','-.',':'][i%4]
        m = ['s','D','o','X'][i%4]
        mw=10-4*i/len(algos_tested)
        axs_apps[fig_row][fig_col].plot(pivot_df_apps.index, pivot_df_apps[a1], marker=m, markersize=mw, label=a1, alpha=0.9, linestyle=ls, linewidth=lw)
        axs_replicas[fig_row][fig_col].plot(pivot_df_replicas.index, pivot_df_replicas[a1], marker=m, markersize=mw, label=a1, alpha=0.9, linestyle=ls, linewidth=lw)
        axs_time[fig_row][fig_col].plot(pivot_df_time.index, pivot_df_time[a1], marker=m, markersize=mw, label=a1, alpha=0.9, linestyle=ls, linewidth=lw)
        axs_violations[fig_row][fig_col].plot(pivot_df_verifications.index, pivot_df_verifications[a1], marker=m, markersize=mw, label=a1, alpha=0.9, linestyle=ls, linewidth=lw)

    axs_apps[fig_row][fig_col].set_title(function_set)
    axs_apps[fig_row][fig_col].grid(True)
    axs_apps[fig_row][fig_col].legend()
    axs_apps[fig_row][fig_col].set_xlabel('Number of Apps')
    axs_apps[fig_row][fig_col].set_ylabel('Average Value')
    axs_apps[fig_row][fig_col].label_outer()

    axs_replicas[fig_row][fig_col].set_title(function_set)
    axs_replicas[fig_row][fig_col].grid(True)
    axs_replicas[fig_row][fig_col].legend()
    axs_replicas[fig_row][fig_col].set_xlabel('Number of Apps')
    axs_replicas[fig_row][fig_col].set_ylabel('Average Value')
    axs_replicas[fig_row][fig_col].label_outer()

    axs_time[fig_row][fig_col].set_title(function_set)
    axs_time[fig_row][fig_col].grid(True)
    axs_time[fig_row][fig_col].legend()
    axs_time[fig_row][fig_col].set_xlabel('Number of Apps')
    axs_time[fig_row][fig_col].set_ylabel('Average Value')
    axs_time[fig_row][fig_col].label_outer()

    axs_violations[fig_row][fig_col].set_title(function_set)
    axs_violations[fig_row][fig_col].grid(True)
    axs_violations[fig_row][fig_col].legend()
    axs_violations[fig_row][fig_col].set_xlabel('Number of Apps')
    axs_violations[fig_row][fig_col].set_ylabel('Average Value')
    axs_violations[fig_row][fig_col].label_outer()

    fig_col += 1
    if fig_col >= 2:
        fig_row += 1
        fig_col = 0

plt.tight_layout()
plt.show()