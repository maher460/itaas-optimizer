from baas_utilities import read_csv_to_list_with_header
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Set text size for all labels
plt.rcParams.update({'font.size': 14})


# Define functions sets
sm2_functions_to_test_all = ["sm2_round_robin_min_sites", 
                         "sm2_closest_min_sites",
                         "sm2_best_lat_min_sites",
                         "sm2_round_robin_max_sites",
                         "sm2_closest_max_sites",
                         "sm2_best_lat_max_sites",
                         "sm2_closest_max_sites_meet_lat",
                         "sm2_best_lat_max_sites_meet_lat",
                         "sm2_milp_max_sites"]

sm2_functions_to_test_min_sites = ["sm2_round_robin_min_sites", 
                         "sm2_closest_min_sites",
                         "sm2_best_lat_min_sites",
                         "sm2_milp_max_sites"]

sm2_functions_to_test_max_sites = ["sm2_round_robin_max_sites",
                         "sm2_closest_max_sites",
                         "sm2_best_lat_max_sites",
                         "sm2_milp_max_sites"]

sm2_functions_to_test_max_sites_meet_lat = ["sm2_closest_max_sites_meet_lat",
                         "sm2_best_lat_max_sites_meet_lat",
                         "sm2_milp_max_sites"]

optimal_algo = "sm2_milp_max_sites"

function_sets_to_test = {"all": sm2_functions_to_test_all, 
                         "min_sites": sm2_functions_to_test_min_sites, 
                         "max_sites": sm2_functions_to_test_max_sites, 
                         "max_sites_meet_lat": sm2_functions_to_test_max_sites_meet_lat}

def run():

    #Create the plots
    fig_apps = plt.figure(figsize=(18, 8), layout="constrained")
    fig_apps.suptitle("Service Model 2: Average Number of Apps (higher is better)")
    axs_apps = fig_apps.subplots(2, 2, sharex=True, sharey=True)

    fig_replicas = plt.figure(figsize=(18, 8), layout="constrained")
    fig_replicas.suptitle("Service Model 2: Average Number of Replicas (lower is better)")
    axs_replicas = fig_replicas.subplots(2, 2, sharex=True, sharey=True)

    fig_time = plt.figure(figsize=(18, 8), layout="constrained")
    fig_time.suptitle("Service Model 2: Average Execution Time (lower is better)")
    axs_time = fig_time.subplots(2, 2, sharex=True, sharey=True)

    fig_violations = plt.figure(figsize=(18, 8), layout="constrained")
    fig_violations.suptitle("Service Model 2: Average Verification Score (higher is better)")
    axs_violations = fig_violations.subplots(2, 2, sharex=True, sharey=True)

    fig_row = 0
    fig_col = 0


    #Read data
    fname = "./evaluation_results/SM2_Apps.csv"
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
    fname = "./evaluation_results/SM2_Replicas.csv"
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
    fname = "./evaluation_results/SM2_ExecutionTimes.csv"
    data = read_csv_to_list_with_header(fname)
    df_time = pd.DataFrame(data[1:], columns=data[0])

    # Convert columns to appropriate data types
    df_time['number_of_apps'] = pd.to_numeric(df_time['number_of_apps'])
    df_time['Avg'] = pd.to_numeric(df_time['Avg'])
    df_time['Min'] = pd.to_numeric(df_time['Min'])
    df_time['Max'] = pd.to_numeric(df_time['Max'])

    # Pivot the data so that each algorithm is a separate column
    pivot_df_time = df_time.pivot(index='number_of_apps', columns='algo_name', values='Avg')


    #Read data
    fname = "./evaluation_results/SM2_VerifiedPlacements.csv"
    data = read_csv_to_list_with_header(fname)
    df_verifications = pd.DataFrame(data[1:], columns=data[0])

    # Convert columns to appropriate data types
    df_verifications['number_of_apps'] = pd.to_numeric(df_verifications['number_of_apps'])
    df_verifications['Avg'] = pd.to_numeric(df_verifications['Avg'])
    df_verifications['Min'] = pd.to_numeric(df_verifications['Min'])
    df_verifications['Max'] = pd.to_numeric(df_verifications['Max'])

    # Pivot the data so that each algorithm is a separate column
    pivot_df_verifications = df_verifications.pivot(index='number_of_apps', columns='algo_name', values='Avg')


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
    #plt.show()


    plt.savefig('evaluation_results/SM2_VerifiedPlacements_Avg_Line.png', bbox_inches='tight')
    plt.close()

    plt.savefig('evaluation_results/SM2_ExecutionTimes_Avg_Line.png', bbox_inches='tight')
    plt.close()

    plt.savefig('evaluation_results/SM2_Replicas_Avg_Line.png', bbox_inches='tight')
    plt.close()

    plt.savefig('evaluation_results/SM2_Apps_Avg_Line.png', bbox_inches='tight')
    plt.close()


    # # Plotting
    # plt.figure(figsize=(10, 6))

    # for column in pivot_df.columns:
    #     plt.plot(pivot_df.index, pivot_df[column], marker='o', label=column)

    # plt.title('Average Values by Algorithm and Number of Apps')
    # plt.xlabel('Number of Apps')
    # plt.ylabel('Average Value')
    # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()
