import matplotlib.pyplot as plt
import pandas as pd

# Data provided
data = """
algo_name,number_of_apps,Avg,Min,Max
sm2_round_robin_min_sites,3,103.44,75,134
sm2_closest_min_sites,3,104.3,75,134
sm2_best_lat_min_sites,3,104.3,75,134
sm2_round_robin_max_sites,3,52.0,43,63
sm2_closest_max_sites,3,52.0,43,63
sm2_best_lat_max_sites,3,52.0,43,63
sm2_closest_max_sites_meet_lat,3,51.6,43,63
sm2_best_lat_max_sites_meet_lat,3,51.4,43,63
sm2_milp_max_sites,3,46.7,36,61
sm2_round_robin_min_sites,5,193.67,117,253
sm2_closest_min_sites,5,185.78,117,254
sm2_best_lat_min_sites,5,186.1,117,254
sm2_round_robin_max_sites,5,104.33,70,135
sm2_closest_max_sites,5,104.33,70,135
sm2_best_lat_max_sites,5,104.33,70,135
sm2_closest_max_sites_meet_lat,5,109.89,70,174
sm2_best_lat_max_sites_meet_lat,5,112.1,70,174
sm2_milp_max_sites,5,100.6,56,165
sm2_round_robin_min_sites,7,298.43,223,363
sm2_closest_min_sites,7,304.8,223,376
sm2_best_lat_min_sites,7,304.8,223,376
sm2_round_robin_max_sites,7,143.2,115,171
sm2_closest_max_sites,7,143.2,115,171
sm2_best_lat_max_sites,7,143.2,115,171
sm2_closest_max_sites_meet_lat,7,153.6,115,189
sm2_best_lat_max_sites_meet_lat,7,153.3,115,189
sm2_milp_max_sites,7,141.6,100,180
sm2_round_robin_min_sites,9,390.2,328,492
sm2_closest_min_sites,9,388.67,328,492
sm2_best_lat_min_sites,9,381.0,312,492
sm2_round_robin_max_sites,9,194.33,160,234
sm2_closest_max_sites,9,194.33,160,234
sm2_best_lat_max_sites,9,194.33,160,234
sm2_closest_max_sites_meet_lat,9,200.89,160,248
sm2_best_lat_max_sites_meet_lat,9,197.8,160,248
sm2_milp_max_sites,9,184.7,150,236
sm2_round_robin_min_sites,11,436.83,364,526
sm2_closest_min_sites,11,435.88,364,526
sm2_best_lat_min_sites,11,438.22,364,526
sm2_round_robin_max_sites,11,0.0,0.0,0.0
sm2_closest_max_sites,11,0.0,0.0,0.0
sm2_best_lat_max_sites,11,0.0,0.0,0.0
sm2_closest_max_sites_meet_lat,11,234.56,193,349
sm2_best_lat_max_sites_meet_lat,11,238.0,193,349
sm2_milp_max_sites,11,217.8,166,334
sm2_round_robin_min_sites,13,519.0,468,582
sm2_closest_min_sites,13,525.5,445,584
sm2_best_lat_min_sites,13,519.25,445,584
sm2_round_robin_max_sites,13,233.0,233,233
sm2_closest_max_sites,13,233.0,233,233
sm2_best_lat_max_sites,13,233.0,233,233
sm2_closest_max_sites_meet_lat,13,263.33,220,297
sm2_best_lat_max_sites_meet_lat,13,265.8,220,304
sm2_milp_max_sites,13,243.9,199,286
sm2_round_robin_min_sites,15,592.0,462,694
sm2_closest_min_sites,15,568.67,462,694
sm2_best_lat_min_sites,15,553.2,462,658
sm2_round_robin_max_sites,15,327.5,322,333
sm2_closest_max_sites,15,327.5,322,333
sm2_best_lat_max_sites,15,327.5,322,333
sm2_closest_max_sites_meet_lat,15,311.62,246,414
sm2_best_lat_max_sites_meet_lat,15,329.4,246,421
sm2_milp_max_sites,15,302.5,212,390
sm2_round_robin_min_sites,20,889.0,889,889
sm2_closest_min_sites,20,749.33,716,788
sm2_best_lat_min_sites,20,712.33,677,744
sm2_round_robin_max_sites,20,0.0,0.0,0.0
sm2_closest_max_sites,20,0.0,0.0,0.0
sm2_best_lat_max_sites,20,0.0,0.0,0.0
sm2_closest_max_sites_meet_lat,20,409.43,329,452
sm2_best_lat_max_sites_meet_lat,20,424.8,323,564
sm2_milp_max_sites,20,391.1,288,541
sm2_round_robin_min_sites,30,0.0,0.0,0.0
sm2_closest_min_sites,30,0.0,0.0,0.0
sm2_best_lat_min_sites,30,0.0,0.0,0.0
sm2_round_robin_max_sites,30,0.0,0.0,0.0
sm2_closest_max_sites,30,0.0,0.0,0.0
sm2_best_lat_max_sites,30,0.0,0.0,0.0
sm2_closest_max_sites_meet_lat,30,636.33,548,749
sm2_best_lat_max_sites_meet_lat,30,633.7,548,737
sm2_milp_max_sites,30,584.0,484,701
"""

# Convert the data string to a pandas DataFrame
data = [line.split(',') for line in data.strip().split('\n')]
df = pd.DataFrame(data[1:], columns=data[0])

# Remove duplicates
df = df.drop_duplicates()

# Convert 'Avg' column to numeric
df['Avg'] = pd.to_numeric(df['Avg'], errors='coerce')

# Group by algorithm name and calculate average of Avg column
avg_data = df.groupby('algo_name')['Avg'].mean().dropna()

# Plotting
plt.figure(figsize=(10, 6))
avg_data.plot(kind='bar', color='skyblue')
plt.title('Average Values by Algorithm')
plt.xlabel('Algorithm')
plt.ylabel('Average Value')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
