import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

try:
    DB_URL = st.secrets["DB_URL"]
except (KeyError, FileNotFoundError):
    DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("CRITICAL ERROR: DATABASE_URL not found in environment variables!")
try:
    API_KEY = st.secrets["WEATHER_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("CRITICAL ERROR: WEATHER_API_KEY not found in environment variables!")

CITY_LIST = [
    "Athens,GR",
    "Thessaloniki,GR",
    "Heraklion,GR",
    "Rhodes,GR",
    "Lamia,GR"
]

DB_TABLES = [
    "Dim_Condition",
    "Dim_Date",
    "Dim_Location",
    "Fact_Weather_Daily"
]
