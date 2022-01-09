from bme280 import get_bme280_data
from sds011 import get_sds011_data
from manage_db import setup_db, add_entry
import time
from numpy import mean

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
  # get a sensor reading
  air_temp, air_pressure, humidity = get_bme280_data()
  aqi, pm2_5, pm10 = get_sds011_data()
  # add values to arrays
  air_temps.append(air_temp)
  air_pressures.append(air_pressure)
  humidities.append(humidity)
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
    air_temp = round(mean(air_temps), 2)
    air_pressure = round(mean(air_pressures), 2)
    humidity = round(mean(humidities), 2)
    aqi = round(mean(aqis), 0)
    pm2_5 = round(mean(pm2_5s), 2)
    pm10 = round(mean(pm10s), 2)
    # add mean values to database
    add_entry(air_temp, air_pressure, humidity, aqi, pm2_5, pm10)
    # reset arrays
    air_temps = []
    air_pressures = []
    humidities = []
    aqis = []
    pm2_5s = []
    pm10s = []
