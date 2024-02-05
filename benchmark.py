from service_model_1_heuristic_optimizer import *
from baas_utilities import *
#import psutil
import time

num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30, 50, 100]
#num_apps_ops = [100]
num_list_per_size = 10

aws_locations =     [("CO1", "Columbus, Ohio", (39.983334, -82.983330), 30), 
                     ("CO2", "Columbus, Ohio", (39.983334, -82.983330), 30), 
                     ("CO3", "Columbus, Ohio", (39.983334, -82.983330), 30), 
                     ("EO1", "Eastern, Oregon", (45.849800, -119.691598), 30),
                     ("EO2", "Eastern, Oregon", (45.849800, -119.691598), 30), 
                     ("EO3", "Eastern, Oregon", (45.849800, -119.691598), 30), 
                     ("EO4", "Eastern, Oregon", (45.849800, -119.691598), 30),  
                     ("SFC1", "San Francisco, California", (37.756098, -122.448587), 30), 
                     ("SFC2", "San Francisco, California", (37.756098, -122.448587), 30), 
                     ("SFC3", "San Francisco, California", (37.756098, -122.448587), 30),
                     ("V1", "Multiple, Virginia", (38.949541, -77.401809), 30),
                     ("V2", "Multiple, Virginia", (38.949541, -77.401809), 30),
                     ("V3", "Multiple, Virginia", (38.949541, -77.401809), 30),
                     ("V4", "Multiple, Virginia", (38.949541, -77.401809), 30),
                     ("V5", "Multiple, Virginia", (38.949541, -77.401809), 30), 
                     ("V6", "Multiple, Virginia", (38.949541, -77.401809), 30)]

aws_locations_short=[("CO1", "Columbus, Ohio", (39.983334, -82.983330), 30), 
                     ("CO2", "Columbus, Ohio", (39.983334, -82.983330), 30), 
                     ("EO1", "Eastern, Oregon", (45.849800, -119.691598), 30),
                     ("EO2", "Eastern, Oregon", (45.849800, -119.691598), 30), 
                     ("SFC1", "San Francisco, California", (37.756098, -122.448587), 30), 
                     ("SFC2", "San Francisco, California", (37.756098, -122.448587), 30), 
                     ("V1", "Multiple, Virginia", (38.949541, -77.401809), 30),
                     ("V2", "Multiple, Virginia", (38.949541, -77.401809), 30),
                     ("V3", "Multiple, Virginia", (38.949541, -77.401809), 30)]

sm1_functions_to_test = [sm1_round_robin_min_sites, 
                         sm1_closest_min_sites,
                         sm1_best_lat_min_sites,
                         sm1_round_robin_max_sites,
                         sm1_closest_max_sites,
                         sm1_best_lat_max_sites,
                         sm1_closest_max_sites_meet_lat,
                         sm1_best_lat_max_sites_meet_lat]

# def get_cpu_memory_usage():
#     # Get the CPU usage
#     cpu_percent = psutil.cpu_percent()
    
#     # Get the memory usage
#     memory_info = psutil.virtual_memory()
#     memory_used = memory_info.used
#     memory_total = memory_info.total
    
#     return cpu_percent, memory_used, memory_total

def read_app_lists(aps_ops, amount_per_list):
    apps_dictionary = {}
    for num_apps in aps_ops:
        apps_dictionary[num_apps] = []
        for num_per_app in range(amount_per_list):
            fname = "./data/app_lists/app_list_"+str(num_apps)+"_"+str(num_per_app)+".csv"
            data = read_csv_to_list(fname)
            data = [[int(x[0]),int(x[1]),int(x[2]),int(x[3]),(float(x[4]),float(x[5])),int(x[6])] for x in data]
            apps_dictionary[num_apps].append(data)
    return apps_dictionary

apps_collection = read_app_lists(num_apps_ops, num_list_per_size)

total = 0
for num_apps in apps_collection.keys():
    total += len(apps_collection[num_apps]) - 5
# bench_results = {}

num_processed = 0

for num_apps in apps_collection.keys():
    #bench_results[num_apps] = []
    for list_num in range(5,len(apps_collection[num_apps])):
        
        temp_res = []
        for func in sm1_functions_to_test:
            # print(func.__name__)
            # print(num_apps)
            # print(list_num)
            app_list = apps_collection[num_apps][list_num]
            # print("A")
            # print(app_list)
            # print(aws_locations_short)
            #res = func(app_list, aws_locations_short)

            # cpu_usage_before, memory_used_before, memory_total_before = get_cpu_memory_usage()
            start_time = time.time()

            res = func(app_list, aws_locations_short)

            end_time = time.time()
            # cpu_usage_after, memory_used_after, memory_total_after = get_cpu_memory_usage()

            # cpu_usage_during = cpu_usage_after - cpu_usage_before
            # memory_used_during = memory_used_after - memory_used_before
            # memory_total_during = memory_total_after - memory_total_before
            execution_time = (end_time - start_time) * 1000


            # print("B")
            quality = calc_quality_service_model_1(app_list, res, aws_locations_short)
            quality["algo_name"] = func.__name__
            quality["time"] = str(round(execution_time, 2))
            # quality["cpu"] = str(round(cpu_usage_during, 2))
            # quality["ram"] = str(round(memory_used_during, 2))
            # quality["total_ram"] = str(round(memory_total_during, 2))
            temp_res.append(quality)
            # print("C")
            #bench_results[num_apps].append(quality)
            # print("D")
            # print(quality)
        fname = "./data/benchmark_results/service_model_1_heuristic/res_app_list_"+str(num_apps)+"_"+str(list_num)+".csv"
        with open(fname, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["algo_name","execution-time-ms","verification","comment","num-apps-assigned","num-replicas-assigned","min-lat","avg-lat","max-lat","min-lat-from-constraint","avg-lat-from-constraint","max-lat-from-constraint"])
            for i in range(len(temp_res)):
                to_write = []
                to_write.append(temp_res[i]["algo_name"])
                to_write.append(temp_res[i]["time"])
                # to_write.append(temp_res[i]["cpu"])
                # to_write.append(temp_res[i]["ram"])
                # to_write.append(temp_res[i]["total_ram"])
                if temp_res[i]["pass"] == True:
                    to_write.append(str(1))
                    to_write.append(temp_res[i]["comment"])
                    to_write += [str(x) for x in temp_res[i]["result"]]
                else:
                    to_write.append(str(0))
                    to_write.append(temp_res[i]["comment"])
                    #to_write += ["","","","","","","",""]
                    to_write += [str(x) for x in temp_res[i]["result"]]
                writer.writerow(to_write)

        num_processed += 1
        percent_done = round((num_processed / total) * 100, 2)
        run_name = "res_app_list_"+str(num_apps)+"_"+str(list_num)
        print("["+str(num_processed)+"/"+str(total)+" ("+str(percent_done)+"%)]:"+" Done working on " + run_name)


# print(bench_results)
