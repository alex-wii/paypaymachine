import os
from shutil import move
import serial
from time import sleep
import json
from serial.tools import list_ports
import time
import sys
from pca9675 import PCA9675I2C
from AllConfig import J34,Track,USBdic
from MoveToStart import Moving

# pcaW18=PCA9675I2C(address=0x18,busnum=1)
# for i in range(16):
#     pcaW18.setup(i,0)
# pcaW18.output(J34.pin9,1)
# pcaW18.output(J17.pin2,1)
# pcaR=PCA9675I2C(address=0x27,busnum=1)
# for pin in range(16):
#         pcaR.setup(pin,1)
def I2CWriteBoardID():
    pcaW11=PCA9675I2C(address=0x11,busnum=1)
    pcaW15=PCA9675I2C(address=0x15,busnum=1)
    pcaW18=PCA9675I2C(address=0x18,busnum=1)
    pcaW1c=PCA9675I2C(address=0x1c,busnum=1)
    pcaW28=PCA9675I2C(address=0x28,busnum=1)
    pcaW2a=PCA9675I2C(address=0x2a,busnum=1)
    pcaW2c=PCA9675I2C(address=0x2c,busnum=1)
    pcaW2e=PCA9675I2C(address=0x2e,busnum=1)
    for i in range(16):   
            pcaW11.setup(i,0)
            pcaW15.setup(i,0)
            pcaW18.setup(i,0)
            pcaW1c.setup(i,0)
            pcaW28.setup(i,0)
            pcaW2a.setup(i,0)
            pcaW2c.setup(i,0)
            pcaW2e.setup(i,0)
    for i in range(16): 
            pcaW11.output(i,1)
            pcaW15.output(i,1)
            pcaW18.output(i,1)
            pcaW1c.output(i,1)
            pcaW28.output(i,1)
            pcaW2a.output(i,1)
            pcaW2c.output(i,1)
            pcaW2e.output(i,1)
    pcaW18.output(J34.pin2,0)
    pcaW18.output(J34.pin4,0)

            
def I2CReadBoardID():
    pcaR26=PCA9675I2C(address=0x26,busnum=1)
    for pin in range(16):
            pcaR26.setup(pin,1)
    pcaR27=PCA9675I2C(address=0x27,busnum=1)
    for pin in range(16):
            pcaR27.setup(pin,1)
    
def usbdicappend(deviceID,usbpath):
    USBdic[deviceID]=usbpath
testC=0
def checkportmovetostart(path):
    global testC
    testC=testC+1
    print(f'---{testC} path={path}')
    with serial.Serial(path, 57600) as ser:
        ser.write(bytes(Track.Read901C + "\r\n" , "utf-8")) #ch0 
        t_name=ser.read(13).decode("utf-8")
        usbdicappend(t_name,path)
        time.sleep(0.1)
        ser.write(bytes(Track.Origin + "\r\n" , "utf-8"))

def MoveToStart(path):
    with serial.Serial(path, 57600) as ser2:
        while True:
            ser2.flushInput() 
            ser2.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=ser2.read(13).decode("utf-8")
            na=address[11:13]
            bc = " ".join(format(ord(c), "b") for c in na)
            if len(bc) == 15:
                bin=bc[13]
                if  bin == "1":
                    break
        Moving()
def MoveToStart_B(track_path):
    ser = serial.Serial(track_path,57600)
    while True:
        ser.flushInput() 
        ser.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
        time.sleep(0.1)
        address=ser.read(13).decode("utf-8")
        na=address[11:13]
        bc = " ".join(format(ord(c), "b") for c in na)
        if len(bc) == 15:
            bin=bc[13]
            if  bin == "1":
                break
    Moving()
def findPrintby6790(comportlist):

    printerPath=""
    printerVid=6790
    for e in comportlist:
        if e.vid == printerVid:
            printerPath=e.device
            break
    return printerPath
def openserial(track_path):
    ser = serial.Serial(track_path,57600)
    ser.write(bytes(Track.Read901C + "\r\n" , "utf-8"))
    t_name=ser.read(13).decode("utf-8")
    USBdic[t_name]=track_path
    time.sleep(0.1)
    ser.write(bytes(Track.Origin + "\r\n" , "utf-8"))

    ser.close()
       

x = list_ports.comports()
comportlist = []
print(f'x={x}')

ppath=findPrintby6790(x)
print(f'ppath={ppath}')

with serial.Serial(ppath, 57600) as ser2:
    data = b'\x02\x00\x0A\x00\x35\xE0\x07\x03\x01\x08\x19\x2D\x01\x79\x03' #2016/03/01/08
    ser2.write(data)

for e in x:
    if "AMA0" in e.device :
        continue
    if len(ppath) > 5 :
        if ppath in e.device :
            continue    
    comportlist.append(e.device)    

pathlist = comportlist
print(pathlist)

for usbpath in pathlist :
    print(f'ubpath in for loop {usbpath}')
    # checkportmovetostart(usbpath)
    openserial(usbpath)
    print()
# remove code
# if os.path.isfile("./TrackUsb.json"):
#     pass
# else:
#     os.mknod("./TrackUsb.json")
# if os.path.isfile("./PrinterUsb.json"):
#     pass
# else:
#     os.mknod("./PrinterUsb.json")

print(USBdic)

with open("/home/pi/paypaymachine/TrackUsb.json", "w") as obj:
    json.dump(USBdic,obj,indent=4,sort_keys=True)
with open("/home/pi/paypaymachine/PrinterUsb.json", "w") as obj:
    json.dump(ppath,obj)
# open("/homeMoveToStart/pi/paypaymachine/TrackUsb.json", 'w').close()

for usbpath in pathlist :
    MoveToStart(usbpath)
# I2CWriteBoardID()
# I2CReadBoardID()


# if os.path.isdir("./run"):
#     pass
# else:
#     os.mkdir("run")
# if os.path.isdir("./done"):
#     pass
# else:
#     os.mkdir("done")
    
    
# try:
#     ########################
#     os.remove("./run/s0A.run")
#     os.remove("./run/s0B.run")
#     os.remove("./run/s0.run")
#     os.remove("./done/s0.done")
#     ########################
#     os.remove("./run/s1A.run")
#     os.remove("./run/s1B.run")
#     os.remove("./run/s1.run")
#     os.remove("./done/s1.done")
#     ########################
#     os.remove("./run/s2A.run")
#     os.remove("./run/s2B.run")
#     os.remove("./run/s2.run")
#     os.remove("./done/s2.done")
#     ########################
#     os.remove("./run/s3A.run")
#     os.remove("./run/s3B.run")
#     os.remove("./run/s3.run")
#     os.remove("./done/s3.done")
#     ########################
#     os.remove("./run/s4A.run")
#     os.remove("./run/s4B.run")
#     os.remove("./run/s4.run")
#     os.remove("./done/s4.done")
#     ########################
#     os.remove("./run/s5A.run")
#     os.remove("./run/s5B.run")
#     os.remove("./run/s5.run")
#     os.remove("./done/s5.done")
#     ########################
#     os.remove("./run/s6A.run")
#     os.remove("./run/s6B.run")
#     os.remove("./run/s6.run")
#     os.remove("./done/s6.done")
# except:
#     pass