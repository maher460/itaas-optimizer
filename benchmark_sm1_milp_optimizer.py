from service_model_1_milp_optimizer import *
from baas_utilities import *
import time

#num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30, 50, 100]
num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30]
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

sm1_functions_to_test = [sm1_milp_max_sites]

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
    total += len(apps_collection[num_apps])

num_processed = 0

for num_apps in apps_collection.keys():
    for list_num in range(len(apps_collection[num_apps])):
        
        temp_res = []
        for func in sm1_functions_to_test:
            app_list = apps_collection[num_apps][list_num]

            start_time = time.time()

            res = func(app_list, aws_locations_short)

            end_time = time.time()

            execution_time = (end_time - start_time) * 1000

            quality = calc_quality_service_model_1(app_list, res, aws_locations_short)
            quality["algo_name"] = func.__name__
            quality["time"] = str(round(execution_time, 2))

            temp_res.append(quality)

        fname = "./data/benchmark_results/service_model_1_milp/res_app_list_"+str(num_apps)+"_"+str(list_num)+".csv"
        with open(fname, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["algo_name","execution-time-ms","verification","comment","num-apps-assigned","num-replicas-assigned","num-machines-used","min-lat","avg-lat","max-lat","min-lat-from-constraint","avg-lat-from-constraint","max-lat-from-constraint"])
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
                    #to_write += ["","","","","","","",""]
                    to_write += [str(x) for x in temp_res[i]["result"]]
                writer.writerow(to_write)

        num_processed += 1
        percent_done = round((num_processed / total) * 100, 2)
        run_name = "res_app_list_"+str(num_apps)+"_"+str(list_num)

        print("\n\n-----------------------------------------------------------------------------------------------------------\n")
        print("\t["+str(num_processed)+"/"+str(total)+" ("+str(percent_done)+"%)]:"+" Done working on " + run_name)
        print("\n-----------------------------------------------------------------------------------------------------------\n\n")

