from .baas_utilities import *
import math

def sm1_round_robin_min_sites(app_charcs, resources):
    placements = []
    cur_site = 0
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)
        num_replicas = reps_per_site * S

        for i in range(S):
            site_name = resources[cur_site][0]
            for j in range(reps_per_site):
                placement.append(site_name)
            cur_site += 1
            if(cur_site >= len(resources)):
                cur_site = 0
        placements.append(placement)
    return placements


def sm1_closest_min_sites(app_charcs, resources):
    placements = []
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)
        num_replicas = reps_per_site * S

        fast_sites = faster_sites(S, app[4], resources)

        for i in range(S):
            site_name = fast_sites[i][0]
            for j in range(reps_per_site):
                placement.append(site_name)
        placements.append(placement)
    return placements


def sm1_best_lat_min_sites(app_charcs, resources):
    placements = []
    for app in app_charcs:
        placement = []
        f=app[0]
        d=app[1]
        k=app[2]
        S = 2*app[1]+1
        u = math.ceil(float(3*f*d+d+S*k)/float(S-2*d))
        num_replicas = 3*f+2*u+1
        reps_per_site = math.ceil(num_replicas/S)
        num_replicas = reps_per_site * S

        fast_sites = fastest_sites(S, app[4], resources)

        for i in range(S):
            site_name = fast_sites[i][0]
            for j in range(reps_per_site):
                placement.append(site_name)
        placements.append(placement)
    return placements


def sm1_round_robin_max_sites(app_charcs, resources):
    placements = []
    cur_site = 0
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

        for i in range(S):
            site_name = resources[cur_site][0]
            for j in range(reps_per_site):
                placement.append(site_name)
            cur_site += 1
            if(cur_site >= len(resources)):
                cur_site = 0
        placements.append(placement)
    return placements


def sm1_closest_max_sites(app_charcs, resources):
    placements = []
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

        fast_sites = faster_sites(S, app[4], resources)

        for i in range(S):
            site_name = fast_sites[i][0]
            for j in range(reps_per_site):
                placement.append(site_name)
        placements.append(placement)
    return placements


def sm1_best_lat_max_sites(app_charcs, resources):
    placements = []
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

        fast_sites = fastest_sites(S, app[4], resources)

        for i in range(S):
            site_name = fast_sites[i][0]
            for j in range(reps_per_site):
                placement.append(site_name)
        placements.append(placement)
    return placements


def sm1_closest_max_sites_meet_lat(app_charcs, resources):
    placements = []
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

            fast_sites = faster_sites(S, app[4], resources)

            sites_loc = []
            for z in fast_sites:
                sites_loc.append(z[2])
            exp_lats = []
            for j in range(len(sites_loc)):
                exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
            max_exp_lat = max(exp_lats)
            if max_exp_lat > app[3]:
                continue

            for i in range(S):
                site_name = fast_sites[i][0]
                for j in range(reps_per_site):
                    placement.append(site_name)
            break
        placements.append(placement)

    return placements


def sm1_best_lat_max_sites_meet_lat(app_charcs, resources):
    placements = []
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

            fast_sites = fastest_sites(S, app[4], resources)

            sites_loc = []
            for z in fast_sites:
                sites_loc.append(z[2])
            exp_lats = []
            for j in range(len(sites_loc)):
                exp_lats.append(calc_lat(app[4], sites_loc[j], sites_loc))
            max_exp_lat = max(exp_lats)
            if max_exp_lat > app[3]:
                continue

            for i in range(S):
                site_name = fast_sites[i][0]
                for j in range(reps_per_site):
                    placement.append(site_name)
            break
        placements.append(placement)

    return placements
