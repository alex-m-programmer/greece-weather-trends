import logging
import os

def get_logger(name):

  logger = logging.getLogger(name)
  logger.setLevel(logging.INFO)

  if logger.hasHandlers():
    return logger

  output_dir = "API_Logs"
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  file_handler = logging.FileHandler(f"{output_dir}/WeatherAPI.log")
  stream_handler = logging.StreamHandler()

  formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(name)s] %(message)s"
  )

  file_handler.setFormatter(formatter)
  stream_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(stream_handler)

  return logger