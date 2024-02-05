from collections import Counter
from collections import defaultdict
import geopy.distance
import itertools
import csv
import math

############################################################
# DEBUG MODE
# DEBUG = 0: No Debug
# DEBUG = 1: Show latencies
DEBUG = 0
############################################################


NUM_REPS_PER_MACHINE = 4
SPEED = 2.14 * (10 ** 5) # km/s


def read_csv_to_list(csv_file):
    data = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            data.append(row)
    return data


def dist_coords(coords_1, coords_2):
    if DEBUG == 1:
        print("######################################")
        print(coords_1)
        print(coords_2)
        coords_1 = (str(coords_1[0]), str(coords_1[1]))
        coords_2 = (str(coords_2[0]), str(coords_2[1]))
        print(coords_1)
        print(coords_2)
        print("######################################")
    return geopy.distance.geodesic(coords_1, coords_2).km


def est_lat(coords_1, coords_2):
    dist = dist_coords(coords_1, coords_2)
    dist = dist * 1.1 # 10% slack
    lat = (dist / SPEED) * 1000 # ms
    lat = lat + 1 # adjusted for routing delay
    return lat

def calc_lat(app_loc, leader_loc, sites_loc):

    if DEBUG == 1:
        print("##############################")

    lat = 0
    lat += (2 * est_lat(app_loc, leader_loc)) # request and reply

    if DEBUG == 1:
        print("[LAT] App to Leader: ", est_lat(app_loc, leader_loc))
    
    sites_lat = []
    for s in sites_loc:
        sites_lat.append(est_lat(leader_loc, s)) 

    lat += max(sites_lat) # pre-prepare

    if DEBUG == 1:
        print("[LAT] Max Leader to Replica: ", max(sites_lat))

    sites_lat = []

    for s1 in sites_loc:
        for s2 in sites_loc:
            sites_lat.append(est_lat(s1, s2)) 

    lat += (2 * max(sites_lat)) # prepare and commit

    if DEBUG == 1:
        print("[LAT] Max Replica to Replica: ", max(sites_lat))

    if DEBUG == 1:
        print("[LAT] Total: ", lat)

    if DEBUG == 1:
        print("##############################")

    return lat

def verify_placement_sm1(app_charcs, placements, resources):
    
    # Check if um Apps is same as num placements
    # if len(app_charcs) != len(placements):
    #     print("[Verification Failed]: Num Apps is not same as num placements")
    #     return {"pass": False, "comment":"Num Apps is not same as num placements"}

    # check every site exists
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter(placements[i])
            sites = list(c.elements())
            for s in sites:
                found = False
                for z in resources:
                    if z[0] == s:
                        found = True
                if not found:
                    # print("[Verification Failed]: Site name does not exist!")
                    return {"pass": False, "comment":"Site name does not exist!"}
    
    # Check if minimum number of sites is satisfied
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter(placements[i])
            num_sites = len(list(c.elements()))
            min_sites = 2*app_charcs[i][1] + 1
            if num_sites < min_sites:
                # print("[Verification Failed]: Number of sites is less than minimum!")
                return {"pass": False, "comment":"Number of sites is less than minimum"}

    # Check if total number of replicas is less than minimum
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter(placements[i])
            num_sites = len(list(c.elements()))
            num_replicas = sum(c.values()) #c.total()
            # max_replicas_per_site = c.most_common(1)[0][1]
            # min_replicas = 3*app_charcs[i][0] + 2*(app_charcs[i][1]*max_replicas_per_site + 1) + 1
            # min_replicas = 3*app_charcs[i][0] + 2*(app_charcs[i][1]*max_replicas_per_site + app_charcs[i][2]) + 1
            u = math.ceil(float(3*app_charcs[i][0]*app_charcs[i][1]+app_charcs[i][1]+num_sites*app_charcs[i][2])/float(num_sites-2*app_charcs[i][1]))
            min_replicas = 3*app_charcs[i][0]+2*u+1
            if num_replicas < min_replicas:
                # print("[Verification Failed]: Total number of replicas is less than minimum!")
                return {"pass": False, "comment":"Total number of replicas is less than minimum"}

    # check latency (based on PBFT)
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter(placements[i])
            sites = list(c.elements())
            sites_loc = []
            for s in sites:
                for z in resources:
                    if z[0] == s:
                        sites_loc.append(z[2])
            exp_lats = []
            for j in range(len(sites)):
                if DEBUG == 1:
                    print("###################")
                    print(sites)
                    print(app_charcs)
                    print(sites_loc)
                    print("###################")
                exp_lats.append(calc_lat(app_charcs[i][4], sites_loc[j], sites_loc))
            max_exp_lat = max(exp_lats)
            if DEBUG == 1:
                print("[LAT] Max Expected Latency: ", max_exp_lat)
                print("[LAT] Application Max Limit: ", app_charcs[i][3])
            if max_exp_lat > app_charcs[i][3]:
                # print("[Verification Failed]: Max expected latency is too high!")
                return {"pass": False, "comment":"Max expected latency is too high"}

    return {"pass": True, "comment": ""}

