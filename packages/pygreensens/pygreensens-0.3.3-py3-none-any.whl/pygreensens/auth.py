import requests
import urllib3
urllib3.disable_warnings()
import json
from datetime import date


class Auth:
	"""Class to make authenticated requests."""

	def __init__(self, username: str, password: str):
		"""Initialize the auth."""
		self.host = "https://api.greensens.de/api"
		self._user = username
		self._pass = password
		self._at = None
		self._atd = None
		self.s = requests.Session()
		self.authenticate()
		self.access_token = f"Bearer {self._at}"
		self._headers = {"Content-Type": "application/json"}

	def _get_sensordata(self) -> requests.Response:
		"""Make a request."""
		self.update_access_token()
		headers = self._headers
		headers["authorization"] = self.access_token
		data = self.s.get(f"{self.host}/plants", headers=headers, verify=False)
		hubs = data.json()['data']['registeredHubs']
		sensors = {}
		for hub in hubs:
			for sensor in hub["plants"]:
				sensors[sensor["id"]] = sensor
		return sensors

	def update_access_token(self):
		if self.access_token == None:
			self.authenticate()
		tokenage = date.today() - self._atd
		tokendays = tokenage.days
		if tokendays > 5:
			self.authenticate()
	
	def authenticate(self):
		payload = {"login": self._user, "password": self._pass}
		url = f"{self.host}/users/authenticate"
		j_payload = json.dumps(payload)
		r = self.s.post(url, headers={"Content-Type": "application/json"}, data=j_payload)
		token = r.json()["data"]["token"]
		auth_date = date.today()
		self._at = token
		self._atd = auth_date


