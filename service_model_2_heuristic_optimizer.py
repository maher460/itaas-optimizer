from baas_utilities import *


def sm2_round_robin_min_sites(app_charcs, resources):
    placements = []
    cur_site = 0
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)

        available_sites = 0
        for site_reps in sites_machines.values():
            if site_reps >= reps_per_site:
                available_sites += 1

        if available_sites >= S:
            i=0
            j=0
            while i<S and j<len(resources):
                site_name = resources[cur_site][0]
                if sites_machines[site_name] >= reps_per_site:
                    m=0
                    l=0
                    while l < resources[cur_site][3] and m < reps_per_site:
                        sitemach = site_name + str(l)
                        if(machines[sitemach] < 4):
                            placement.append((site_name, l))
                            machines[sitemach] += 1
                            m += 1
                            if machines[sitemach] == 4:
                                sites_machines[site_name] -= 1
                        l += 1
                    i+=1
                cur_site += 1
                if(cur_site >= len(resources)):
                    cur_site = 0
                j+=1
        #print(placement)
        placements.append(placement)

    return placements


def sm2_closest_min_sites(app_charcs, resources):
    placements = []
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)

        available_sites = 0
        for site_reps in sites_machines.values():
            if site_reps >= reps_per_site:
                available_sites += 1

        if available_sites >= S:
            t_resources = faster_sites(len(resources), app[4], resources)
            i=0
            j=0
            while i<S and j<len(t_resources):
                site_name = t_resources[j][0]
                if sites_machines[site_name] >= reps_per_site:
                    m=0
                    l=0
                    while l < t_resources[j][3] and m < reps_per_site:
                        sitemach = site_name + str(l)
                        if(machines[sitemach] < 4):
                            placement.append((site_name, l))
                            machines[sitemach] += 1
                            m += 1
                            if machines[sitemach] == 4:
                                sites_machines[site_name] -= 1
                        l += 1
                    i+=1
                j+=1
        #print(placement)
        placements.append(placement)

    return placements


def sm2_best_lat_min_sites(app_charcs, resources):
    placements = []
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)

        available_sites = 0
        available_resources = []
        for r in resources:
            if sites_machines[r[0]] >= reps_per_site:
                available_sites += 1
                available_resources.append(r[:])

        # for site_reps in sites_machines.values():
        #     if site_reps >= reps_per_site:
        #         available_sites += 1

        if available_sites >= S:
            t_resources = fastest_sites(S, app[4], available_resources)
            i=0
            j=0
            while i<S and j<len(t_resources):
                site_name = t_resources[j][0]
                if sites_machines[site_name] >= reps_per_site:
                    m=0
                    l=0
                    while l < t_resources[j][3] and m < reps_per_site:
                        sitemach = site_name + str(l)
                        if(machines[sitemach] < 4):
                            placement.append((site_name, l))
                            machines[sitemach] += 1
                            m += 1
                            if machines[sitemach] == 4:
                                sites_machines[site_name] -= 1
                        l += 1
                    i+=1
                j+=1
        #print(placement)
        placements.append(placement)

    return placements


def sm2_round_robin_max_sites(app_charcs, resources):
    placements = []
    cur_site = 0
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = min(3*f+2*(k+d)+1, len(resources))
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)
        num_replicas = reps_per_site * S

        available_sites = 0
        for site_reps in sites_machines.values():
            if site_reps >= reps_per_site:
                available_sites += 1

        if available_sites >= S:
            i=0
            j=0
            while i<S and j<len(resources):
                site_name = resources[cur_site][0]
                if sites_machines[site_name] >= reps_per_site:
                    m=0
                    l=0
                    while l < resources[cur_site][3] and m < reps_per_site:
                        sitemach = site_name + str(l)
                        if(machines[sitemach] < 4):
                            placement.append((site_name, l))
                            machines[sitemach] += 1
                            m += 1
                            if machines[sitemach] == 4:
                                sites_machines[site_name] -= 1
                        l += 1
                    i+=1
                cur_site += 1
                if(cur_site >= len(resources)):
                    cur_site = 0
                j+=1
        #print(placement)
        placements.append(placement)

    return placements


def sm2_closest_max_sites(app_charcs, resources):
    placements = []
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = min(3*f+2*(k+d)+1, len(resources))
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)
        num_replicas = reps_per_site * S

        available_sites = 0
        available_resources = []
        for r in resources:
            if sites_machines[r[0]] >= reps_per_site:
                available_sites += 1
                available_resources.append(r[:])

        if available_sites >= S:
            t_resources = faster_sites(S, app[4], available_resources)
            i=0
            j=0
            while i<S and j<len(t_resources):
                site_name = t_resources[j][0]
                if sites_machines[site_name] >= reps_per_site:
                    m=0
                    l=0
                    while l < t_resources[j][3] and m < reps_per_site:
                        sitemach = site_name + str(l)
                        if(machines[sitemach] < 4):
                            placement.append((site_name, l))
                            machines[sitemach] += 1
                            m += 1
                            if machines[sitemach] == 4:
                                sites_machines[site_name] -= 1
                        l += 1
                    i+=1
                j+=1
        #print(placement)
        placements.append(placement)

    return placements


