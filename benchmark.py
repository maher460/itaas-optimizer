from service_model_1_heuristic_optimizer import *
from baas_utilities import *

num_apps_ops = [3, 5, 7, 9, 11, 13, 15, 20, 30, 50, 100]
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


sm1_functions_to_test = [sm1_round_robin_min_sites, 
                         sm1_closest_min_sites,
                         sm1_best_lat_min_sites,
                         sm1_round_robin_max_sites,
                         sm1_closest_max_sites,
                         sm1_best_lat_max_sites,
                         sm1_closest_max_sites_meet_lat,
                         sm1_best_lat_max_sites_meet_lat]