# Raspberry Pi weather station + web server

This repo currently works with the following weather sensors over the I2C bus, though it can easily be modified to accommodate more:

- BME280
- SDS011
- SPS30

There are three main parts:

- `config.json`: JSON text file that tells the scripts information regarding the sensor configuration.
- `read_sensors.py`: streams data from weather sensors to a local database on the Raspberry Pi.
- `server.js`: launches a node.js web server with a live dashboard and plots of weather sensor data.

## Requirements

- Node.js
- Python >=3.6
- Sqlite3

## Quick Start

1. Clone this repository.

2. Make any necessary modifications to the `config.json` file for the installed sensors.

2. Run `start_station.sh`.
   Note: to access the webserver outside the local network, you will need to setup port forwarding.

Once you are happy that everything works, the database/server can be set to launch automatically on startup as background processes by adding `start_station.sh` to `/etc/rc.local` and rebooting (or restarting rc-local.service).
