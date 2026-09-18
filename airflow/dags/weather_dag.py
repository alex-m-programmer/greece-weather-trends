# weather_dag.py
from airflow.sdk import DAG
from airflow.sdk import task
from datetime import datetime, timedelta, date
from src.ingestion.api import fetch_raw_data
from src.transformation.transform import clean_weather_data
from src.database.db import save_to_db
from config import CITY_LIST

default_args = {
  "retries": 3,
  "retry_delay": timedelta(minutes=2),
  "retry_exponential_backoff": True,
  "max_retry_delay": timedelta(minutes=15),
}

with DAG(
  dag_id="weather_pipeline",
  start_date=datetime(2026, 9, 19),
  schedule="0 2 * * *",
  catchup=False,
  default_args=default_args,
) as dag:

  @task(max_active_tis_per_dag=1)
  def process_city(city):
    target_date = (date.today() - timedelta(days=1)).isoformat()
    raw_df = fetch_raw_data(city, start_date=target_date, end_date=target_date)
    clean_df = clean_weather_data(raw_df, city)
    save_to_db(clean_df)

  process_city.expand(city=CITY_LIST)