def calc_quality_service_model_1(app_charcs, placements, resources):
    
    result = verify_placement_sm1(app_charcs, placements, resources)
    # if result["pass"] == False:
    #     result["result"] = []
    #     return result

    num_apps = 0
    num_replicas = 0
    total_lat = 0
    total_lat_from_constraint = 0
    all_lat_from_constraint = []
    all_lat = []

    for p in placements:
        if p != []:
            num_apps += 1
            num_replicas += len(p)

    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter(placements[i])
            sites = list(c.elements())
            sites_loc = []
            for s in sites:
                for z in resources:
                    if z[0] == s:
                        sites_loc.append(z[2])
            exp_lats = []
            for j in range(len(sites)):
                if DEBUG == 1:
                    print("###################")
                    print(sites)
                    print(app_charcs)
                    print(sites_loc)
                    print("###################")
                exp_lats.append(calc_lat(app_charcs[i][4], sites_loc[j], sites_loc))
            max_exp_lat = max(exp_lats)
            total_lat += max_exp_lat
            total_lat_from_constraint += app_charcs[i][3] - max_exp_lat
            all_lat_from_constraint.append(app_charcs[i][3] - max_exp_lat)
            all_lat.append(max_exp_lat)

    min_lat_from_constraint = min(all_lat_from_constraint)
    avg_lat_from_constraint = sum(all_lat_from_constraint) / float(len(all_lat_from_constraint))
    max_lat_from_constraint = max(all_lat_from_constraint)

    min_lat = min(all_lat)
    avg_lat = sum(all_lat) / float(len(all_lat))
    max_lat = max(all_lat)

    result["result"] = [num_apps, num_replicas, round(min_lat, 2), round(avg_lat, 2), round(max_lat, 2), round(min_lat_from_constraint, 2), round(avg_lat_from_constraint, 2), round(max_lat_from_constraint, 2)]

    return result



