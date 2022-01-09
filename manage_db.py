import sqlite3


db_path = '/home/pi/Documents/weather_station/weather.db'

def setup_db():
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	check_table = '''SELECT name from sqlite_master WHERE type='table' AND name='weather';'''
	c.execute(check_table)
	if c.fetchone() is None:
		# table does not exist, need to create it
		print('Weather data table does not exist yet, creating...')
		create_table = '''CREATE TABLE weather(
				  ID INTEGER NOT NULL PRIMARY KEY,
				  TS TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')),
				  AIR_TEMP DECIMAL(6,2) NOT NULL,
				  AIR_PRESSURE DECIMAL(6,2) NOT NULL,
				  HUMIDITY DECIMAL(6,2) NOT NULL,
				  AQI DECIMAL(6,2) NOT NULL,
				  PM2_5 DECIMAL(6,2) NOT NULL,
				  PM10 DECIMAL(6,2) NOT NULL
				  );'''
		c.execute(create_table)
		conn.commit()
		conn.close()
	else:
		print('Found weather data table.')


def add_entry(air_temp, air_pressure, humidity, aqi, pm2_5, pm10):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	insert_call = f'''INSERT INTO weather
			  (AIR_TEMP, AIR_PRESSURE, HUMIDITY, AQI, PM2_5, PM10)
			  VALUES ({air_temp}, {air_pressure}, {humidity}, {aqi}, {pm2_5}, {pm10});'''
	c.execute(insert_call)
	conn.commit()
	conn.close()
	print(f'Added entry: \nT:{air_temp} C, p: {air_pressure} hPa, RH: {humidity}%, AQI: {aqi}, PM2.5: {pm2_5} ug/m3, PM10: {pm10} ug/m3')



if __name__ == "__main__":
	setup_db()
	#from random import randint
	#for i in range(100):
	#	add_entry(4.2 + randint(-5, 5), 1000 + randint(-100, 100), 56, 23.04, 0.1)
