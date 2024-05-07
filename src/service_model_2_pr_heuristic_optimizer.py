from .baas_utilities import *


def sm2_pr_closest_min_sites(app_charcs, resources):

    placements = []
    pr_groups = {}

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app_num in range(len(app_charcs)):
        app = app_charcs[app_num]
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        pr=app[5]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(float(num_replicas)/S)
        num_replicas = reps_per_site * S

        pr_key = (f,d,k,pr)

        selected_pr_group = None

        if pr_key in pr_groups.keys():
            for pr_group in pr_groups[pr_key]:
                if selected_pr_group == None:
                    if len(pr_group["apps"]) < NUM_REPS_PER_MACHINE:
                        sites = pr_group["sites"].keys()
                        sites_loc = []
                        for s in sites:
                            for z in resources:
                                if z[0] == s:
                                    sites_loc.append(z[2])
                        exp_lats = []
                        for j in range(len(sites)):
                            exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                        max_exp_lat = max(exp_lats)
                        if max_exp_lat <= app[3]:
                            selected_pr_group = pr_group
        
        if selected_pr_group == None:
            new_pr_group = {}
            temp_sites = {}
            t_resources = faster_sites(len(resources), app[4], resources)
            sites_assigned = 0
            for r in t_resources:
                if sites_assigned < S:
                    site_name = r[0]
                    if sites_machines[site_name] >= reps_per_site:
                        temp_start_server_num = r[3]-sites_machines[site_name]
                        temp_end_server_num = r[3]-sites_machines[site_name]+reps_per_site # not including
                        temp_sites[site_name] = list(range(temp_start_server_num, temp_end_server_num))
                        sites_assigned += 1
            if sites_assigned == S:
                sites = temp_sites.keys()
                sites_loc = []
                for s in sites:
                    for z in resources:
                        if z[0] == s:
                            sites_loc.append(z[2])
                exp_lats = []
                for j in range(len(sites)):
                    exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                max_exp_lat = max(exp_lats)
                if max_exp_lat <= app[3]:
                    for site_name in temp_sites.keys():
                        sites_machines[site_name] -= reps_per_site
                    new_pr_group["sites"] = temp_sites
                    new_pr_group["apps"] = []
                    if pr_key in pr_groups.keys():
                        pr_groups[pr_key].append(new_pr_group)
                    else:
                        pr_groups[pr_key] = [new_pr_group]
                    selected_pr_group = new_pr_group

        if selected_pr_group:
            for site in selected_pr_group["sites"]:
                for server in selected_pr_group["sites"][site]:
                    placement.append((site, server))
            selected_pr_group["apps"].append(app_num)
        placements.append(placement)

    return (placements, pr_groups, sites_machines)


def sm2_pr_best_lat_min_sites(app_charcs, resources):

    placements = []
    pr_groups = {}

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app_num in range(len(app_charcs)):
        app = app_charcs[app_num]
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        pr=app[5]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(float(num_replicas)/S)
        num_replicas = reps_per_site * S

        pr_key = (f,d,k,pr)

        selected_pr_group = None

        if pr_key in pr_groups.keys():
            for pr_group in pr_groups[pr_key]:
                if selected_pr_group == None:
                    if len(pr_group["apps"]) < NUM_REPS_PER_MACHINE:
                        sites = pr_group["sites"].keys()
                        sites_loc = []
                        for s in sites:
                            for z in resources:
                                if z[0] == s:
                                    sites_loc.append(z[2])
                        exp_lats = []
                        for j in range(len(sites)):
                            exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                        max_exp_lat = max(exp_lats)
                        if max_exp_lat <= app[3]:
                            selected_pr_group = pr_group
        
        if selected_pr_group == None:
            new_pr_group = {}
            temp_sites = {}
            
            available_sites = 0
            available_resources = []
            for r in resources:
                if sites_machines[r[0]] >= reps_per_site:
                    available_sites += 1
                    available_resources.append(r[:])

            if available_sites >= S:
                t_resources = fastest_sites(S, app[4], available_resources)
                sites_assigned = 0
                for r in t_resources:
                    if sites_assigned < S:
                        site_name = r[0]
                        if sites_machines[site_name] >= reps_per_site:
                            temp_start_server_num = r[3]-sites_machines[site_name]
                            temp_end_server_num = r[3]-sites_machines[site_name]+reps_per_site # not including
                            temp_sites[site_name] = list(range(temp_start_server_num, temp_end_server_num))
                            sites_assigned += 1
                if sites_assigned == S:
                    sites = temp_sites.keys()
                    sites_loc = []
                    for s in sites:
                        for z in resources:
                            if z[0] == s:
                                sites_loc.append(z[2])
                    exp_lats = []
                    for j in range(len(sites)):
                        exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                    max_exp_lat = max(exp_lats)
                    if max_exp_lat <= app[3]:
                        for site_name in temp_sites.keys():
                            sites_machines[site_name] -= reps_per_site
                        new_pr_group["sites"] = temp_sites
                        new_pr_group["apps"] = []
                        if pr_key in pr_groups.keys():
                            pr_groups[pr_key].append(new_pr_group)
                        else:
                            pr_groups[pr_key] = [new_pr_group]
                        selected_pr_group = new_pr_group

        if selected_pr_group:
            for site in selected_pr_group["sites"]:
                for server in selected_pr_group["sites"][site]:
                    placement.append((site, server))
            selected_pr_group["apps"].append(app_num)
        placements.append(placement)

    return (placements, pr_groups, sites_machines)


