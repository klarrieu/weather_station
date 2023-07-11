from bme280 import get_bme280_data
bme280_installed = True
try:
  from sds011 import get_sds011_data
except:
  print('SDS011 not installed.')
  sds011_installed = False
from correct_temp import correct_temp
from manage_db import setup_db, add_entry
import time
from numpy import mean
import numpy as np

setup_db()

# initialize arrays
air_temps = []
air_pressures = []
humidities = []
aqis = []
pm2_5s = []
pm10s = []

#start clock
t1 = time.time()

while True:
  # get sensor readings
  if bme280_installed:
    air_temp, air_pressure, humidity = get_bme280_data()
  if sds011_installed:
    aqi, pm2_5, pm10 = get_sds011_data()
  if bme280_installed:
    # correct air temp accounting for heat from pi CPU
    air_temp = correct_temp(air_temp)
    # add values to arrays
    air_temps.append(air_temp)
    air_pressures.append(air_pressure)
    humidities.append(humidity)
  if sds011_installed:
    aqis.append(aqi)
    pm2_5s.append(pm2_5)
    pm10s.append(pm10)
  # get current time
  t2 = time.time()
  # if we've been reading values for 60 seconds
  if t2 - t1 >= 60:
    # reset clock
    t1 = time.time()
    # get mean values from last 60 seconds
    if bme280_installed:
      air_temp = round(mean(air_temps), 2)
      air_pressure = round(mean(air_pressures), 2)
      humidity = round(mean(humidities), 2)
      bme280_vals = (air_temp, air_pressure, humidity)
    else:
      bme280_vals = None
    if sds011_installed:
      aqi = round(mean(aqis), 0)
      pm2_5 = round(mean(pm2_5s), 2)
      pm10 = round(mean(pm10s), 2)
      sds011_vals = (aqi, pm2_5, pm10)
    else:
      sds011_vals = None
    # add mean values to database
    add_entry(bme280_vals=bme280_vals,
	      sds011_vals=sds011_vals)
    # reset arrays
    air_temps = []
    air_pressures = []
    humidities = []
    aqis = []
    pm2_5s = []
    pm10s = []
