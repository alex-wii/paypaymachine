import serial
from time import sleep
# from setting import tdic1,tdic2
import json
import time
from AllConfig import Track

def main():
    usbpath =''
    with open("./TrackUsb.json", 'r') as obj1:
        usbpath = json.load(obj1)
    CMD=input('input the CMD : ')
    p1=usbpath[Track.ATrainID] ###  W2  ###
    with serial.Serial(p1, 57600) as ser:
        if CMD == "c1" :
            ser.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "c2" :
            ser.write(bytes(Track.PositionCup2 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "i" :
            ser.write(bytes(Track.PositionIce + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "1" :
            ser.write(bytes(Track.PositionS1 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "2" :
            ser.write(bytes(Track.PositionS2 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "3" :
            ser.write(bytes(Track.PositionS3 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "4" :
            ser.write(bytes(Track.PositionS4 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "5" :
            ser.write(bytes(Track.PositionS5 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
        if CMD == "6" :
            ser.write(bytes(Track.PositionEnd + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
            
if __name__ == "__main__":
    main()