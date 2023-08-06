from .auth import Auth
from .const import *


class Sensor:
	def __init__(self, id, raw_data: dict, auth: Auth):
		self.raw_data = raw_data
		self.auth = auth
		self._id = id

	@property
	def id(self) -> int:
		"""Return the ID of the sensor."""
		return self.raw_data["id"]

	@property
	def status(self) -> str:
		"""Return the status of the sensor."""
		return str(self.raw_data["status"])

	@property
	def name(self) -> str:
		"""Return the name of the sensor."""
		return str(self.raw_data["sensorID"])

	@property
	def moisture(self) -> float:
		"""Return the value of the sensor."""
		return self.raw_data["moisture"]

	@property
	def temperature(self) -> float:
		"""Return the value of the sensor."""
		return self.raw_data["temperature"]

	@property
	def illumination(self) -> float:
		"""Return the value of the sensor."""
		return self.raw_data["illumination"]
	
	@property
	def plantnameLA(self) -> str:
		"""Return the value of the sensor."""
		return str(self.raw_data["plantNameLA"])	

	@property
	def plantnameEN(self) -> str:
		"""Return the value of the sensor."""
		return str(self.raw_data["plantNameEN"])

	@property
	def plantnameDE(self) -> str:
		"""Return the value of the sensor."""
		return str(self.raw_data["plantNameDE"])

	@property
	def lastConnection(self):
		"""Return the value of the sensor."""
		return self.raw_data["lastConnection"]

	@property
	def chargeLevel(self):
		"""Return the value of the sensor."""
		return self.raw_data["chargeLevel"]


	def update(self):
		"""Update the sensor data."""
		data = self.auth._get_sensordata()
		self.raw_data[self.id] = data
