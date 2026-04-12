#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boolean Data Analytics Course

This script retrieves data from the CoinGecko API for the last 28 days and, 
for each day retrieved, saves the results to a csv file in the 'btc' folder.
"""

import pandas as pd
import requests
import datetime
import os

# set the directory to our class
os.chdir(os.path.dirname(__file__))

# initalisation of parameters
end_date = datetime.date.today()   # <-- today's date
days_back = 10   # <-- lookback window

# list of dates from the last 28 days
date_list = pd.date_range(end=end_date, periods=days_back) \
    .strftime("%d-%m-%Y").tolist()   # format dates as required by the API

# create a directory where to store all the files that we're going to generate
os.makedirs('data/btc/2026', exist_ok=True)

# loop through the list of dates and, at each cycle: 
# - make an HTTP request to the CoinGecko API 
# - retrieve the information we need in JSON format
# - save the data to a temporary DataFrame named "tmp_df"
# - add the current cycle's date to a new column name "date" in the DataFrame
# - save the temporary DataFrame to a .csv file in your local folder
files_written = []
errors = []

import time

for dt in date_list:
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/history?date=' + dt
    max_retries = 3
    attempt = 0
    while attempt < max_retries:
        print(f"\n[INFO] Requesting data for {dt} (attempt {attempt+1}/{max_retries}) -> {url}")
        try:
            cg_response = requests.get(url)
            print(f"[DEBUG] Status code: {cg_response.status_code}")
            cg_json = cg_response.json()
        except Exception as e:
            print(f"[ERROR] Exception during request or JSON parsing for {dt}: {e}")
            errors.append((dt, f"request/json attempt {attempt+1}", str(e)))
            break

        if cg_response.status_code == 429:
            print(f"[RATE LIMIT] Status code 429 for {dt}. Waiting 60 seconds before retry...")
            attempt += 1
            time.sleep(60)
            continue
        elif cg_response.status_code != 200:
            error_msg = cg_json.get('status', {}).get('error_message', 'Unknown error')
            print(f"[ERROR] Status code {cg_response.status_code} for {dt} | {error_msg}")
            errors.append((dt, f"status_code {cg_response.status_code}", error_msg))
            break

        if 'market_data' not in cg_json:
            print(f"[WARN] No 'market_data' found for {dt}. Response keys: {list(cg_json.keys())}")
            errors.append((dt, "no_market_data", str(cg_json)))
            break

        try:
            tmp_df = pd.DataFrame.from_dict(cg_json['market_data']).reset_index()
            tmp_df['date'] = dt
            filename = f'data/btc/2026/btc_{dt}.csv'
            tmp_df.to_csv(filename, index=False)
            print(f"[SUCCESS] Data for {dt} saved to {filename} | shape: {tmp_df.shape}")
            files_written.append(filename)
        except Exception as e:
            print(f"[ERROR] Exception during DataFrame creation or file write for {dt}: {e}")
            errors.append((dt, "dataframe/write", str(e)))
        break
    else:
        print(f"[FAILURE] Max retries reached for {dt}. Skipping.")
        errors.append((dt, "max_retries", "Gave up after 3 attempts due to repeated 429 errors."))

print(f"\n[SUMMARY] Files written: {len(files_written)}")
for f in files_written:
    print(f"  - {f}")

print(f"[SUMMARY] Errors encountered: {len(errors)}")
for dt, etype, msg in errors:
    print(f"  - {dt} [{etype}]: {msg}")

print(f"[INFO] Files in data/btc/2026: {os.listdir('data/btc/2026')}")
