import serial
from time import sleep
# from setting import tdic1,tdic2
import json
import time
from AllConfig import Track
def Moving():
    usbpath =""
    with open("./TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    AUsb=usbpath[Track.ATrainID]
    BUsb=usbpath[Track.BTrainID]
    YUsb=usbpath[Track.YTrackID]
    with serial.Serial() as ser:
        ser.baudrate = 57600
        ser.port = AUsb
        ser.open()
        ser.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
    with serial.Serial() as ser2:
        ser2.baudrate = 57600
        ser2.port = BUsb
        ser2.open()
        ser2.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        ser2.write(bytes(Track.Move + "\r\n" , "utf-8"))
    with serial.Serial() as ser3:
        ser3.baudrate = 57600
        ser3.port = YUsb
        ser3.open()
        ser3.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 20%speed    ###
        time.sleep(0.1)
        ser3.write(bytes(Track.YTrackEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        ser3.write(bytes(Track.Move + "\r\n" , "utf-8"))