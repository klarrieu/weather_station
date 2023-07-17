#!/bin/bash
sleep 8
cd /home/pi/weather_station
forever start -c node server.js -l forever.log -o server.log -e server_err.log
python read_sensors.py