def verify_placement_sm2(app_charcs, placements, resources, pr):

    # check every site exists
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter([x[0] for x in placements[i]])
            sites = list(c.elements())
            for s in sites:
                found = False
                for z in resources:
                    if z[0] == s:
                        found = True
                if not found:
                    #print("[Verification Failed]: Site name does not exist!")
                    return {"pass": False, "comment":"Site name does not exist!"}

    # Check if minimum number of sites is satisfied
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter([x[0] for x in placements[i]])
            num_sites = len(list(c.elements()))
            min_sites = 2*app_charcs[i][1] + 1
            if num_sites < min_sites:
                #print("[Verification Failed]: Number of sites is less than minimum!")
                return {"pass": False, "comment":"Number of sites is less than minimum"}

    # Check if total number of replicas is less than minimum
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter([x[0] for x in placements[i]])
            num_replicas = sum(c.values()) #c.total()
            max_replicas_per_site = c.most_common(1)[0][1]
            min_replicas = 3*app_charcs[i][0] + 2*(app_charcs[i][1]*max_replicas_per_site + app_charcs[i][2]) + 1
            if num_replicas < min_replicas:
                #print("[Verification Failed]: Total number of replicas is less than minimum!")
                return {"pass": False, "comment":"Total number of replicas is less than minimum"}

    # check latency requirement (based on PBFT)
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter([x[0] for x in placements[i]])
            sites = list(c.elements())
            sites_loc = []
            for s in sites:
                for z in resources:
                    if z[0] == s:
                        sites_loc.append(z[2])
            exp_lats = []
            for j in range(len(sites)):
                exp_lats.append(calc_lat(app_charcs[i][4], sites_loc[j], sites_loc))
            max_exp_lat = max(exp_lats)
            if DEBUG == 1:
                print("[LAT] Max Expected Latency: ", max_exp_lat)
                print("[LAT] Application Max Limit: ", app_charcs[i][3])
            if max_exp_lat > app_charcs[i][3]:
                #print("[Verification Failed]: Max expected latency is too high!")
                return {"pass": False, "comment":"Max expected latency is too high"}

    # Check each specific machine exists, and no machine is overloaded
    machines = defaultdict(int)
    for i in range(len(placements)):
        if placements[i] != []:
            for x in placements[i]:
                found = False
                for a in resources:
                    if a[0] == x[0]:
                        found = True
                        if a[3] < x[1]:
                            #print("[Verification Failed]: Specific machine does not exist!")
                            return {"pass": False, "comment":"Specific machine does not exist"}
                if not found:
                    #print("[Verification Failed]: Site name does not exist!")
                    return {"pass": False, "comment":"Site name does not exist!"}
                comb_name = x[0] + str(x[1])
                machines[comb_name] += 1
    if max(machines.values()) > NUM_REPS_PER_MACHINE:
        #print("[Verification Failed]: Too many replicas in one machine!")
        return {"pass": False, "comment":"Too many replicas in one machine"}

    for i in range(len(placements)):
        if placements[i] != []:
            if(len(placements[i]) != len(list(set(placements[i])))):
                #print("[Verification Failed]: More than one replica of the same application in the same machine!")
                return {"pass": False, "comment":"More than one replica of the same application in the same machine"}

    # Check if proactive recovery group contains only apps with same charcs and no pr group is overloaded
    if pr == True:
        inv_pr_groups = {}
        app_pr_keys = {}

        for i in range(len(placements)):
            app = app_charcs[i]
            f=app[0]
            d=app[1]
            k=app[2]
            pr=app[5]

            pr_key = (f,d,k,pr)
            app_pr_keys[i] = pr_key

            if placements[i] != []:
                for x in placements[i]:
                    if x[0] in inv_pr_groups:
                        if x[1] in inv_pr_groups[x[0]]:
                            if (len(inv_pr_groups[x[0]][x[1]]) >= NUM_REPS_PER_MACHINE):
                                #print("[Verification Failed]: Proactive Recovery group contains more replicas than max allowed!")
                                return {"pass": False, "comment":"Proactive Recovery group contains more replicas than max allowed"}
                            for app2 in inv_pr_groups[x[0]][x[1]]:
                                if app_pr_keys[app2] != app_pr_keys[i]:
                                    #print("[Verification Failed]: Proactive Recovery group contains apps with different characteristics!")
                                    return {"pass": False, "comment":"Proactive Recovery group contains apps with different characteristics"}
                            inv_pr_groups[x[0]][x[1]].append(i)
                        else:
                            inv_pr_groups[x[0]][x[1]] = [i]
                    else:
                        inv_pr_groups[x[0]] = {x[1]: [i]}

    return {"pass": True, "comment": ""}


