from src.service_model_1_heuristic_optimizer import *
from src.baas_utilities import *
import time

apps_list = "./data/app_lists"
resources_list = "./data/resources_list_v2.csv"
results_dir = "./data/benchmark_results/service_model_1_heuristic"

num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30, 50, 100]
num_list_per_size = 10

sm1_functions_to_test = [sm1_round_robin_min_sites, 
                         sm1_closest_min_sites,
                         sm1_best_lat_min_sites,
                         sm1_round_robin_max_sites,
                         sm1_closest_max_sites,
                         sm1_best_lat_max_sites,
                         sm1_closest_max_sites_meet_lat,
                         sm1_best_lat_max_sites_meet_lat]

resources = format_resources(read_csv_to_list(resources_list))
apps_collection = read_app_lists(apps_list, num_apps_ops, num_list_per_size)

total = 0
for num_apps in apps_collection.keys():
    total += len(apps_collection[num_apps])

num_processed = 0

for num_apps in apps_collection.keys():
    for list_num in range(len(apps_collection[num_apps])):
        
        temp_res = []
        for func in sm1_functions_to_test:
            app_list = apps_collection[num_apps][list_num]

            start_time = time.time()

            placements = func(app_list, resources)

            end_time = time.time()

            execution_time = (end_time - start_time) * 1000

            quality = calc_quality_service_model_1(app_list, placements, resources)
            quality["algo_name"] = func.__name__
            quality["time"] = str(round(execution_time, 2))
            temp_res.append(quality)

        fname = results_dir + "/res_app_list_"+str(num_apps)+"_"+str(list_num)+".csv"
        with open(fname, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["algo_name","execution-time-ms","verification","comment","num-apps-assigned","num-replicas-assigned","min-lat","avg-lat","max-lat","min-lat-from-constraint","avg-lat-from-constraint","max-lat-from-constraint"])
            for i in range(len(temp_res)):
                to_write = []
                to_write.append(temp_res[i]["algo_name"])
                to_write.append(temp_res[i]["time"])

                if temp_res[i]["pass"] == True:
                    to_write.append(str(1))
                    to_write.append(temp_res[i]["comment"])
                    to_write += [str(x) for x in temp_res[i]["result"]]
                else:
                    to_write.append(str(0))
                    to_write.append(temp_res[i]["comment"])
                    to_write += [str(x) for x in temp_res[i]["result"]]
                writer.writerow(to_write)

        num_processed += 1
        percent_done = round((num_processed / total) * 100, 2)
        run_name = "res_app_list_"+str(num_apps)+"_"+str(list_num)
        print("["+str(num_processed)+"/"+str(total)+" ("+str(percent_done)+"%)]:"+" Done working on " + run_name)
