import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

if not DB_URL:
    raise ValueError("CRITICAL ERROR: DATABASE_URL not found in environment variables!")

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