def sm2_best_lat_max_sites(app_charcs, resources):
    placements = []
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = min(3*f+2*(k+d)+1, len(resources))
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)
        num_replicas = reps_per_site * S

        available_sites = 0
        available_resources = []
        for r in resources:
            if sites_machines[r[0]] >= reps_per_site:
                available_sites += 1
                available_resources.append(r[:])

        # for site_reps in sites_machines.values():
        #     if site_reps >= reps_per_site:
        #         available_sites += 1

        if available_sites >= S:
            t_resources = fastest_sites(S, app[4], available_resources)
            i=0
            j=0
            while i<S and j<len(t_resources):
                site_name = t_resources[j][0]
                if sites_machines[site_name] >= reps_per_site:
                    m=0
                    l=0
                    while l < t_resources[j][3] and m < reps_per_site:
                        sitemach = site_name + str(l)
                        if(machines[sitemach] < 4):
                            placement.append((site_name, l))
                            machines[sitemach] += 1
                            m += 1
                            if machines[sitemach] == 4:
                                sites_machines[site_name] -= 1
                        l += 1
                    i+=1
                j+=1
        #print(placement)
        placements.append(placement)

    return placements


def sm2_closest_max_sites_meet_lat(app_charcs, resources):
    placements = []
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        min_sites = 2*d+1
        max_sites = min(3*f+2*(k+d)+1, len(resources))

        for S in range(max_sites, min_sites-1, -1):

            u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
            num_replicas = 3*f+2*u+1
            reps_per_site = math.ceil(num_replicas/S)
            num_replicas = reps_per_site * S

            available_sites = 0
            available_resources = []
            for r in resources:
                if sites_machines[r[0]] >= reps_per_site:
                    available_sites += 1
                    available_resources.append(r[:])

            if available_sites >= S:
                t_resources = faster_sites(S, app[4], available_resources)

                sites_loc = []
                for z in t_resources:
                    sites_loc.append(z[2])
                exp_lats = []
                for j in range(len(sites_loc)):
                    exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                max_exp_lat = max(exp_lats)
                if max_exp_lat > app[3]:
                    continue
                
                i=0
                j=0
                while i<S and j<len(t_resources):
                    site_name = t_resources[j][0]
                    if sites_machines[site_name] >= reps_per_site:
                        m=0
                        l=0
                        while l < t_resources[j][3] and m < reps_per_site:
                            sitemach = site_name + str(l)
                            if(machines[sitemach] < 4):
                                placement.append((site_name, l))
                                machines[sitemach] += 1
                                m += 1
                                if machines[sitemach] == 4:
                                    sites_machines[site_name] -= 1
                            l += 1
                        i+=1
                    j+=1
            #print(placement)
            break
        placements.append(placement)

    return placements


def sm2_best_lat_max_sites_meet_lat(app_charcs, resources):
    placements = []
    machines = defaultdict(int)

    sites_machines = defaultdict(int)
    for r in resources:
        sites_machines[r[0]] = r[3]
    
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        min_sites = 2*d+1
        max_sites = min(3*f+2*(k+d)+1, len(resources))

        for S in range(max_sites, min_sites-1, -1):

            u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
            num_replicas = 3*f+2*u+1
            reps_per_site = math.ceil(num_replicas/S)
            num_replicas = reps_per_site * S

            available_sites = 0
            available_resources = []
            for r in resources:
                if sites_machines[r[0]] >= reps_per_site:
                    available_sites += 1
                    available_resources.append(r[:])

            if available_sites >= S:
                t_resources = fastest_sites(S, app[4], available_resources)

                sites_loc = []
                for z in t_resources:
                    sites_loc.append(z[2])
                exp_lats = []
                for j in range(len(sites_loc)):
                    exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
                max_exp_lat = max(exp_lats)
                if max_exp_lat > app[3]:
                    continue
                
                i=0
                j=0
                while i<S and j<len(t_resources):
                    site_name = t_resources[j][0]
                    if sites_machines[site_name] >= reps_per_site:
                        m=0
                        l=0
                        while l < t_resources[j][3] and m < reps_per_site:
                            sitemach = site_name + str(l)
                            if(machines[sitemach] < 4):
                                placement.append((site_name, l))
                                machines[sitemach] += 1
                                m += 1
                                if machines[sitemach] == 4:
                                    sites_machines[site_name] -= 1
                            l += 1
                        i+=1
                    j+=1
            #print(placement)
            break
        placements.append(placement)

    return placements
