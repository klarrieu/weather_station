import sqlite3


db_path = '/home/pi/Documents/weather_station/weather.db'

bme280_pars = ("AIR_TEMP", "AIR_PRESSURE", "HUMIDITY")
sds011_pars = ("AQI", "PM2_5", "PM10")

def setup_db():
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	check_table = '''SELECT name from sqlite_master WHERE type='table' AND name='weather';'''
	c.execute(check_table)
	if c.fetchone() is None:
		# table does not exist, need to create it
		print('Weather data table does not exist yet, creating...')
		create_table = f'''CREATE TABLE weather(
				   ID INTEGER NOT NULL PRIMARY KEY,
				   TS TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
				   AIR_TEMP DECIMAL(6,2),
				   AIR_PRESSURE DECIMAL(6,2),
			  	   HUMIDITY DECIMAL(6,2),
				   AQI DECIMAL(6,2),
				   PM2_5 DECIMAL(6,2),
				   PM10 DECIMAL(6,2)
				   );'''
		c.execute(create_table)
		conn.commit()
		conn.close()
	else:
		print('Found weather data table.')


def add_entry(bme280_vals=None, sds011_vals=None):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	# tuple of column names for parameters we have
	pars = ((bme280_pars if bme280_vals else ()) +
	       (sds011_pars if sds011_vals else ()))
	# tuple of corresponding values for this entry
	values = ((bme280_vals if bme280_vals else ()) +
		 (sds011_vals if sds011_vals else ()))
	insert_call = f'''INSERT INTO weather {pars}
			  VALUES {values};'''
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
