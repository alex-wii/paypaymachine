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
from AllConfig import J33,J34,Track

pump=PCA9675I2C(address=0x15,busnum=1)      ###     幫浦      ###
for i in range(16):
    pump.setup(i,0)
    # time.sleep(0.1)
    pump.output(i,1)
doorA=PCA9675I2C(address=0x1c,busnum=1)      ###     A道電磁閥    ###
for i in range(16):
    doorA.setup(i,0)
    doorA.output(i,1)
doorB=PCA9675I2C(address=0x11,busnum=1)      ###     B道電磁閥    ###
for i in range(16):
    doorB.setup(i,0)
    doorB.output(i,1)

iocontrolsleep = 1

track=sys.argv[1]
timedata=sys.argv[2]
machinetime=int(timedata)
#Station為站之參數
#data12345為5幫浦各自時間之參數
time1=int(timedata[2:4])
time2=int(timedata[6:8])
time3=int(timedata[10:12])
time4=int(timedata[14:16])
time5=int(timedata[18:20])
def Atrain():   
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            doorA.output(J33.pin4,0) 
            time.sleep(iocontrolsleep)
            pump.output(J33.pin4,0) 
            time.sleep(time1)
            pump.output(J33.pin4,1)
            time.sleep(iocontrolsleep)
            doorA.output(J33.pin4,1)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            doorA.output(J33.pin6,0) 
            time.sleep(iocontrolsleep)
            pump.output(J33.pin6,0)
            time.sleep(time2)
            pump.output(J33.pin6,1)
            time.sleep(iocontrolsleep)
            doorA.output(J33.pin6,1)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            doorA.output(J33.pin8,0)  
            time.sleep(iocontrolsleep)
            pump.output(J33.pin8,0)
            time.sleep(time3)
            pump.output(J33.pin8,1)
            time.sleep(iocontrolsleep)
            doorA.output(J33.pin8,1)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            doorA.output(J34.pin2,0) 
            time.sleep(iocontrolsleep)
            pump.output(J34.pin2,0)
            time.sleep(time4)
            pump.output(J34.pin2,1)
            time.sleep(iocontrolsleep)
            doorA.output(J34.pin2,1)
        if time5 !=0 :
            time.sleep(iocontrolsleep)
            doorA.output(J34.pin4,0)  
            time.sleep(iocontrolsleep)
            pump.output(J34.pin4,0)
            time.sleep(time5)
            pump.output(J34.pin4,1)
            time.sleep(iocontrolsleep)
            doorA.output(J34.pin4,1)

def Btrain():
        if time1 !=0 :
            time.sleep(iocontrolsleep)
            doorB.output(J33.pin4,0) 
            time.sleep(iocontrolsleep)
            pump.output(J33.pin4,0) 
            time.sleep(time1)
            pump.output(J33.pin4,1)
            time.sleep(iocontrolsleep)
            doorB.output(J33.pin4,1)
        if time2 !=0 :
            time.sleep(iocontrolsleep)
            doorB.output(J33.pin6,0) 
            time.sleep(iocontrolsleep)
            pump.output(J33.pin6,0)
            time.sleep(time2)
            pump.output(J33.pin6,1)
            time.sleep(iocontrolsleep)
            doorB.output(J33.pin6,1)
        if time3 !=0 :
            time.sleep(iocontrolsleep)
            doorB.output(J33.pin8,0)  
            time.sleep(iocontrolsleep)
            pump.output(J33.pin8,0)
            time.sleep(time3)
            pump.output(J33.pin8,1)
            time.sleep(iocontrolsleep)
            doorB.output(J33.pin8,1)
        if time4 !=0 :
            time.sleep(iocontrolsleep)
            doorB.output(J34.pin2,0) 
            time.sleep(iocontrolsleep)
            pump.output(J34.pin2,0)
            time.sleep(time4)
            pump.output(J34.pin2,1)
            time.sleep(iocontrolsleep)
            doorB.output(J34.pin2,1)
        if time5 !=0 :
            time.sleep(iocontrolsleep)
            doorB.output(J34.pin4,0)  
            time.sleep(iocontrolsleep)
            pump.output(J34.pin4,0)
            time.sleep(time5)
            pump.output(J34.pin4,1)
            time.sleep(iocontrolsleep)
            doorB.output(J34.pin4,1)
        
        
def main():
    
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        sys.exit(1)
        open("/home/pi/paypaymachine/done/s2.done", 'w').close()
        
    usbpath =""
    with open("/home/pi/paypaymachine/TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    if os.path.isfile("/home/pi/paypaymachine/run/s2.run"):
                sys.exit(1)
    open("/home/pi/paypaymachine/run/s2.run", 'w').close()
    p1=usbpath[Track.ATrainID]
    p2=usbpath[Track.BTrainID]
    with serial.Serial(p1, 57600) as ser:
        if track == "A":
            if os.path.isfile("/home/pi/paypaymachine/run/s2B.run"):
                sys.exit(1)
            open("/home/pi/paypaymachine/run/s2A.run", 'w').close()
            ser.write(bytes(Track.PositionS2 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser.write(bytes(Track.Move + "\r\n" , "utf-8"))
            while True:
                ser.flushInput() 
                ser.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=ser.read(13).decode("utf-8")
                # print(address)
                na=address[11:13]
                # print(na)
                bc = " ".join(format(ord(c), "b") for c in na)
                # print(bc,type(bc))
                if len(bc) == 15:
                    bin=bc[13]
                    # print(bin,type(bin))
                    if  bin == "1":
                        break
            Atrain()
            time.sleep(5)
            os.remove("/home/pi/paypaymachine/run/s2A.run")
    with serial.Serial(p2, 57600) as ser2:
        if track == "B":
            if os.path.isfile("/home/pi/paypaymachine/run/s2A.run"):
                sys.exit(1)
            open("/home/pi/paypaymachine/run/s2B.run", 'w').close()
            ser2.write(bytes(Track.PositionS2 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            ser2.write(bytes(Track.Move + "\r\n" , "utf-8"))
            while True:
                ser2.flushInput() 
                ser2.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=ser2.read(13).decode("utf-8")
                # print(address)
                na=address[11:13]
                # print(na)
                bc = " ".join(format(ord(c), "b") for c in na)
                # print(bc,type(bc))
                if len(bc) == 15:
                    bin=bc[13]
                    # print(bin,type(bin))
                    if  bin == "1":
                        break
            Btrain()
            time.sleep(5)
            os.remove("/home/pi/paypaymachine/run/s2B.run")
    time.sleep(1)
    os.remove("/home/pi/paypaymachine/run/s2.run")
    open("/home/pi/paypaymachine/done/s2.done", 'w').close()
    
if __name__ == "__main__":
    main()