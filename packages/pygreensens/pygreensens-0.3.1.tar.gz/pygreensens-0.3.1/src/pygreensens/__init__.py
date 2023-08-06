"""pygreensens"""
__version__ = "0.3.1"

if __name__ != '__main__':
    from .pygreensens import GreenSens
    from .const import *
else:
    from pygreensens import GreenSens
    from const import *
    test_user = ""
    test_pass = ""
    test_cond = ["sensorID", "temperature"]
    test = GreenSens(test_user, test_pass, test_cond)

