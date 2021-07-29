import serial
from time import sleep
# from setting import tdic1,tdic2
import json
import time
from AllConfig import Track
def Moving():
    usbpath =""
    with open("/home/pi/paypaymachine/TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    AUsb=usbpath[Track.ATrainID]
    BUsb=usbpath[Track.BTrainID]
    YUsb=usbpath[Track.YTrackID]
    with serial.Serial(AUsb, 57600) as ser:
        ser.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
    with serial.Serial(BUsb, 57600) as ser2:
        ser2.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        ser2.write(bytes(Track.Move + "\r\n" , "utf-8"))
    with serial.Serial(YUsb, 57600) as ser3:
        ser3.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 20%speed    ###
        time.sleep(0.1)
        ser3.write(bytes(Track.YTrackEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        ser3.write(bytes(Track.Move + "\r\n" , "utf-8"))


Moving()
