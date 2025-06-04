# map.py

import pandas as pd
import plotly.express as px
import requests

def fetch_crime_data():
    base_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    years = range(2014, 2026)
    all_data = []

    for year in years:
        year_data = []
        for offset in range(0, 10000, 3000):
            params = {
                "$limit": 3000,
                "$offset": offset,
                "$where": f"latitude IS NOT NULL AND longitude IS NOT NULL "
                          f"AND date >= '{year}-01-01T00:00:00' AND date < '{year+1}-01-01T00:00:00'"
            }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            df_year = pd.DataFrame(response.json())
            df_year["year"] = year
            all_data.append(df_year)

    df = pd.concat(all_data, ignore_index=True)
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['primary_type'] = df['primary_type'].astype(str).str.upper()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude', 'primary_type'])
    return df


def create_filtered_map(df, selected_crime, selected_year):
    filtered_df = df.copy()

    if selected_crime != "All Crime Types":
        filtered_df = filtered_df[filtered_df['primary_type'] == selected_crime]

    if selected_year != "All Years":
        filtered_df = filtered_df[filtered_df['year'] == selected_year]

    return filtered_df
