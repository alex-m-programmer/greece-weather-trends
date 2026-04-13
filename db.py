from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from config import DB_URL
from logger import get_logger
import pandas as pd

engine = create_engine(DB_URL)
logger = get_logger(__name__)

def save_to_db(df, table_name="weather_data"):
  if df.empty:
    return False

  city = df['city'].iloc[0]
    
  try:
    with engine.begin() as conn:
      df.to_sql(
        table_name,
        con=conn,
        if_exists="append",
        index=False,
        method="multi"
      )
      logger.info(f"Successfully saved {city} to database.")
      return True

  except Exception as e:
    error_str = str(e).lower()
    if "unique" in error_str or "duplicate" in error_str or "pkey" in error_str:
      logger.info(f"Skipped {city}: Data for this date already exists.")
      return False 
        
    logger.error(f"Database Error for {city}: {e}")
    return False
  
def get_data_from_db():
  query = "SELECT * FROM weather_data"

  try:
    df = pd.read_sql(query, engine)

    if df is None or df.empty:
      logger.warning("No data found in database.")
      return

    df["datetime"] = pd.to_datetime(df["datetime"])
    logger.info(f"Successfully loaded {len(df)} rows from the database.")
    return df
  except Exception as e:
    logger.error(f"Error reading from database: {e}")
    return None