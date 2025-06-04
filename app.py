# app.py

import streamlit as st
import plotly.express as px
from map import fetch_crime_data, create_filtered_map

st.set_page_config(page_title="Chicago Crime Heatmap", layout="wide")
st.title("📍 Chicago Crime Heatmap (2014–2025)")

# Fetch and cache the data
@st.cache_data(show_spinner=True)
def load_data():
    return fetch_crime_data()

df = load_data()

# Sidebar filters
crime_types = sorted(df['primary_type'].unique())
years = sorted(df['year'].unique())

crime_types.insert(0, "All Crime Types")
years.insert(0, "All Years")

selected_crime = st.sidebar.selectbox("Select Crime Type", crime_types)
selected_year = st.sidebar.selectbox("Select Year", years)

# Apply filtering
filtered_df = create_filtered_map(df, selected_crime, selected_year)

# Display heading and map
title_crime = selected_crime if selected_crime != "All Crime Types" else "All Crimes"
title_year = selected_year if selected_year != "All Years" else "All Years"
st.subheader(f"{title_crime} in {title_year}")
st.caption(f"Showing {len(filtered_df):,} crime records.")

if filtered_df.empty:
    st.warning("No data available for this selection.")
else:
    fig = px.density_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        radius=10,
        center={"lat": 41.8781, "lon": -87.6298},
        zoom=10,
        mapbox_style="carto-positron",
        height=700
    )
    st.plotly_chart(fig, use_container_width=True)
