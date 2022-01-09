import serial
import smbus2
import time


# AQI equation: https://forum.airnowtech.org/t/the-aqi-equation/169
def aqi_pm(c, size):
  # c: concentration (ug/m3), size: '2.5' or '10'
  # concentration breakpoints
  if size == '2.5':
    c_bps = [0, 12.0, 35.4, 55.4, 150.4, 250.4, 500.4]
  elif size == '10':
    c_bps = [0, 54, 154, 254, 354, 424, 604]
  else:
    print('error: size must be 2.5 or 10.')
  # AQI breakpoints
  aqi_bps = [0, 50, 100, 150, 200, 300, 500]
  # determine which breakpoints we are between
  if c == 0:
    return 0
  for i in range(len(c_bps) - 1):
    c_lo, c_hi = c_bps[i: i+2]
    aqi_lo, aqi_hi = aqi_bps[i: i+2]
    if c_lo < c <= c_hi:
      # compute AQI (linear interpolation)
      aqi = aqi_lo + (c - c_lo) * (aqi_hi - aqi_lo) / (c_hi - c_lo)
      return int(aqi)
  # if haven't returned yet, we are > 500 AQI, compute same way
  aqi = aqi_lo + (pm2_5 - c_lo) * (aqi_hi - aqi_lo) / (c_hi - c_lo)
  # round AQI to integer
  return round(aqi, 0)


def get_aqi(pm2_5, pm10):
  return max(aqi_pm(pm2_5, '2.5'), aqi_pm(pm10, '10'))


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
