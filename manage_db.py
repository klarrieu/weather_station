import sqlite3
from read_config import read_config


installed_devices, device_configs = read_config()
pars = tuple(par for device in installed_devices for par in device_configs[device]["params"])


db_path = '/home/pi/Documents/weather_station/weather.db'

bme280_pars = ("AIR_TEMP", "AIR_PRESSURE", "HUMIDITY")
sds011_pars = ("AQI", "PM2_5", "PM10")
sps30_pars =  ("AQI", "PM1", "PM2_5", "PM4", "PM10", "MEAN_SIZE")

def setup_db():
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	check_table = '''SELECT name from sqlite_master WHERE type='table' AND name='weather';'''
	c.execute(check_table)
	if c.fetchone() is None:
		# table does not exist, need to create it
		print('Weather data table does not exist yet, creating...')
		par_roundings = [rounding for device in installed_devices for rounding in device_configs[device]["rounding"]]
		table_pars = [f"{par} DECIMAL(6, {rounding})" for par, rounding in zip(pars, par_roundings)]
		create_table = f'''CREATE TABLE weather(
				   ID INTEGER NOT NULL PRIMARY KEY,
				   TS TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
				   {", ".join(table_pars)}
				   );'''
		print(create_table)
		c.execute(create_table)
		conn.commit()
		conn.close()
	else:
		print('Found weather data table.')


def add_entry(values):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	insert_call = f'''INSERT INTO weather {pars}
			  VALUES {values};'''
	print(insert_call)
	c.execute(insert_call)
	conn.commit()
	conn.close()
	#print(f'Added entry: \nT:{air_temp} C, p: {air_pressure} hPa, RH: {humidity}%, AQI: {aqi}, PM2.5: {pm2_5} ug/m3, PM10: {pm10} ug/m3')
	print(f"Added entry: {dict(zip(pars, values))}")


if __name__ == "__main__":
	setup_db()
	#from random import randint
	#for i in range(100):
	#	add_entry(4.2 + randint(-5, 5), 1000 + randint(-100, 100), 56, 23.04, 0.1)
