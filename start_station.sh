#!/bin/bash
sleep 8
cd ~/weather_station
forever start -c node server.js
python read_sensors.py
