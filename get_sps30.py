import sys
sys.path.append('./sps30/')
import json
from time import sleep
from sps30 import SPS30
from aqi import get_aqi


pm_sensor = SPS30()
pm_sensor.start_measurement()

def get_sps30_data():
    while True:
        measurement = pm_sensor.get_measurement()
        if len(measurement):
            break
    reading = measurement["sensor_data"]
    mass_density = reading["mass_density"]
    pm1 = mass_density["pm1.0"]
    pm2_5 = mass_density["pm2.5"]
    pm4 = mass_density["pm4.0"]
    pm10 = mass_density["pm10"]
    aqi = get_aqi(pm2_5, pm10)
    mean_size = reading["particle_size"]
    return aqi, pm1, pm2_5, pm4, pm10, mean_size


if __name__ == "__main__":
    print(f"Firmware version: {pm_sensor.firmware_version()}")
    print(f"Product type: {pm_sensor.product_type()}")
    print(f"Serial number: {pm_sensor.serial_number()}")
    print(f"Status register: {pm_sensor.read_status_register()}")
    print(f"Auto cleaning interval: {pm_sensor.read_auto_cleaning_interval()}s")
    #pm_sensor.start_measurement()

    while True:
        try:
            #print(json.dumps(pm_sensor.get_measurement(), indent=2))
            #sleep(2)
            print(get_sps30_data())
        except KeyboardInterrupt:
            print("Stopping measurement...")
            pm_sensor.stop_measurement()
            sys.exit()
