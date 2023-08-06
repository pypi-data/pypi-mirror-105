"""pygreensens"""
__version__ = "0.3.2"

if __name__ != '__main__':
	from .auth import Auth
	from .api import GreensensApi
	from .const import *
else:
	from auth import Auth
	from api import GreensensApi
	from const import *

	test_user = ""
	test_pass = ""
	def main():
		auth = Auth(BASE_URL, test_user, test_pass)
		api = GreensensApi(auth)

		sensors = api.get_sensors()

		for sensor in sensors:
			sensor.update()
			print(sensor.id)
	
	main()

