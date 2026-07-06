from dotenv import load_dotenv
import datetime
import os
import time
import pandas as pd
import requests

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

BASE_URL = "https://api.wigle.net/api/v2/network/search"
REQUEST_DELAY = 5 
MAX_RETRIES = 3

QUADRANTS = "etl_scripts/quadrants_rj.csv"
OUTPUT_DIR = "wigle_data/wigleRJ-results/results_rj"
RESUME_DIR = "wigle_data/wigleRJ-results/resume_logs" #directory for 'searchAfter' logs

headers = {
    "Authorization": f"Basic {API_TOKEN}"
}

try:
    df_quadrants = pd.read_csv(QUADRANTS)
except FileNotFoundError:
    raise FileNotFoundError(f"File {QUADRANTS} not found.")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESUME_DIR, exist_ok=True)


# iterates over each quadrant to fetch data from the WiGle API
for index, row in df_quadrants.iterrows():
    latrange1 = row["latrange1"]
    latrange2 = row["latrange2"]
    longrange1 = row["longrange1"]
    longrange2 = row["longrange2"]

    quadrant_id = f"quad_{latrange1:.4f}_{longrange1:.4f}".replace('.', '_')
    results_filepath = os.path.join(OUTPUT_DIR, f"{quadrant_id}.csv")
    resume_filepath = os.path.join(RESUME_DIR, f"{quadrant_id}.log")

    print("-" * 60)
    print(f"Processing {index + 1}/{len(df_quadrants)}: {quadrant_id} quadrant")

    query_params = {
        "latrange1": latrange1,
        "latrange2": latrange2,
        "longrange1": longrange1,
        "longrange2": longrange2,
    }

    #checks if a file exists for the current quadrant to resume collection from its search_after
    if os.path.exists(resume_filepath):        
        try:
            with open(resume_filepath, 'r') as f:
                searchAfter = f.read().strip()
            if searchAfter == "complete":
                continue
            if not searchAfter:
                searchAfter = None           
        except Exception as e:
            searchAfter = None


    current_count = 0
    total_count = None
    retries = 0
    pages = 0
    complete_quadrant = False

    while True: 
        try:
            if searchAfter:
                query_params["searchAfter"] = searchAfter

            response = requests.get(
                BASE_URL, 
                params=query_params, 
                headers=headers, 
                timeout=(10, 60)
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                if total_count is None:
                    total_count = data.get("totalResults", 0)
                    print(f"Total of new results found in this quad: {total_count}")

                if not results:
                    print("No other results found.")
                    complete_quadrant = True
                    with open(resume_filepath, 'w') as f:
                        f.write("complete")
                    break

                # save results in csv
                file_exists = os.path.exists(results_filepath)
                df = pd.DataFrame(results)
                df.to_csv(
                    results_filepath, 
                    mode='a', 
                    index=False,
                    header=not file_exists
                )

                current_count += len(results)
                pages += 1
                searchAfter = data.get("searchAfter") #gets new searchAfter token

                #saves searchAfter in log if it exists
                if searchAfter:
                    with open(resume_filepath, 'w') as f:
                        f.write(searchAfter)
                else: 
                    complete_quadrant = True
                    break

                retries = 0
                time.sleep(REQUEST_DELAY)

            #error treatments
            elif response.status_code == 401:
                print("ERROR 401: Invalid Token.")
                break
            elif response.status_code == 429:
                print("ERROR 429: Too many requests. Sleep for 60 seconds.")
                time.sleep(60)
            else:
                print(f"ERROR {response.status_code}: {response.text}")
                break

        except(
            requests.exceptions.Timeout, 
            requests.exceptions.ConnectionError
        ) as e:
            retries += 1
            print(f"Timeout: {e}. Try {retries}/{MAX_RETRIES}.")
            if retries >= MAX_RETRIES:
                print("Max retries achieved")
                break
            time.sleep(REQUEST_DELAY * 5)
        except Exception as e:
            print(f"Unexpectd: {e}")
            break
    
    #if quadrant is complete, writes "complete" in serachAfter log
    if complete_quadrant:
        if os.path.exists(resume_filepath):
            with open(resume_filepath, 'w') as f:
                f.write("complete")


print("-" * 60)
print("Finished.")