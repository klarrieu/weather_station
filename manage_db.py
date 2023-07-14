import sqlite3
from read_config import read_config


installed_devices, device_configs = read_config()
pars = tuple(par for device in installed_devices for par in device_configs[device]["params"])
par_roundings = [rounding for device in installed_devices for rounding in device_configs[device]["rounding"]]


db_path = './weather.db'

def setup_db():
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	check_table = '''SELECT name from sqlite_master WHERE type='table' AND name='weather';'''
	c.execute(check_table)
	if c.fetchone() is None:
		# table does not exist, need to create it
		print('Weather data table does not exist yet, creating...')
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
	values = tuple(round(val, rounding) for val, rounding in zip(values, par_roundings))
	insert_call = f'''INSERT INTO weather {pars}
			  VALUES {values};'''
	c.execute(insert_call)
	conn.commit()
	conn.close()
	print(f"Added entry: {dict(zip(pars, values))}")


if __name__ == "__main__":
	setup_db()
