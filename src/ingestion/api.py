# api.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from io import StringIO
import pandas as pd
from config import API_KEY

def _build_session():
  session = requests.Session()
  retry_strategy = Retry(
    total=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
  )
  adapter = HTTPAdapter(max_retries=retry_strategy)
  session.mount("https://", adapter)
  session.mount("http://", adapter)
  return session


def fetch_raw_data(city, start_date, end_date):
  url = (
    f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&include=days&contentType=csv"
  )

  session = _build_session()
  res = session.get(url, timeout=10)
  res.raise_for_status()
  res.encoding = "utf-8"
  return pd.read_csv(StringIO(res.text))