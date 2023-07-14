import serial
import smbus2
import time
from aqi import get_aqi


ser = serial.Serial('/dev/ttyUSB0', 9600)


def get_sds011_data():
  data = None
  while not data:
    data = ser.read(10)
    pm2_5 = (data[2] + data[3] * 256) / 10
    pm10 = (data[4] + data[5] * 256) / 10
    aqi = get_aqi(pm2_5, pm10)
  return aqi, pm2_5, pm10


if __name__ == "__main__":
  while True:
    data = ser.read(10)
    if data:
      print(data)
      print([val for val in data])
      pm2_5 = (data[2] + data[3] * 256) / 10
      pm10 = (data[4] + data[5] * 256) / 10
      aqi = get_aqi(pm2_5, pm10)
      print(f'PM2.5: {pm2_5} ug/m3')
      print(f'PM10: {pm10} ug/m3')
      print(f'AQI: {aqi}')
