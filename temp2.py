import matplotlib.pyplot as plt
import pandas as pd

# Data provided
data = """
algo_name,number_of_apps,Avg,Min,Max
sm2_round_robin_min_sites,3,0.9,0,1
sm2_closest_min_sites,3,1.0,1,1
sm2_best_lat_min_sites,3,1.0,1,1
sm2_round_robin_max_sites,3,0.7,0,1
sm2_closest_max_sites,3,0.7,0,1
sm2_best_lat_max_sites,3,0.7,0,1
sm2_closest_max_sites_meet_lat,3,1.0,1,1
sm2_best_lat_max_sites_meet_lat,3,1.0,1,1
sm2_milp_max_sites,3,1.0,1,1
sm2_round_robin_min_sites,5,0.6,0,1
sm2_closest_min_sites,5,0.9,0,1
sm2_best_lat_min_sites,5,1.0,1,1
sm2_round_robin_max_sites,5,0.3,0,1
sm2_closest_max_sites,5,0.3,0,1
sm2_best_lat_max_sites,5,0.3,0,1
sm2_closest_max_sites_meet_lat,5,1.0,1,1
sm2_best_lat_max_sites_meet_lat,5,1.0,1,1
sm2_milp_max_sites,5,1.0,1,1
sm2_round_robin_min_sites,7,0.7,0,1
sm2_closest_min_sites,7,1.0,1,1
sm2_best_lat_min_sites,7,1.0,1,1
sm2_round_robin_max_sites,7,0.5,0,1
sm2_closest_max_sites,7,0.5,0,1
sm2_best_lat_max_sites,7,0.5,0,1
sm2_closest_max_sites_meet_lat,7,1.0,1,1
sm2_best_lat_max_sites_meet_lat,7,1.0,1,1
sm2_milp_max_sites,7,1.0,1,1
sm2_round_robin_min_sites,9,0.5,0,1
sm2_closest_min_sites,9,0.9,0,1
sm2_best_lat_min_sites,9,1.0,1,1
sm2_round_robin_max_sites,9,0.3,0,1
sm2_closest_max_sites,9,0.3,0,1
sm2_best_lat_max_sites,9,0.3,0,1
sm2_closest_max_sites_meet_lat,9,1.0,1,1
sm2_best_lat_max_sites_meet_lat,9,1.0,1,1
sm2_milp_max_sites,9,1.0,1,1
sm2_round_robin_min_sites,11,0.6,0,1
sm2_closest_min_sites,11,0.9,0,1
sm2_best_lat_min_sites,11,1.0,1,1
sm2_round_robin_max_sites,11,0.0,0,0
sm2_closest_max_sites,11,0.0,0,0
sm2_best_lat_max_sites,11,0.0,0,0
sm2_closest_max_sites_meet_lat,11,1.0,1,1
sm2_best_lat_max_sites_meet_lat,11,1.0,1,1
sm2_milp_max_sites,11,1.0,1,1
sm2_round_robin_min_sites,13,0.4,0,1
sm2_closest_min_sites,13,0.8,0,1
sm2_best_lat_min_sites,13,0.9,0,1
sm2_round_robin_max_sites,13,0.1,0,1
sm2_closest_max_sites,13,0.1,0,1
sm2_best_lat_max_sites,13,0.1,0,1
sm2_closest_max_sites_meet_lat,13,1.0,1,1
sm2_best_lat_max_sites_meet_lat,13,1.0,1,1
sm2_milp_max_sites,13,1.0,1,1
sm2_round_robin_min_sites,15,0.4,0,1
sm2_closest_min_sites,15,0.8,0,1
sm2_best_lat_min_sites,15,1.0,1,1
sm2_round_robin_max_sites,15,0.2,0,1
sm2_closest_max_sites,15,0.2,0,1
sm2_best_lat_max_sites,15,0.2,0,1
sm2_closest_max_sites_meet_lat,15,1.0,1,1
sm2_best_lat_max_sites_meet_lat,15,1.0,1,1
sm2_milp_max_sites,15,1.0,1,1
sm2_round_robin_min_sites,20,0.2,0,1
sm2_closest_min_sites,20,0.6,0,1
sm2_best_lat_min_sites,20,0.8,0,1
sm2_round_robin_max_sites,20,0.0,0,0
sm2_closest_max_sites,20,0.0,0,0
sm2_best_lat_max_sites,20,0.0,0,0
sm2_closest_max_sites_meet_lat,20,1.0,1,1
sm2_best_lat_max_sites_meet_lat,20,1.0,1,1
sm2_milp_max_sites,20,1.0,1,1
sm2_round_robin_min_sites,30,0.2,0,1
sm2_closest_min_sites,30,0.4,0,1
sm2_best_lat_min_sites,30,0.9,0,1
sm2_round_robin_max_sites,30,0.0,0,0
sm2_closest_max_sites,30,0.0,0,0
sm2_best_lat_max_sites,30,0.0,0,0
sm2_closest_max_sites_meet_lat,30,1.0,1,1
sm2_best_lat_max_sites_meet_lat,30,1.0,1,1
sm2_milp_max_sites,30,1.0,1,1
"""

# Convert the data string to a pandas DataFrame
data = [line.split(',') for line in data.strip().split('\n')]
df = pd.DataFrame(data[1:], columns=data[0])

# Convert columns to appropriate data types
df['number_of_apps'] = pd.to_numeric(df['number_of_apps'])
df['Avg'] = pd.to_numeric(df['Avg'])
df['Min'] = pd.to_numeric(df['Min'])
df['Max'] = pd.to_numeric(df['Max'])

# Pivot the data so that each algorithm is a separate column
pivot_df = df.pivot(index='number_of_apps', columns='algo_name', values='Avg')

# Plotting
plt.figure(figsize=(10, 6))

for column in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[column], marker='o', label=column)

plt.title('Average Values by Algorithm and Number of Apps')
plt.xlabel('Number of Apps')
plt.ylabel('Average Value')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
plt.show()
