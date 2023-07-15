# import BME280 stuff
from bme280 import get_bme280_data
# import SDS011 stuff
try:
  from sds011 import get_sds011_data
except:
  print('SDS011 not installed.')
# import SPS30 stuff
try:
  from get_sps30 import get_sps30_data
except:
  print('SPS30 not installed.')
# import database management stuff, etc.
from manage_db import setup_db, add_entry
import time
from numpy import mean
import numpy as np
from read_config import read_config
import logging


logging.basicConfig(filename='sensors.log', encoding='utf-8', level=logging.DEBUG)

installed_devices, device_configs = read_config()
getters = {device: globals()[device_configs[device]["getter"]] for device in installed_devices}

# prepare database for I/O
setup_db()

# initialize array of sensor readings
readings = []

#start clock
t1 = time.time()

while True:
  try:
    # get sensor readings
    row = []
    for device in installed_devices:
      device_reading = getters[device]()
      row.extend(device_reading)
    readings.append(row)
    # get current time
    t2 = time.time()
    # if we've been reading values for 60 seconds
    if t2 - t1 >= 60:
      # reset clock
      t1 = time.time()
      # get mean values from last 60 seconds
      readings = tuple(np.array(readings).mean(axis=0))
      # add mean values to database
      add_entry(readings)
      # reset array
      readings = []
  except Exception as e:
    # log error and try again
    logging.error(e)
