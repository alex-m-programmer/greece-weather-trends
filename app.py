import streamlit as st
import pandas as pd
from db import get_data_from_db
import plotly.express as px

st.set_page_config(page_title="Greece Weather Dashboard", layout="wide")
st.title("🌦️ Greece Weather Analytics")

@st.cache_data(ttl=3600) 
def load_data():
  return get_data_from_db()

df = load_data()

if df.empty:
  st.error("No data found in the Cloud Database.")
else:
  # --- SIDEBAR FILTERS ---
  st.sidebar.header("Dashboard Filters")
  selected_cities = st.sidebar.multiselect("Select Cities", options=df['city'].unique(), default=df['city'].unique())
    
  filtered_df = df[df['city'].isin(selected_cities)].sort_values("datetime")

  # --- TOP ROW: KPI METRICS ---
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Avg Temp", f"{filtered_df['temp'].mean():.1f}°C")
  m2.metric("Max Humidity", f"{filtered_df['humidity'].max():.1f}%")
  m3.metric("Avg Wind Speed", f"{filtered_df['windspeed'].mean():.1f} km/h")
  m4.metric("Total Precip", f"{filtered_df['precip'].sum():.2f} mm")

  st.divider()

  # --- ROW 2: TEMPERATURE & HUMIDITY ---
  col_left, col_right = st.columns(2)

  with col_left:
    st.subheader("Temperature Trends (Max/Min/Avg)")
      # Using Plotly for better interactivity with multiple lines
    fig_temp = px.line(filtered_df, x="datetime", y=["tempmax", "tempmin", "temp"], color="city", title="Daily Temperatures")
    st.plotly_chart(fig_temp, use_container_width=True)

  with col_right:
    st.subheader("Humidity Levels")
    fig_hum = px.area(filtered_df, x="datetime", y="humidity", color="city", title="Humidity Percentage over Time")
    st.plotly_chart(fig_hum, use_container_width=True)

  # --- ROW 3: WIND & PRECIPITATION ---
  col_a, col_b = st.columns(2)

  with col_a:
    st.subheader("Wind Speed Analysis")
    fig_wind = px.bar(filtered_df, x="datetime", y="windspeed", color="city", barmode="group", title="Wind Speed by City")
    st.plotly_chart(fig_wind, use_container_width=True)

  with col_b:
    st.subheader("Precipitation (Rainfall)")
    fig_precip = px.scatter(filtered_df, x="temp", y="precip", size="precip", color="city", title="Precipitation vs Temperature")
    st.plotly_chart(fig_precip, use_container_width=True)

  # --- DATA TABLE ---
  with st.expander("📂 View Complete Dataset"):
    st.dataframe(filtered_df, use_container_width=True)