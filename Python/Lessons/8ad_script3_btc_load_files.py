#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boolean Data Analytics Course

This script loops through each of the files in the 'btc' folder and appends
them to an initially empty DataFrame. 
"""

import pandas as pd
import seaborn as sns
import os


# set the directory to the folder containing this script
os.chdir(os.path.dirname(__file__))

# list all the contents of the 'btc' folder
DATA_FOLDER = 'data/btc/2026'
os.listdir(DATA_FOLDER)

files = os.listdir(DATA_FOLDER)
df = pd.DataFrame([])
files_loaded = []
errors = []

for file in files:
    if not file.endswith('.csv'):
        print(f"[SKIP] Not a CSV file: {file}")
        continue
    file_path = os.path.join(DATA_FOLDER, file)
    print(f"[INFO] Loading file: {file_path}")
    try:
        tmp_df = pd.read_csv(file_path)
        if 'date' not in tmp_df.columns:
            print(f"[WARN] 'date' column missing in {file}")
        df = pd.concat([df, tmp_df], ignore_index=True)
        print(f"[SUCCESS] Loaded {file} | shape: {tmp_df.shape}")
        files_loaded.append(file)
    except Exception as e:
        print(f"[ERROR] Failed to load {file}: {e}")
        errors.append((file, str(e)))

print(f"\n[SUMMARY] Files loaded: {len(files_loaded)}")
for f in files_loaded:
    print(f"  - {f}")

print(f"[SUMMARY] Errors encountered: {len(errors)}")
for fname, msg in errors:
    print(f"  - {fname}: {msg}")

# re-index the DataFrame to avoid having duplicates in the index
df.index = pd.RangeIndex(len(df.index))

# convert the date variable to DateTime
try:
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    print("[INFO] 'date' column successfully converted to datetime.")
except Exception as e:
    print(f"[ERROR] Failed to convert 'date' column to datetime: {e}")

# finally we plot the time series for a specific exchange: BTC vs EUR
sns.set_theme(rc={'figure.figsize':(13, 7)})
plot = sns.lineplot(x='date', y='current_price', data=df[df['index']=='eur'])
plot.set(title='Bitcoin Price Chart (BTC/EUR)', 
         xlabel='', 
         ylabel='Price in Euro')
# ...and save it locally to a .png file
plot.get_figure().savefig("btceur_line_plot.png") 

# remove all csv files from the 'btc' directory
for file in os.listdir(DATA_FOLDER): 
    file_path = os.path.join(DATA_FOLDER, file)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"[INFO] Removed file: {file_path}")

# remove the (now empty) directory
os.rmdir(DATA_FOLDER)
print(f"[INFO] Removed directory: {DATA_FOLDER}")
