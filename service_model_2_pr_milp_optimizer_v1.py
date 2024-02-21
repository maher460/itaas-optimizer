# Best results so far...
# Try running with more seconds till halt, maybe 30 min and more threads, maybe 12...

from mip import Model, BINARY, INTEGER, CONTINUOUS, xsum, maximize
from baas_utilities import est_lat
import math
from itertools import product


def sm2_pr_milp_max_sites(app_charcs, resources):
    
    apps = len(app_charcs)
    max_reps = 30
    sites = len(resources)
    servers = 30

    max_total_replicas = 112 * apps

    num_confs = sites

    lats_apps = []

    lats_sites = []

    pr_keys_sets = {}

    for i in range(len(app_charcs)):
        app = i
        f=app_charcs[i][0]
        d=app_charcs[i][1]
        k=app_charcs[i][2]
        pr=app_charcs[i][5]

        for conf in range(num_confs):

            pr_key = (f,d,k,pr,conf)
            pr_keys_sets[(app,conf)] = pr_key


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


    model = Model()


    #c = model.add_var(name="C", var_type=CONTINUOUS)
    r = model.add_var(name="R", lb=0, ub=1, var_type=CONTINUOUS)

    a = [[[model.add_var(var_type=BINARY, name='a({},{},{})'.format(app+1, conf+1, rg+1)) for rg in range(apps)] for conf in range(num_confs)] for app in range(apps)]
    x = [[model.add_var(var_type=INTEGER, lb=0, ub=servers, name='x({},{})'.format(rg+1, site+1)) for site in range(sites)] for rg in range(apps)]

    v = [[model.add_var(var_type=BINARY, name='v({},{})'.format(app+1, rg+1)) for rg in range(apps)] for app in range(apps)]

    # s[App][Site] = 0/1
    s = [[model.add_var(var_type=BINARY, name='s({},{})'.format(rg+1, site+1)) for site in range(sites)] for rg in range(apps)]

    # z[App][Site1][Site2] = 0/1
    z = [[[model.add_var(var_type=BINARY, name='z({},{},{})'.format(rg+1, site1+1, site2+1)) for site1 in range(sites)] for site2 in range(sites)] for rg in range(apps)]

    # P3_T2: latency
    l = [model.add_var(var_type=CONTINUOUS, lb=0, ub=1000, name="l({})".format(rg+1)) for rg in range(apps)]


    ### P3_T1: If pr_keys of two apps don't match, then they cannot be in the same group 
    for (i,j, conf_i, conf_j) in product(range(apps), range(apps), range(num_confs), range(num_confs)):
        if pr_keys_sets[(i,conf_i)] != pr_keys_sets[(j,conf_j)]:
            for rg in range(apps):
                model += a[i][conf_i][rg] + a[j][conf_j][rg] <= 1

    for rg in range(apps):
        # lat constraint
        for (l_site, s1_site, s2_site, s3_site) in product(range(sites), range(sites), range(sites), range(sites)):
            model += (z[rg][l_site][s1_site] * lats_sites[l_site][s1_site]) \
                 + (z[rg][s2_site][s3_site] * lats_sites[s2_site][s3_site] * 2) \
                 <= l[rg]

    for i in range(len(app_charcs)):
        app = i
        f=app_charcs[i][0]
        d=app_charcs[i][1]
        k=app_charcs[i][2]
        pr=app_charcs[i][5]
        min_sites = 2*d+1
        max_sites = min(3*f+2*(k+d)+1, len(resources))

        pr_key = (f,d,k,pr)

        # P3_T1: ONLY one a[app][config][rg] is 1 for the same app, others must be zero
        model += xsum(a[app][conf][rg] for (conf, rg) in product(range(num_confs),range(apps))) <= 1

        for rg in range(apps):

            model += xsum(a[app][conf][rg] for conf in range(num_confs)) >= v[app][rg]
            model += xsum(a[app][conf][rg] for conf in range(num_confs)) <= v[app][rg]

            for l_site in range(sites):
                model += l[rg] + (s[rg][l_site] * lats_apps[app][l_site] * 2)  <= app_charcs[app][3] * v[app][rg] + 1000 * (1 - v[app][rg])

        # P3_T1: set confs that are not possible to 0 
        for temp_conf in range(min_sites-1):
            for rg in range(apps):
                model += a[app][temp_conf][rg] == 0
        for temp_conf in range(max_sites, sites):
            for rg in range(apps):
                model += a[app][temp_conf][rg] == 0

        for cur_sites in range(min_sites,max_sites+1):

            t_conf = cur_sites-1

            u = math.ceil(float(3*f*d+d+cur_sites*k)/float(cur_sites-2*d))
            min_replicas = 3*f+2*u+1
            max_replicas_per_site = math.ceil(float(min_replicas)/float(cur_sites))
            min_replicas = max_replicas_per_site * cur_sites

            for rg in range(apps):

                model += xsum(s[rg][site] for site in range(sites)) <= a[app][t_conf][rg] * cur_sites + (1-a[app][t_conf][rg]) * sites
                model += xsum(s[rg][site] for site in range(sites)) >= a[app][t_conf][rg] * cur_sites

                # P3_T1: PR group must have the minimum number of replicas
                model += xsum(x[rg][site] for site in range(sites)) >= min_replicas * a[app][t_conf][rg]
                model += xsum(x[rg][site] for site in range(sites)) <= min_replicas * a[app][t_conf][rg] + (1-a[app][t_conf][rg]) * (max_total_replicas) # TODO: Try with this constraint removed
   
                # multi site
                for site in range(sites):
                    model += x[rg][site] <= max_replicas_per_site * a[app][t_conf][rg] + servers * (1-a[app][t_conf][rg]) #(PHASE 2: Maybe decrease this max_replicas_per_site to force more multiple sites for the different configs? Multiply this with c[app][config] so only one is true)

            

    # P3_T1: At most 4 apps per PR group
    for rg in range(apps):
        model += xsum(a[app][conf][rg] for (conf, app) in product(range(num_confs),range(apps))) <= 4

    for site in range(sites):
        model += xsum(x[rg][site] for rg in range(apps)) <= servers

    # P3_T1: matching s (site) with x (rg placement) (s is 1 when any x in that site is 1, s is 0 otherwise)
    for rg in range(apps):

        for site in range(sites):
            model += x[rg][site] >= s[rg][site]
        for site in range(sites):
            model += x[rg][site] <= s[rg][site] * servers

        # z is 1 if both s1 and s2 is 1, z is 0 otherwise
        for (site1, site2) in product(range(sites), range(sites)):
            model += z[rg][site1][site2] <= s[rg][site1]
            model += z[rg][site1][site2] <= s[rg][site2]
            model += z[rg][site1][site2] >= s[rg][site1] + s[rg][site2] - 1

    #model += c >= (xsum( (s[app][l_site] * lats_apps[app][l_site] * 2 + z[app][l_site][s1_site] * lats_sites[l_site][s1_site] + z[app][s2_site][s3_site] * lats_sites[s2_site][s3_site] * 2) / app_charcs[app][3] for (app, l_site, s1_site, s2_site, s3_site) in product(range(apps), range(sites), range(sites), range(sites), range(sites))) / (apps * sites * sites * sites * sites))
    model += r >= xsum(x[rg][site] for (rg,site) in product(range(apps),range(sites))) / float(max_total_replicas) # TODO: Try with this constraint removed

    model.objective = maximize(xsum(a[app][conf][rg] for (app, conf, rg) in product(range(apps), range(num_confs), range(apps))) - r)

    #model.max_seconds = 300
    #model.max_seconds_same_incumbent = 10
    #model.max_nodes = 10000
    model.threads = 8
    model.optimize(max_seconds_same_incumbent=900)

    placements = {}

    sites_servers = []
    for i in range(sites):
        sites_servers.append([-1]*servers)

    pr_groups = {}
    for (rg, site) in product(range(apps),range(sites)):
        server_num = 0
        for temp_serv_num in range(servers):
            if sites_servers[site][temp_serv_num] >= 0:
                server_num += 1
        for i in range(0, int(x[rg][site].x)):
            if(rg in pr_groups.keys()):
                pr_groups[rg].append((resources[site][0], server_num))
            else:
                pr_groups[rg] = [(resources[site][0], server_num)]
            sites_servers[site][server_num] = rg
            server_num += 1

    for (app, conf, rg) in product(range(apps), range(num_confs), range(apps)):
        if int(a[app][conf][rg].x) == 1:
            placements[app] = pr_groups[rg]

    t_placements = []

    for i in range(len(app_charcs)):
        if i in placements:
            t_placements.append(placements[i])
        else:
            t_placements.append([])

    placements = t_placements

    return placements