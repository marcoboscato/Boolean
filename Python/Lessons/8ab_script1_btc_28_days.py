# -*- coding: utf-8 -*-
"""
Boolean Data Analytics Course

This script creates a DataFrame containing the current_price, the market_cap 
and the total_volume of transactions between bitcoin and each of the 61 
available tickers for the last 28 days.
"""

import pandas as pd
import requests
import seaborn as sns
import datetime
import time

# initalisation of parameters 
end_date = datetime.date.today()  # <-- today's date
days_back = 28  # <-- lookback window

# list of dates from the last 28 days
date_list = pd.date_range(end=end_date, periods=days_back) \
    .strftime("%d-%m-%Y").tolist()  # format dates as required by the API

# initialise an empty DataFrame named "df"
df = pd.DataFrame([])

# loop through the list of dates and, at each cycle: 
# - make an HTTP request to the CoinGecko API 
# - retrieve the information we need in JSON format
# - save the data to a temporary DataFrame named "tmp_df"
# - add the current cycle's date to a new column name "date" in the DataFrame
# - append the temporary DataFrame to the "df" DataFrame
max_retries = 5
for dt in date_list:
    print(f"\nProcessing date: {dt}")
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/history?date=' + dt
    success = False
    for attempt in range(1, max_retries + 1):
        r = requests.get(url)
        print(f"Attempt {attempt}/{max_retries} - Status code: {r.status_code}")

        if r.status_code == 429:
            wait = 60 * attempt  # increasing wait: 60s, 120s, 180s, ...
            print(f"Rate limited (429). Waiting {wait} seconds before retry...")
            time.sleep(wait)
            continue

        try:
            data = r.json()
            if 'market_data' in data:
                print(f"'market_data' found for {dt}. Building DataFrame...")
                tmp_df = pd.DataFrame.from_dict(data['market_data']).reset_index()
                tmp_df['date'] = dt
                df = pd.concat([df, tmp_df])
                print(f"Appended data for {dt}. df shape: {df.shape}")
                success = True
                break
            else:
                print(f"No 'market_data' for date {dt}. Response keys: {list(data.keys())}")
                break
        except Exception as e:
            print(f"Error parsing response for {dt}: {e}")
            break

    if not success:
        print(f"Failed to get data for {dt} after {attempt} attempt(s)")

    # delay between requests to avoid hitting rate limit
    time.sleep(15)

# check if any data was collected before proceeding
if df.empty:
    print("\nNo data was collected. Cannot proceed with plotting.")
else:
    # re-index the DataFrame to avoid having duplicates in the index
    df.reset_index(inplace=True)

    # convert the date variable to DateTime
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

    # finally we plot the time series for a specific exchange: BTC vs EUR
    sns.set(rc={'figure.figsize':(13, 7)})
    sns.lineplot(x='date', y='current_price', data=df[df['index']=='eur'])
