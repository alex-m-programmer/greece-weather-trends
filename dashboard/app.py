import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.database.db import load_weather_data

st.set_page_config(page_title="Weather Dashboard", layout="wide")


@st.cache_data(ttl=3600)
def load_data():
  return load_weather_data()


df = load_data()

st.title("🌤️ Greek Cities Weather Dashboard")

if df.empty:
  st.warning("No data found yet. Run the Airflow pipeline first.")
  st.stop()

cities = sorted(df["city"].unique())
selected_cities = st.sidebar.multiselect("Cities", cities, default=cities)

min_date, max_date = df["full_date"].min(), df["full_date"].max()
date_range = st.sidebar.date_input(
  "Date range", (min_date, max_date), min_value=min_date, max_value=max_date
)

filtered = df[df["city"].isin(selected_cities)]
if isinstance(date_range, tuple) and len(date_range) == 2:
  start, end = date_range
  filtered = filtered[(filtered["full_date"] >= start) & (filtered["full_date"] <= end)]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Temp (°C)", f"{filtered['temp'].mean():.1f}")
col2.metric("Avg Humidity (%)", f"{filtered['humidity'].mean():.1f}")
col3.metric("Max Wind Gust (km/h)", f"{filtered['windgust'].max():.1f}")
col4.metric("Total Precip (mm)", f"{filtered['precip'].sum():.1f}")

st.subheader("Temperature over time")
st.line_chart(filtered.pivot_table(index="full_date", columns="city", values="temp"))

st.subheader("Humidity over time")
st.line_chart(filtered.pivot_table(index="full_date", columns="city", values="humidity"))

st.subheader("Conditions breakdown")
st.bar_chart(filtered["conditions"].value_counts())

st.subheader("Raw data")
st.dataframe(filtered.sort_values("full_date", ascending=False), use_container_width=True)
