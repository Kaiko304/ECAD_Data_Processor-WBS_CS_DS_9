#!/usr/bin/env python
# coding: utf-8
# KKo2024
# ---------------------------------------------------------------------------------------------------#
# Please download: zip-files and station-files from https://www.ecad.eu/dailydata/predefinedseries.php
# for the features you want to process (e.g. tx, tn, rr...)
# and store them in path /data/ECAD/ecad_downloads/
# ---------------------------------------------------------------------------------------------------#
# Please INPUT the following:

# which features do you want to process? (Use ecad abbrevations)
features = ["tn", "tx", "hu"]
capital_features = ["TN", "TX", "HU"]

# For which countries do you want the data extracted? (use ISO 3166 alpha-2)
sel_countries = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']

# Start date of time periode for weather data?
periode_start = "2022-01-01"

# ---------------------------------------------------------------------------------------------------#
# OUTPUTS:
# station files will be saved as csv at data/ECAD/
# data files will be saved as csv at data/ECAD/
# (station data contains longitude and latitude for geospatial use)
# ---------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------#

def clean_stations(st):
    st['country'] = st['country'].str.strip()
    return(st)

def convert_coordinates(st):
    df = st
    df['latitude'] = df['latitude_DMS'].apply(dms_to_decimal)
    df['longitude'] = df['longitude_DMS'].apply(dms_to_decimal)
    df = df[['station_id', 'station_name', 'country', 'height_m', 'latitude', 'longitude']]
    st = df
    return(st)

def dms_to_decimal(dms_str):
    import pandas as pd
    degrees, minutes, seconds = map(float, dms_str[1:].split(':'))
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    return decimal_degrees if dms_str[0] in ('+', 'N', 'E') else -decimal_degrees

def set_stations(f):
    st = pd.read_csv(f"data/ECAD/ecad_downloads/eca_stations_{f}.txt", sep=",", skiprows=19, header=None, names=["station_id", "station_name", "country", "latitude_DMS", "longitude_DMS", "height_m"])
    st = clean_stations(st)
    st = st.loc[st["country"].isin(sel_countries)]
    st = convert_coordinates(st)
    st.to_csv(f"data/ECAD/eu_stations_{f}.csv")
    station_ids = st["station_id"]
    return station_ids

def load_data(f, fn, station_ids):
    import zipfile
    import os
    
    dfs = []
    path = f"data/ECAD/ecad_downloads/ECA_blend_{f}.zip"
    with zipfile.ZipFile(path, 'r') as z:
        for i in z.namelist():
            if "STAID" in i:
                st_no = int(i[8:14].lstrip("0"))
                if st_no in station_ids:
                    with z.open(i) as file:
                        df = pd.read_csv(file, skiprows=22, header=None)
                        df.columns = ['station_id', 'source_id', 'date', f'{f}', 'quality']
                        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    return df

def clean_data(df):
    df["date"] = pd.to_datetime(df['date'], format='%Y%m%d') 
    df = df.loc[df["date"]>=periode_start]
    return df

# --- HELM BOX ---
import pandas as pd
dfs = {}
features = features
filenames = capital_features
for f, fn in zip(features, filenames): 
    station_ids = set_stations(f)
    df = load_data(f, fn, station_ids)
    df = clean_data(df)
    dfs[f"{f}_df"] = df
    df.to_csv(f"data/ECAD/{f}_df.csv", index=False)

