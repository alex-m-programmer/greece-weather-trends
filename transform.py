import pandas as pd
from logger import get_logger

logger = get_logger(__name__)

def clean_weather_data(raw_df, city):
  initial_count = len(raw_df)
  columns_to_keep = [
    "datetime", "tempmax", "tempmin", "temp",
    "feelslike", "humidity", "precip", "precipprob",
    "windspeed", "windgust", "cloudcover",
    "sunrise", "sunset", "conditions"
  ]

  df = raw_df[[col for col in columns_to_keep if col in raw_df.columns]].copy()
  df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

  critical_cols = ["datetime", "tempmax", "tempmin", "temp", "humidity", "precip", "windspeed", "windgust"]
  df = df.dropna(subset=critical_cols)
 
  df["city"] = city
  numeric_cols = ["tempmax","tempmin","temp","feelslike","humidity","precip","precipprob","windspeed","windgust","cloudcover"]
  df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

  df = df[
    (df["temp"] >= -50) & (df["temp"] <= 60) &
    (df["tempmin"] >= -50) & (df["tempmin"] <= 60) &
    (df["tempmax"] >= -50) & (df["tempmax"] <= 60) &
    (df["tempmin"] <= df["temp"]) & (df["temp"] <= df["tempmax"]) &
    (df["humidity"] >= 0) & (df["humidity"] <= 100) &
    (df["precip"] >= 0) & (df["precip"] <= 1000) &
    (df["windspeed"] >= 0) &
    (df["windgust"] >= df["windspeed"])
  ]

  df["precipprob"] = df["precipprob"].mask(~df["precipprob"].between(0, 100))
  df["cloudcover"] = df["cloudcover"].mask(~df["cloudcover"].between(0, 100))
  df = df.drop_duplicates(subset=["city", "datetime"])

  logger.info(f"Successfully processed {city}. Final row count: {len(df)}")
    
  if len(df) < initial_count:
    logger.warning(f"{city}: Dropped {initial_count - len(df)} rows.")
        
  return df