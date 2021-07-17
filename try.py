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
from AllConfig import J17,J33,Track

track=sys.argv[1]

def main():
    
    usbpath =""
    with open("./TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    with serial.Serial() as ser:
        if track == "A":
            p1=usbpath[Track.ATrainID]
            ser.baudrate = 57600
            ser.port =p1
            ser.open()
            ser.write(bytes(Track.PositionS1 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
            # time.sleep(8)   #1:5 2:10 3:25
            while True:
                ser.flushInput()
                ser.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=ser.read(13).decode("utf-8")
                # print(address)
                na=address[11:13]
                # print(na,type(na))
                bc = " ".join(format(ord(c), "b") for c in na)
                # print(bc,type(bc))
                if len(bc) == 15:
                    bin=bc[13]
                    # print(bin,type(bin))
                    if  bin == "1":
                        break
            print("1")
if __name__ == "__main__":
    main()