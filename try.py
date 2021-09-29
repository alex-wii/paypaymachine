import serial
from time import sleep
import time
import pigpio
import os
import sys
import json
from AllConfig import J2,J3,J17,J33,J34,Track
from pca9675 import PCA9675I2C

pcaW11=PCA9675I2C(address=0x11,busnum=1)
pcaW11_Data = 0xFFFF
pcaW15=PCA9675I2C(address=0x15,busnum=1)
pcaW15_Data = 0xFFFF
pcaW18=PCA9675I2C(address=0x18,busnum=1)
pcaW18_Data = 0xFFFF
pcaW1c=PCA9675I2C(address=0x1c,busnum=1)
pcaW1c_Data = 0xFFFF
pcaW28=PCA9675I2C(address=0x28,busnum=1)
pcaW28_Data = 0xFFFF
pcaW2a=PCA9675I2C(address=0x2a,busnum=1)
pcaW2a_Data = 0xFFFF
pcaW2c=PCA9675I2C(address=0x2c,busnum=1)
pcaW2c_Data = 0xFFFF
pcaR27=PCA9675I2C(address=0x27,busnum=1)
pcaR26=PCA9675I2C(address=0x26,busnum=1)

pcaW18_Data=pcaW18.output(J34.pin4,0,pcaW18_Data)  ### 出杯轉盤關閉    ###
pcaW18_Data=pcaW18.output(J34.pin2,0,pcaW18_Data)  ### 出杯轉盤方向    ###
pcaW18_Data=pcaW18.output(J34.pin9,1,pcaW18_Data)  ### 爪夾   ###開爪

usbpath =''
with open("/home/pi/paypaymachine/TrackUsb.json", 'r') as obj1:
    usbpath = json.load(obj1)
with open("/home/pi/paypaymachine/PrinterUsb.json", "r") as obj1:
    Printer = json.load(obj1)

TrainA = usbpath[Track.ATrainID]
serA=serial.Serial(TrainA,57600)
TrainB = usbpath[Track.BTrainID]
serB=serial.Serial(TrainB,57600)
TrackY = usbpath[Track.YTrackID]
serY=serial.Serial(TrackY,57600)
TrackZ = usbpath[Track.ZTrackID]
serZ=serial.Serial(TrackZ,57600)
serP=serial.Serial(Printer,57600)
serP.bytesize=serial.EIGHTBITS

iocontrolsleep = 0.5

track=sys.argv[1] ##AS1,AS2,AS3,AS4,AS5,BS1,BS2,BS3,BS4,BS5
timedata=sys.argv[2]##01000200030004000500
machinetime=int(timedata)
time1=int(timedata[2:4])
time2=int(timedata[6:8])
time3=int(timedata[10:12])
time4=int(timedata[14:16])
time5=int(timedata[18:20])

