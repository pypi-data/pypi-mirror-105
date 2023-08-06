from typing import List

from .auth import Auth
from .sensor import Sensor
from .const import *


class GreensensApi:
	def __init__(self, auth: Auth):
		self.auth = auth

	def get_sensors(self) -> List[Sensor]:
		"""Return the lights."""
		data = self.auth._get_sensordata()
		return [Sensor(sensor, data, self.auth) for sensor, data in data.items()]
