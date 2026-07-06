"""
Script to join csv results obtained in Wigle API
"""
import pandas as pd
import os

path = 'wigle-RJ-results/results_rj'
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
dfs_list = []

output_path = os.path.join(path, 'wigle_results.csv')

for file in csv_files:
    complete_path = os.path.join(path, file)
    try:
        df = pd.read_csv(complete_path)
        dfs_list.append(df)
    except Exception as e:
        print(f"Error reading file {file}: {e}")

if dfs_list:
    final_df = pd.concat(dfs_list, ignore_index=True)
    final_df.to_csv(output_path, index=False)
    print("CSV files joined successfully! =) ")
else:
    print("No CSV file found.")