def main():
    global pcaW15_Data
    global pcaW11_Data
    global pcaW28_Data
    global pcaW2a_Data
    global pcaW1c_Data
    global pcaW2c_Data

    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        sys.exit(1)
    if track == "AS1":
        print("AS1")
        pump = pcaW15
        doorA = pcaW1c
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin2,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin2,0,pcaW15_Data)
            time.sleep(time1)
            pcaW15_Data=pump.output(J17.pin2,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin2,1,pcaW1c_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin4,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin4,0,pcaW15_Data)
            time.sleep(time2)
            pcaW15_Data=pump.output(J17.pin4,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin4,1,pcaW1c_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin6,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin6,0,pcaW15_Data)
            time.sleep(time3)
            pcaW15_Data=pump.output(J17.pin6,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin6,1,pcaW1c_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin8,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin8,0,pcaW15_Data)
            time.sleep(time4)
            pcaW15_Data=pump.output(J17.pin8,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J17.pin8,1,pcaW1c_Data)
        if time5 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin2,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin2,0,pcaW15_Data)
            time.sleep(time5)
            pcaW15_Data=pump.output(J33.pin2,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin2,1,pcaW1c_Data)
    elif track == "AS2":
        print("AS2")
        pump = pcaW15
        doorA = pcaW1c
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin4,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin4,0,pcaW15_Data)
            time.sleep(time1)
            pcaW15_Data=pump.output(J33.pin4,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin4,1,pcaW1c_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin6,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin6,0,pcaW15_Data)
            time.sleep(time2)
            pcaW15_Data=pump.output(J33.pin6,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin6,1,pcaW1c_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin8,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin8,0,pcaW15_Data)
            time.sleep(time3)
            pcaW15_Data=pump.output(J33.pin8,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J33.pin8,1,pcaW1c_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J34.pin2,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J34.pin2,0,pcaW15_Data)
            time.sleep(time4)
            pcaW15_Data=pump.output(J34.pin2,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J34.pin2,1,pcaW1c_Data)
        if time5 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J34.pin4,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J34.pin4,0,pcaW15_Data)
            time.sleep(time5)
            pcaW15_Data=pump.output(J34.pin4,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J34.pin4,1,pcaW1c_Data)
    elif track == "AS3":
        print("AS3")
        pump = pcaW15
        doorA = pcaW1c
        pump1 = pcaW28
        doorA1 = pcaW2c
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J34.pin6,0,pcaW1c_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J34.pin6,0,pcaW15_Data)
            time.sleep(time1)
            pcaW15_Data=pump.output(J34.pin6,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW1c_Data=doorA.output(J34.pin6,1,pcaW1c_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA1.output(J34.pin7,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump1.output(J34.pin7,0,pcaW28_Data)
            time.sleep(time2)
            pcaW28_Data=pump1.output(J34.pin7,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA1.output(J34.pin7,1,pcaW2c_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA1.output(J17.pin2,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump1.output(J17.pin2,0,pcaW28_Data)
            time.sleep(time3)
            pcaW28_Data=pump1.output(J17.pin2,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA1.output(J17.pin2,1,pcaW2c_Data)
        if time4 !=0 :      ### 甜度糖_蔗糖_寡糖  ###
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA1.output(J34.pin9,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump1.output(J34.pin9,0,pcaW28_Data)
            time.sleep(time4)
            pcaW28_Data=pump1.output(J34.pin9,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA1.output(J34.pin9,1,pcaW2c_Data)
    #if time5 !=0 :
    #time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin4,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin4,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin4,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin4,1)
    elif track == "AS4":
        print("AS4")
        pump = pcaW28
        doorA = pcaW2c
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J34.pin4,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J34.pin4,0,pcaW28_Data)
            time.sleep(time1)
            pcaW28_Data=pump.output(J34.pin4,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J34.pin4,1,pcaW2c_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J17.pin6,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J17.pin6,0,pcaW28_Data)
            time.sleep(time2)
            pcaW28_Data=pump.output(J17.pin6,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J17.pin6,1,pcaW2c_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J17.pin8,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J17.pin8,0,pcaW28_Data)
            time.sleep(time3)
            pcaW28_Data=pump.output(J17.pin8,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J17.pin8,1,pcaW2c_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J34.pin2,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J34.pin2,0,pcaW28_Data)
            time.sleep(time4)
            pcaW28_Data=pump.output(J34.pin2,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J34.pin2,1,pcaW2c_Data)
    # if time5 !=0 :
    #     time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin8,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin8,0)
    #     time.sleep(time5)
    #     teapump.output(J17.pin8,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin8,1)
    elif track == "AS5":
        print("AS5")
        pump = pcaW28
        doorA = pcaW2c
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J33.pin2,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J33.pin2,0,pcaW28_Data)
            time.sleep(time1)
            pcaW28_Data=pump.output(J33.pin2,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J33.pin2,1,pcaW2c_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J33.pin4,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J33.pin4,0,pcaW28_Data)
            time.sleep(time2)
            pcaW28_Data=pump.output(J33.pin4,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J33.pin4,1,pcaW2c_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J34.pin6,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J34.pin6,0,pcaW28_Data)
            time.sleep(time3)
            pcaW28_Data=pump.output(J34.pin6,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J34.pin6,1,pcaW2c_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J33.pin8,0,pcaW2c_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J33.pin8,0,pcaW28_Data)
            time.sleep(time4)
            pcaW28_Data=pump.output(J33.pin8,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2c_Data=doorA.output(J33.pin8,1,pcaW2c_Data)
    # if time5 !=0 :
    #     time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin10,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin10,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin10,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin10,1)
    elif track == "BS1":  ########  B Train  ######
        print("BS1")
        pump = pcaW15
        doorB = pcaW11
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin2,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin2,0,pcaW15_Data)
            time.sleep(time1)
            pcaW15_Data=pump.output(J17.pin2,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin2,1,pcaW11_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin4,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin4,0,pcaW15_Data)
            time.sleep(time2)
            pcaW15_Data=pump.output(J17.pin4,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin4,1,pcaW11_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin6,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin6,0,pcaW15_Data)
            time.sleep(time3)
            pcaW15_Data=pump.output(J17.pin6,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin6,1,pcaW11_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin8,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J17.pin8,0,pcaW15_Data)
            time.sleep(time4)
            pcaW15_Data=pump.output(J17.pin8,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J17.pin8,1,pcaW11_Data)
        if time5 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin2,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin2,0,pcaW15_Data)
            time.sleep(time5)
            pcaW15_Data=pump.output(J33.pin2,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin2,1,pcaW11_Data)
    elif track == "BS2":
        print("BS2")
        pump = pcaW15
        doorB = pcaW11
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin4,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin4,0,pcaW15_Data)
            time.sleep(time1)
            pcaW15_Data=pump.output(J33.pin4,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin4,1,pcaW11_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin6,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin6,0,pcaW15_Data)
            time.sleep(time2)
            pcaW15_Data=pump.output(J33.pin6,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin6,1,pcaW11_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin8,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J33.pin8,0,pcaW15_Data)
            time.sleep(time3)
            pcaW15_Data=pump.output(J33.pin8,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J33.pin8,1,pcaW11_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J34.pin2,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J34.pin2,0,pcaW15_Data)
            time.sleep(time4)
            pcaW15_Data=pump.output(J34.pin2,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J34.pin2,1,pcaW11_Data)
        if time5 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J34.pin4,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J34.pin4,0,pcaW15_Data)
            time.sleep(time5)
            pcaW15_Data=pump.output(J34.pin4,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J34.pin4,1,pcaW11_Data)
    elif track == "BS3":
        print("BS3")
        pump = pcaW15
        doorB = pcaW11
        pump1 = pcaW28
        doorB1 = pcaW2a
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J34.pin6,0,pcaW11_Data)
            time.sleep(iocontrolsleep)
            pcaW15_Data=pump.output(J34.pin6,0,pcaW15_Data)
            time.sleep(time1)
            pcaW15_Data=pump.output(J34.pin6,1,pcaW15_Data)
            time.sleep(iocontrolsleep)
            pcaW11_Data=doorB.output(J34.pin6,1,pcaW11_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB1.output(J34.pin7,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump1.output(J34.pin7,0,pcaW28_Data)
            time.sleep(time2)
            pcaW28_Data=pump1.output(J34.pin7,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB1.output(J34.pin7,1,pcaW2a_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB1.output(J17.pin2,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump1.output(J17.pin2,0,pcaW28_Data)
            time.sleep(time3)
            pcaW28_Data=pump1.output(J17.pin2,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB1.output(J17.pin2,1,pcaW2a_Data)
        if time4 !=0 :      ### 甜度糖_蔗糖_寡糖  ###
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB1.output(J34.pin9,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump1.output(J34.pin9,0,pcaW28_Data)
            time.sleep(time4)
            pcaW28_Data=pump1.output(J34.pin9,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB1.output(J34.pin9,1,pcaW2a_Data)
    # if time5 !=0 :
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin4,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin4,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin4,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin4,1)
    elif track == "BS4":
        print("BS4")
        pump = pcaW28
        doorB = pcaW2a
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J34.pin4,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J34.pin4,0,pcaW28_Data)
            time.sleep(time1)
            pcaW28_Data=pump.output(J34.pin4,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J34.pin4,1,pcaW2a_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J17.pin6,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J17.pin6,0,pcaW28_Data)
            time.sleep(time2)
            pcaW28_Data=pump.output(J17.pin6,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J17.pin6,1,pcaW2a_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J17.pin8,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J17.pin8,0,pcaW28_Data)
            time.sleep(time3)
            pcaW28_Data=pump.output(J17.pin8,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J17.pin8,1,pcaW2a_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J34.pin2,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J34.pin2,0,pcaW28_Data)
            time.sleep(time4)
            pcaW28_Data=pump.output(J34.pin2,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J34.pin2,1,pcaW2a_Data)
    # if time5 !=0 :
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin7,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin8,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin8,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin7,1)
    elif track == "BS5":
        print("BS5")
        pump = pcaW28
        doorB = pcaW2a
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J33.pin2,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J33.pin2,0,pcaW28_Data)
            time.sleep(time1)
            pcaW28_Data=pump.output(J33.pin2,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J33.pin2,1,pcaW2a_Data)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J33.pin4,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J33.pin4,0,pcaW28_Data)
            time.sleep(time2)
            pcaW28_Data=pump.output(J33.pin4,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J33.pin4,1,pcaW2a_Data)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J34.pin6,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J34.pin6,0,pcaW28_Data)
            time.sleep(time3)
            pcaW28_Data=pump.output(J34.pin6,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J34.pin6,1,pcaW2a_Data)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J33.pin8,0,pcaW2a_Data)
            time.sleep(iocontrolsleep)
            pcaW28_Data=pump.output(J33.pin8,0,pcaW28_Data)
            time.sleep(time4)
            pcaW28_Data=pump.output(J33.pin8,1,pcaW28_Data)
            time.sleep(iocontrolsleep)
            pcaW2a_Data=doorB.output(J33.pin8,1,pcaW2a_Data)
    # if time5 !=0 :
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin9,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin10,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin10,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin9,1)
if __name__ == "__main__":
    main()