def sm2_pr_closest_max_sites(app_charcs, resources):

    placements = []
    pr_groups = {}

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app_num in range(len(app_charcs)):
        app = app_charcs[app_num]
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        pr=app[5]

        min_sites = 2*app[1]+1
        max_sites = min(3*f + 2*(k+d) + 1, len(resources))

        for S in range(max_sites, min_sites-1, -1):

            u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
            num_replicas = 3*f+2*u+1
            reps_per_site = math.ceil(float(num_replicas)/float(S))
            num_replicas = reps_per_site * S

            pr_key = (f,d,k,pr,S)

            selected_pr_group = None

            if pr_key in pr_groups.keys():
                for pr_group in pr_groups[pr_key]:
                    if selected_pr_group == None:
                        if len(pr_group["apps"]) < NUM_REPS_PER_MACHINE:
                            sites = pr_group["sites"].keys()
                            sites_loc = []
                            for s in sites:
                                for z in resources:
                                    if z[0] == s:
                                        sites_loc.append(z[2])
                            exp_lats = []
                            for j in range(len(sites)):
                                exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                            max_exp_lat = max(exp_lats)
                            if max_exp_lat <= app[3]:
                                selected_pr_group = pr_group
        
            if selected_pr_group == None:
                new_pr_group = {}
                temp_sites = {}
                t_resources = faster_sites(len(resources), app[4], resources)
                sites_assigned = 0
                for r in t_resources:
                    if sites_assigned < S:
                        site_name = r[0]
                        if sites_machines[site_name] >= reps_per_site:
                            temp_start_server_num = r[3]-sites_machines[site_name]
                            temp_end_server_num = r[3]-sites_machines[site_name]+reps_per_site # not including
                            temp_sites[site_name] = list(range(temp_start_server_num, temp_end_server_num))
                            sites_assigned += 1
                if sites_assigned == S:
                    sites = temp_sites.keys()
                    sites_loc = []
                    for s in sites:
                        for z in resources:
                            if z[0] == s:
                                sites_loc.append(z[2])
                    exp_lats = []
                    for j in range(len(sites)):
                        exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                    max_exp_lat = max(exp_lats)
                    if max_exp_lat <= app[3]:
                        for site_name in temp_sites.keys():
                            sites_machines[site_name] -= reps_per_site
                        new_pr_group["sites"] = temp_sites
                        new_pr_group["apps"] = []
                        if pr_key in pr_groups.keys():
                            pr_groups[pr_key].append(new_pr_group)
                        else:
                            pr_groups[pr_key] = [new_pr_group]
                        selected_pr_group = new_pr_group

            if selected_pr_group:
                for site in selected_pr_group["sites"]:
                    for server in selected_pr_group["sites"][site]:
                        placement.append((site, server))
                selected_pr_group["apps"].append(app_num)
                break

        placements.append(placement)

    return (placements, pr_groups, sites_machines)


def sm2_pr_best_lat_max_sites(app_charcs, resources):

    placements = []
    pr_groups = {}

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app_num in range(len(app_charcs)):
        app = app_charcs[app_num]
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        pr=app[5]

        min_sites = 2*app[1]+1
        max_sites = min(3*f + 2*(k+d) + 1, len(resources))

        for S in range(max_sites, min_sites-1, -1):

            u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
            num_replicas = 3*f+2*u+1
            reps_per_site = math.ceil(float(num_replicas)/float(S))
            num_replicas = reps_per_site * S

            pr_key = (f,d,k,pr,S)

            selected_pr_group = None

            if pr_key in pr_groups.keys():
                for pr_group in pr_groups[pr_key]:
                    if selected_pr_group == None:
                        if len(pr_group["apps"]) < NUM_REPS_PER_MACHINE:
                            sites = pr_group["sites"].keys()
                            sites_loc = []
                            for s in sites:
                                for z in resources:
                                    if z[0] == s:
                                        sites_loc.append(z[2])
                            exp_lats = []
                            for j in range(len(sites)):
                                exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                            max_exp_lat = max(exp_lats)
                            if max_exp_lat <= app[3]:
                                selected_pr_group = pr_group
        
            if selected_pr_group == None:
                new_pr_group = {}
                temp_sites = {}

                available_sites = 0
                available_resources = []
                for r in resources:
                    if sites_machines[r[0]] >= reps_per_site:
                        available_sites += 1
                        available_resources.append(r[:])

                if available_sites >= S:
                    t_resources = fastest_sites(S, app[4], available_resources)
                    sites_assigned = 0
                    for r in t_resources:
                        if sites_assigned < S:
                            site_name = r[0]
                            if sites_machines[site_name] >= reps_per_site:
                                temp_start_server_num = r[3]-sites_machines[site_name]
                                temp_end_server_num = r[3]-sites_machines[site_name]+reps_per_site # not including
                                temp_sites[site_name] = list(range(temp_start_server_num, temp_end_server_num))
                                sites_assigned += 1
                    if sites_assigned == S:
                        sites = temp_sites.keys()
                        sites_loc = []
                        for s in sites:
                            for z in resources:
                                if z[0] == s:
                                    sites_loc.append(z[2])
                        exp_lats = []
                        for j in range(len(sites)):
                            exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                        max_exp_lat = max(exp_lats)
                        if max_exp_lat <= app[3]:
                            for site_name in temp_sites.keys():
                                sites_machines[site_name] -= reps_per_site
                            new_pr_group["sites"] = temp_sites
                            new_pr_group["apps"] = []
                            if pr_key in pr_groups.keys():
                                pr_groups[pr_key].append(new_pr_group)
                            else:
                                pr_groups[pr_key] = [new_pr_group]
                            selected_pr_group = new_pr_group

            if selected_pr_group:
                for site in selected_pr_group["sites"]:
                    for server in selected_pr_group["sites"][site]:
                        placement.append((site, server))
                selected_pr_group["apps"].append(app_num)
                break

        placements.append(placement)

    return (placements, pr_groups, sites_machines)