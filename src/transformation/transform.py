import pandas as pd
import logging

logger = logging.getLogger(__name__)

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

  critical_cols = [
    "datetime", "tempmax", "tempmin", "temp",
    "humidity", "precip", "windspeed", "windgust"
  ]

  df = df.dropna(subset=critical_cols)
  df["city"] = city

  numeric_cols = [
    "tempmax", "tempmin", "temp", "feelslike",
    "humidity", "precip", "precipprob",
    "windspeed", "windgust", "cloudcover"
  ]

  df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

  df = df[
    (df["temp"].between(-50, 60)) &
    (df["tempmin"].between(-50, 60)) &
    (df["tempmax"].between(-50, 60)) &
    (df["tempmin"] <= df["temp"]) &
    (df["temp"] <= df["tempmax"]) &
    (df["humidity"].between(0, 100)) &
    (df["precip"].between(0, 1000)) &
    (df["windspeed"] >= 0)
  ]

  df["precipprob"] = df["precipprob"].mask(~df["precipprob"].between(0, 100))
  df["cloudcover"] = df["cloudcover"].mask(~df["cloudcover"].between(0, 100))
  df["conditions"] = df["conditions"].fillna("Unknown")
  df["sunrise"] = pd.to_datetime(df["sunrise"], errors="coerce").dt.time
  df["sunset"] = pd.to_datetime(df["sunset"], errors="coerce").dt.time
  df = df.drop_duplicates(subset=["city", "datetime"])

  gust_anomalies = (df["windgust"] < df["windspeed"]).sum()
  if gust_anomalies > 0:
    logger.warning(f"{city}: {gust_anomalies} rows have windgust < windspeed (kept, flagged as anomaly).")

  logger.info(f"Successfully processed {city}. Final row count: {len(df)}")

  if len(df) < initial_count:
    logger.warning(f"{city}: Dropped {initial_count - len(df)} rows.")

  return df