import serial
from time import sleep
# from setting import tdic1,tdic2
import json
import time
import pigpio
import os
import sys
# sys.path.append('/home/pi/machineT/machine/pca9675')
from pca9675 import PCA9675I2C
from AllConfig import J3,J17,J33,J34,Track

# add for web api
import requests
import payconfiguration
import json
from datetime import datetime
import test_api
# add for web api end

    # os.remove("/home/pi/paypaymachine/run/s6.run")
    # open("/home/pi/paypaymachine/done/s6.done", 'w').close()
    # open(f"/home/pi/paypaymachine/done/{ordernumber}.done", 'w').close()
    sendAPItoken(ordernumber)
if __name__ == "__main__":
    main()