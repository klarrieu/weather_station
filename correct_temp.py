import subprocess
import time


# get current temp of cpu
def get_cpu_temp():
  cpu_temp = subprocess.check_output('vcgencmd measure_temp', shell=True).decode('UTF-8')
  cpu_temp = cpu_temp.replace('temp=', '').replace("\'C\n", '')
  cpu_temp = float(cpu_temp)
  return(cpu_temp)


# correct bme280 air temperature reading, adjusting for temp of the pi
def correct_temp(sensor_temp):
  cpu_temp = get_cpu_temp()
  print(cpu_temp)
  delta = 0
  if cpu_temp > sensor_temp:
    # correction proportional to difference between cpu_temp and sensor reading
    # could do more multi-point calibration to refine this
    delta = (cpu_temp - sensor_temp) / 7
  t = sensor_temp - delta
  t = round(t, 2)
  return t


if __name__=="__main__":
  print(correct_temp(3.7))
