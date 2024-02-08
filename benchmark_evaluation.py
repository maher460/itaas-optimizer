from baas_utilities import read_csv_to_list
import pprint

pp = pprint.PrettyPrinter(indent=0.5)

#evaluation_names = ["service_model_1_heuristic", "service_model_1_milp"]
evaluation_names = ["service_model_1_heuristic", "service_model_1_milp"]

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

# pp.pprint(algos_tested)
# pp.pprint(benchmark_results)

verified_algos = [x for x in algos_tested]

print(verified_algos)

data_temp = {}
data_time = {}
for alg in algos_tested:
    data_temp[alg] = []

for num_apps in num_apps_ops:
    for num_per_app in range(num_list_per_size):
        for a1 in algos_tested:
            if benchmark_results[num_apps][num_per_app][a1]["verification"]==1:
                if benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"]==benchmark_results[num_apps][num_per_app]["sm1_milp_max_sites"]["num-apps-assigned"]:
                    data_temp[a1].append((benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"])/float(benchmark_results[num_apps][num_per_app]["sm1_milp_max_sites"]["num-replicas-assigned"]))
                if benchmark_results[num_apps][num_per_app][a1]["verification"] != 1 and a1 in verified_algos:
                    verified_algos.remove(a1)
pp.pprint(data_temp)
compare_algos = {}
for a1 in verified_algos:
    if a1 not in compare_algos.keys():
        compare_algos[a1] = {}
    for a2 in verified_algos:
        if a2 not in compare_algos[a1].keys():
            compare_algos[a1][a2] = {"reps_total": 0, "reps_count": 0, "reps_avg": 0.0, "apps_total": 0, "apps_count": 0, "apps_avg": 0.0}

for num_apps in num_apps_ops:
    for num_per_app in range(num_list_per_size):
        for a1 in verified_algos:
            for a2 in verified_algos:
                #if benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"] < benchmark_results[num_apps][num_per_app][a2]["num-replicas-assigned"]:
                compare_algos[a1][a2]["reps_count"] += 1
                compare_algos[a1][a2]["reps_total"] += benchmark_results[num_apps][num_per_app][a2]["num-replicas-assigned"] - benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"]
                compare_algos[a1][a2]["reps_avg"] = round(float(compare_algos[a1][a2]["reps_total"]) / compare_algos[a1][a2]["reps_count"], 2)
                #if benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"] > benchmark_results[num_apps][num_per_app][a2]["num-apps-assigned"]:
                compare_algos[a1][a2]["apps_count"] += 1
                compare_algos[a1][a2]["apps_total"] += benchmark_results[num_apps][num_per_app][a1]["num-apps-assigned"] - benchmark_results[num_apps][num_per_app][a2]["num-apps-assigned"]
                compare_algos[a1][a2]["apps_avg"] = round(float(compare_algos[a1][a2]["apps_total"]) / compare_algos[a1][a2]["apps_count"], 2)

                #compare_algos[a1][a2] += benchmark_results[num_apps][num_per_app][a1]["num-replicas-assigned"] - benchmark_results[num_apps][num_per_app][a2]["num-replicas-assigned"]

# pp.pprint(compare_algos)
# pp.pprint(verified_algos)


import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)

mu = 200
sigma = 25
n_bins = 25
data = np.random.normal(mu, sigma, size=100)

fig = plt.figure(figsize=(9, 4), layout="constrained")
axs = fig.subplots(1, 1, sharex=True, sharey=True)

# Cumulative distributions.
for a1 in algos_tested:
    axs.ecdf(data_temp[a1], label=a1)
# n, bins, patches = axs[0].hist(data, n_bins, density=True, histtype="step",
#                                cumulative=True, label="Cumulative histogram")
# x = np.linspace(data.min(), data.max())
# y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
#      np.exp(-0.5 * (1 / sigma * (x - mu))**2))
# y = y.cumsum()
# y /= y[-1]
# axs[0].plot(x, y, "k--", linewidth=1.5, label="Theory")

# # Complementary cumulative distributions.
# axs[1].ecdf(data, complementary=True, label="CCDF")
# axs[1].hist(data, bins=bins, density=True, histtype="step", cumulative=-1,
#             label="Reversed cumulative histogram")
# axs[1].plot(x, 1 - y, "k--", linewidth=1.5, label="Theory")

# Label the figure.
fig.suptitle("Cumulative distributions")
#for ax in axs:
axs.grid(True)
axs.legend()
# ax.set_xlabel("Annual rainfall (mm)")
# ax.set_ylabel("Probability of occurrence")
axs.label_outer()

plt.show()