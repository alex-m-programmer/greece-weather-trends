import requests
import datetime
from io import StringIO
import pandas as pd
from config import API_KEY
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_raw_data(city, start_date=None, end_date=None):
  if start_date is None:
    start_date = datetime.date.today()
  if end_date is None:
    end_date = datetime.date.today()
  url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&key={API_KEY}&include=days&contentType=csv"
    
  res = requests.get(url, timeout=10)
  res.raise_for_status()
  res.encoding = "utf-8"
  return pd.read_csv(StringIO(res.text))
