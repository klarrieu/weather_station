# Raspberry Pi weather station + web server

This repo currently works with the following weather sensors:

- BME280
- SDS011
- SPS30


There are two main parts:

- `read_sensors.py`: streams data from weather sensors to a local database on the Raspberry Pi.

- `server.js`: launches a node.js web server with a live dashboard and plots of weather sensor data.


## Requirements

- node.js
- Python 3.6+
- sqlite


## Quick Start

1. Clone this repository.

2. `python read_sensors.py` will start streaming data from the sensors to a local database `weather.db`.

3. `node server.js` will launch the web server from the Raspberry Pi's IP address. 

   Note: to access the webserver outside the local network, you will need to setup port forwarding via your ISP.

Once you are happy that everything works, the database/server can be set to launch automatically on startup as background processes:

1. Add `start_station.sh` to `/etc/rc.local`.

2. `sudo reboot` to reboot the pi.
