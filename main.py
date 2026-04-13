import time
from config import CITY_LIST
from logger import get_logger
from api import fetch_raw_data
from transform import clean_weather_data
from db import save_to_db

def run_pipeline():
  logger = get_logger(__name__)
  
  for city in CITY_LIST:
    try:
      logger.info(f"Starting Process for {city}")

      raw_df = fetch_raw_data(city)
      clean_df = clean_weather_data(raw_df, city)
      save_to_db(clean_df)

      time.sleep(1)

    except Exception as e:
      logger.error(f"Failed to process {city}: {e}")
  
  logger.info("ETL Cycle Complete. Database is updated.")

if __name__ == "__main__":
  run_pipeline()