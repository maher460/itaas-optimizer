from mip import Model, BINARY, INTEGER, CONTINUOUS, xsum, maximize
from baas_utilities import est_lat
import math
from itertools import product

def sm1_milp_max_sites(app_charcs, resources):
    
    apps = len(app_charcs)
    max_reps = 30
    sites = len(resources)
    servers = 30

    max_num_replicas = 112 * apps

    lats_apps = []

    lats_sites = []

    for app in app_charcs:
        temp_list = []
        for site in resources:
            temp_list.append(est_lat(app[4], site[2]))
        lats_apps.append(temp_list)

    for site1 in resources:
        temp_list = []
        for site2 in resources:
            temp_list.append(est_lat(site1[2], site2[2]))
        lats_sites.append(temp_list)

    num_confs = sites

    model = Model()

    #c = model.add_var(name="C", var_type=CONTINUOUS)
    r = model.add_var(name="R", var_type=CONTINUOUS)
    x = [[model.add_var(var_type=INTEGER, lb=0, name='x({},{})'.format(app+1, site+1)) for site in range(sites)] for app in range(apps)]
    a = [[model.add_var(var_type=BINARY, name='a({},{})'.format(app+1, conf+1)) for conf in range(num_confs)] for app in range(apps)]
    s = [[model.add_var(var_type=BINARY, name='s({},{})'.format(app+1, site+1)) for site in range(sites)] for app in range(apps)]
    z = [[[model.add_var(var_type=BINARY, name='z({},{},{})'.format(app+1, site1+1, site2+1)) for site2 in range(sites)] for site1 in range(sites)] for app in range(apps)]

    for i in range(len(app_charcs)):
        app = i
        f=app_charcs[i][0]
        d=app_charcs[i][1]
        k=app_charcs[i][2]
        min_sites = 2*d+1
        max_sites = min(3*f+2*(k+d)+1, len(resources))

        # sites_list = []
        # for cur_sites in range(min_sites, max_sites):
        #     sites_list.append(cur_sites)

        model += xsum(a[app][conf] for conf in range(num_confs)) <= 1

        for temp_conf in range(min_sites-1):
            #print(temp_conf)
            model += a[app][temp_conf] == 0
        for temp_conf in range(max_sites, sites):
            #print(temp_conf)
            model += a[app][temp_conf] == 0

        # for conf in range(num_confs):

        for cur_sites in range(min_sites, max_sites+1):

            conf = cur_sites -1

            model += xsum(s[app][site] for site in range(sites)) <= a[app][conf] * cur_sites + (1-a[app][conf]) * sites
            model += xsum(s[app][site] for site in range(sites)) >= a[app][conf] * cur_sites

            # cur_sites = sites_list[conf]

            u = math.ceil(float(3*f*d+d+cur_sites*k)/float(cur_sites-2*d))
            min_replicas = 3*f+2*u+1
            max_replicas_per_site = math.ceil(float(min_replicas)/float(cur_sites))
            min_replicas = max_replicas_per_site * cur_sites

            if cur_sites == min_sites:

                # matching s (site) with x (placement) (s is 1 when any x in that site is 1, s is 0 otherwise)
                for site in range(sites):
                    model += x[app][site] >= s[app][site]
                for site in range(sites):
                    model += x[app][site] <= s[app][site] * max_replicas_per_site

                # z is 1 if both s1 and s2 is 1, z is 0 otherwise
                for (site1, site2) in product(range(sites), range(sites)):
                    model += z[app][site1][site2] <= s[app][site1]
                    model += z[app][site1][site2] <= s[app][site2]
                    model += z[app][site1][site2] >= s[app][site1] + s[app][site2] - 1

                # lat constraint
                for (l_site, s1_site, s2_site, s3_site) in product(range(sites), range(sites), range(sites), range(sites)):
                    model += ((s[app][l_site] * lats_apps[app][l_site] * 2) \
                         + (z[app][l_site][s1_site] * lats_sites[l_site][s1_site]) \
                         + (z[app][s2_site][s3_site] * lats_sites[s2_site][s3_site] * 2) \
                         <= app_charcs[app][3])

            #Each app has at least the minimum number of replicas
            model += xsum(x[app][site] for site in range(sites)) >= min_replicas * a[app][conf] #(PHASE 2: CAN MULTIPLY THE CONFIGURATION VARIABLE HERE? c[app][config]?)
            model += xsum(x[app][site] for site in range(sites)) <= min_replicas * a[app][conf] + (1-a[app][conf]) * max_num_replicas

            # multi site (# PHASE 2 and also PHASE 1: We can replace this with by just requiring sum(s[app][site]) to be the required number of sites for this app and configuration)
            # for site in range(sites):
            #     model += x[app][site] <= max_replicas_per_site * a[app][conf] + servers * (1-a[app][conf]) #(PHASE 2: Maybe decrease this max_replicas_per_site to force more multiple sites for the different configs? Multiply this with c[app][config] so only one is true)

    # At most 4 replicas permachine
    # for site in range(sites):
    #     model += xsum(x[app][site] for app in range(apps)) <= servers * 4

    #model += c >= (xsum( (s[app][l_site] * lats_apps[app][l_site] * 2 + z[app][l_site][s1_site] * lats_sites[l_site][s1_site] + z[app][s2_site][s3_site] * lats_sites[s2_site][s3_site] * 2) / app_charcs[app][3] for (app, l_site, s1_site, s2_site, s3_site) in product(range(apps), range(sites), range(sites), range(sites), range(sites))) / (apps * sites * sites * sites * sites))
    model += r >= xsum(x[app][site] for (app,site) in product(range(apps),range(sites))) / float(max_num_replicas)

    model.objective = maximize(xsum(a[app][conf] for (app, conf) in product(range(apps), range(num_confs))) - r ) # - (r/float(apps*sites*servers)) )

    #model.threads = 1
    #model.max_seconds = 900
    model.optimize()

    placements = {}

    # Output of assignments
    for (app, site) in product(range(apps), range(sites)):

        for i in range(int(x[app][site].x)):
            if(app in placements.keys()):
                placements[app].append(resources[site][0])
            else:
                placements[app] = [resources[site][0]]

    t_placements = []

    for i in range(len(app_charcs)):
        if i in placements:
            t_placements.append(placements[i])
        else:
            t_placements.append([])

    placements = t_placements

    return placements