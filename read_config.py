import json


def read_config():
	f = open("config.json")
	data = json.load(f)
	installed_devices = data["installed_devices"]
	device_configs = data["device_configs"]
	return installed_devices, device_configs
