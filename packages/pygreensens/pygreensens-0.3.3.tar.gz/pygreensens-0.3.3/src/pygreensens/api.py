from typing import List

# from .auth import Auth
from auth import Auth

class GreensensApi:
	def __init__(self, auth: Auth):
		self.auth = auth
		self.data = None
		self.sensors = self.get_sensors()

	def get_sensor_data(self):
		"""Return sensor data"""
		self.update()
		return self.data
	
	def get_sensors(self):
		"""Return sensor list"""
		self.update()
		list = []
		for key, value in self.data.items():
			list.append(key)
		return list
	
	def update(self):
		"""Update sensor data"""
		self.data = self.auth._get_sensordata()
