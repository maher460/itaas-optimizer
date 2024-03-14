import csv
import random
from baas_utilities import read_csv_to_list

random.seed(42)

f_ops = [1, 1, 1, 2, 2, 3]
d_ops = [1, 1, 1, 2, 2, 3]
k_ops = [1, 1, 1, 2, 2, 3]
r_ops = [1, 1, 1, 1, 1, 3, 3, 3, 3, 6, 6, 6, 12, 24, 48]
lat_ops = [100, 200, 500, 1000]
loc_ops = [(x[0],x[1]) for x in read_csv_to_list("./../data/geo_coordinates_usa.csv")]

num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30, 50, 100]
num_list_per_size = 10

for num_app in num_apps_ops:
    for num_per_app in range(num_list_per_size):
        fname = "./../data/app_lists/app_list_"+str(num_app)+"_"+str(num_per_app)+".csv"
        with open(fname, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(["f","d","k","latency","latitude","longitude","pr_interval"])
            for i in range(num_app):
                f = random.choice(f_ops)
                d = random.choice(d_ops)
                k = random.choice(k_ops)
                r = random.choice(r_ops)
                lat = random.choice(lat_ops)
                loc = random.choice(loc_ops)
                writer.writerow([str(f), str(d), str(k), str(lat), str(loc[0]), str(loc[1]), str(r)])
