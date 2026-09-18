import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import DB_URL

logger = logging.getLogger(__name__)
engine = create_engine(DB_URL)


def get_or_create_location(conn, city):

  result = conn.execute(text("""SELECT location_key FROM Dim_Location WHERE city = :city"""), {"city": city}).fetchone()

  if result:
    return result[0]

  conn.execute(text("""INSERT INTO Dim_Location (city) VALUES (:city)"""), {"city": city})

  result = conn.execute(text("""SELECT location_key FROM Dim_Location WHERE city = :city"""), {"city": city}).fetchone()

  return result[0]


def get_or_create_condition(conn, condition):

  result = conn.execute(text("""SELECT condition_key FROM Dim_Condition WHERE conditions = :condition"""), {"condition": condition}).fetchone()

  if result:
    return result[0]

  conn.execute(text("""INSERT INTO Dim_Condition (conditions) VALUES (:condition)"""), {"condition": condition})

  result = conn.execute(text("""SELECT condition_key FROM Dim_Condition WHERE conditions = :condition"""), {"condition": condition}).fetchone()

  return result[0]


def get_or_create_date(conn, date_value):

  date_value = pd.to_datetime(date_value).date()

  date_key = int(date_value.strftime("%Y%m%d"))

  result = conn.execute(text("""SELECT date_key FROM Dim_Date WHERE date_key = :date_key"""), {"date_key": date_key}).fetchone()

  if result:
    return result[0]

  conn.execute(
    text("""
      INSERT INTO Dim_Date (
        date_key,
        full_date,
        [year],
        [month],
        [day],
        day_of_week,
        [quarter]
      )
      VALUES (
        :date_key,
        :full_date,
        :year,
        :month,
        :day,
        :day_of_week,
        :quarter
      )
    """),
    {
      "date_key": date_key,
      "full_date": date_value,
      "year": date_value.year,
      "month": date_value.month,
      "day": date_value.day,
      "day_of_week": date_value.strftime("%A"),
      "quarter": ((date_value.month - 1) // 3) + 1
    }
  )

  return date_key


def insert_weather_fact(conn, row, date_key, location_key, condition_key):

  existing = conn.execute(text("""SELECT weather_fact_id FROM Fact_Weather_Daily WHERE date_key = :date_key AND location_key = :location_key"""), {"date_key": date_key, "location_key": location_key}).fetchone()

  if existing:
    return False

  conn.execute(
    text("""
      INSERT INTO Fact_Weather_Daily (
      date_key,
      location_key,
      condition_key,
      tempmax,
      tempmin,
      temp,
      feelslike,
      humidity,
      precip,
      precipprob,
      windspeed,
      windgust,
      cloudcover,
      sunrise,
      sunset
    )
    VALUES (
      :date_key,
      :location_key,
      :condition_key,
      :tempmax,
      :tempmin,
      :temp,
      :feelslike,
      :humidity,
      :precip,
      :precipprob,
      :windspeed,
      :windgust,
      :cloudcover,
      :sunrise,
      :sunset
    )
  """),
    {
      "date_key": date_key,
      "location_key": location_key,
      "condition_key": condition_key,
      "tempmax": row.get("tempmax"),
      "tempmin": row.get("tempmin"),
      "temp": row.get("temp"),
      "feelslike": row.get("feelslike"),
      "humidity": row.get("humidity"),
      "precip": row.get("precip"),
      "precipprob": row.get("precipprob"),
      "windspeed": row.get("windspeed"),
      "windgust": row.get("windgust"),
      "cloudcover": row.get("cloudcover"),
      "sunrise": row.get("sunrise"),
      "sunset": row.get("sunset")
    }
  )

  return True


def save_to_db(df):

  if df.empty:
    logger.warning("No data to save.")
    return False

  city = df["city"].iloc[0]

  try:
    with engine.begin() as conn:

      location_key = get_or_create_location(conn, city)

      inserted_count = 0
      skipped_count = 0

      for _, row in df.iterrows():
        date_key = get_or_create_date(conn, row["datetime"])
        condition_key = get_or_create_condition(conn, row.get("conditions"))
        inserted = insert_weather_fact(conn, row, date_key, location_key, condition_key)

        if inserted:
          inserted_count += 1
        else:
          skipped_count += 1

      logger.info(f"{city}: Successfully processed {inserted_count} new rows, {skipped_count} existing rows.")

      return True

  except SQLAlchemyError as e:
    logger.error(f"Database error for {city}: {e}")
    raise

  except Exception as e:
    logger.exception(f"Unexpected error while saving {city}: {e}")
    raise


def load_weather_data():
  query = text("""
    SELECT
      l.city,
      d.full_date,
      c.conditions,
      f.tempmax,
      f.tempmin,
      f.temp,
      f.feelslike,
      f.humidity,
      f.precip,
      f.windspeed,
      f.windgust,
      f.cloudcover
    FROM Fact_Weather_Daily f
    JOIN Dim_Location l ON f.location_key = l.location_key
    JOIN Dim_Date d ON f.date_key = d.date_key
    JOIN Dim_Condition c ON f.condition_key = c.condition_key
    ORDER BY d.full_date
  """)
  with engine.connect() as conn:
    return pd.read_sql(query, conn)