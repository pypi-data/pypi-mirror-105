"""pygreensens"""
__version__ = "0.3.3"

if __name__ != '__main__':
	from .auth import Auth
	from .api import GreensensApi
else:
	from auth import Auth
	from api import GreensensApi

	test_user = ""
	test_pass = ""
	def main():
		auth = Auth(test_user, test_pass)
		api = GreensensApi(auth)

		sensors = api.sensors
		data = api.data

		for sensor in sensors:
			print(data[sensor], "\n")
		
	
	main()