def calc_quality_service_model_2(app_charcs, placements, resources, pr):

    result = verify_placement_sm2(app_charcs, placements, resources, pr)

    num_apps = 0
    num_replicas = 0
    total_lat = 0
    total_lat_from_constraint = 0
    all_lat_from_constraint = []
    all_lat = []
    sites_machines = {}
    num_machines = 0

    for p in placements:
        if p != []:
            num_apps += 1
            num_replicas += len(p)
            for x in p:
                if x in sites_machines.keys():
                    sites_machines[x] += 1
                else:
                    sites_machines[x] = 1
    num_machines = len(sites_machines.keys())

     # check latency (based on PBFT)
    for i in range(len(placements)):
        if placements[i] != []:
            c = Counter([x[0] for x in placements[i]])
            sites = list(c.elements())
            sites_loc = []
            for s in sites:
                for z in resources:
                    if z[0] == s:
                        sites_loc.append(z[2])
            exp_lats = []
            for j in range(len(sites)):
                exp_lats.append(calc_lat(app_charcs[i][4], sites_loc[j], sites_loc))
            max_exp_lat = max(exp_lats)
            total_lat += max_exp_lat
            total_lat_from_constraint += app_charcs[i][3] - max_exp_lat
            all_lat_from_constraint.append(app_charcs[i][3] - max_exp_lat)
            all_lat.append(max_exp_lat)

    min_lat_from_constraint = min(all_lat_from_constraint)
    avg_lat_from_constraint = sum(all_lat_from_constraint) / float(len(all_lat_from_constraint))
    max_lat_from_constraint = max(all_lat_from_constraint)

    min_lat = min(all_lat)
    avg_lat = sum(all_lat) / float(len(all_lat))
    max_lat = max(all_lat)

    result["result"] = (num_apps, num_replicas, num_machines, round(min_lat, 2), round(avg_lat, 2), round(max_lat, 2), round(min_lat_from_constraint, 2), round(avg_lat_from_constraint, 2), round(max_lat_from_constraint, 2))

    return result


def print_quality(res):
    if(len(res) == 9):
        print("Total number of apps assigned [higher is better]:", res[0])
        print("Total number of replicas assigned [lower is better]:", res[1])
        print("Total number of machines used [lower is better]:", res[2])
        print("Min/Avg/Max Latency (in seconds) [lower is better]:", str(res[4]) + " / " + str(res[5]) + " / " + str(res[6]))
        print("Min/Avg/Max Latency from Constraint (in seconds) [higher is better]:", str(res[7]) + " / " + str(res[8]) + " / " + str(res[9]))
    if(len(res) == 8):
        print("Total number of apps assigned [higher is better]:", res[0])
        print("Total number of replicas assigned [lower is better]:", res[1])
        print("Min/Avg/Max Latency (in seconds) [lower is better]:", str(res[4]) + " / " + str(res[5]) + " / " + str(res[6]))
        print("Min/Avg/Max Latency from Constraint (in seconds) [higher is better]:", str(res[7]) + " / " + str(res[8]) + " / " + str(res[9]))


def visualize(placements):
    print("-------------------------------------------------------------")
    print("Application Assignments to Machines (SiteName: MachineNumber):")
    print()
    apps = []
    for p in placements:
        temp = {}
        for x in p:
            if x[0] in temp:
                temp[x[0]] += 1
            else:
                temp[x[0]] = 1
        apps.append(temp)
    if(len(apps) == 0 or len(placements) == 0):
        print("No application assignment found...")
    for i in range(len(apps)):
        print("App ", i+1, ":")
        print(apps[i])
        print()
    print("-------------------------------------------------------------")

def fastest_sites(num_sites, app_loc, resources):
    
    fast_sites = []
    best_lat = -1

    for temp_sites in itertools.combinations(resources, num_sites):
        sites_loc = [x[2] for x in temp_sites]
        exp_lats = []

        for j in range(len(temp_sites)):
            exp_lats.append(calc_lat(app_loc, sites_loc[j], sites_loc))

        max_exp_lat = max(exp_lats)

        if (max_exp_lat < best_lat) or (best_lat == -1):
            best_lat = max_exp_lat
            fast_sites = temp_sites[:]

    return fast_sites

def faster_sites(num_sites, app_loc, resources):
    
    fast_sites = sorted(resources, key=lambda r: est_lat(app_loc,r[2]))
    fast_sites = fast_sites[:num_sites]
    return fast_sites