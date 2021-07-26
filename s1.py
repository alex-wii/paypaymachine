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

doorA=PCA9675I2C(address=0x1c,busnum=1)      ###     A道電磁閥    ###
doorB=PCA9675I2C(address=0x11,busnum=1)      ###     B道電磁閥    ###
for i in range(16):
        # print(f'setup pin{i} is 0')    
        # pump.setup(i,0)
        doorA.setup(i,0)
        doorB.setup(i,0)
        doorA.output(i,1)
        doorB.output(i,1)
pump=PCA9675I2C(address=0x15,busnum=1)      ###     幫浦      ###
for i in range(16):
    pump.setup(i,0)
    time.sleep(0.1)
    doorA.output(i,0)
    doorB.output(i,0)
    pump.output(i,1)


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
            time.sleep(0.1)
            doorA.output(J17.pin2,1) 
            time.sleep(0.1)
            pump.output(J17.pin2,0) 
            time.sleep(time1)
            doorA.output(J17.pin2,0)
            time.sleep(0.1)
            pump.output(J17.pin2,1)
        if time2 !=0 :
            time.sleep(0.1)
            doorA.output(J17.pin4,1) 
            time.sleep(0.1)
            pump.output(J17.pin4,0)
            time.sleep(time2)
            doorA.output(J17.pin4,0)
            time.sleep(0.1)
            pump.output(J17.pin4,1)
        if time3 !=0 :
            time.sleep(0.1)
            doorA.output(J17.pin6,1)  
            time.sleep(0.1)
            pump.output(J17.pin6,0)
            time.sleep(time3)
            doorA.output(J17.pin6,0)
            time.sleep(0.1)
            pump.output(J17.pin6,1)
        if time4 !=0 :
            time.sleep(0.1)
            doorA.output(J17.pin8,1) 
            time.sleep(0.1)
            pump.output(J17.pin8,0)
            time.sleep(time4)
            doorA.output(J17.pin8,0)
            time.sleep(0.1)
            pump.output(J17.pin8,1)
        if time5 !=0 :
            time.sleep(0.1)
            doorA.output(J33.pin2,1)  
            time.sleep(0.1)
            pump.output(J33.pin2,0)
            time.sleep(time5)
            doorA.output(J33.pin2,0)
            time.sleep(0.1)
            pump.output(J33.pin2,1)

def Btrain():
        if time1 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin2,1) 
            time.sleep(0.1)
            pump.output(J17.pin2,0) 
            time.sleep(time1)
            doorB.output(J17.pin2,0)
            time.sleep(0.1)
            pump.output(J17.pin2,1)
        if time2 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin4,1) 
            time.sleep(0.1)
            pump.output(J17.pin4,0)
            time.sleep(time2)
            doorB.output(J17.pin4,0)
            time.sleep(0.1)
            pump.output(J17.pin4,1)
        if time3 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin6,1)  
            time.sleep(0.1)
            pump.output(J17.pin6,0)
            time.sleep(time3)
            doorB.output(J17.pin6,0)
            time.sleep(0.1)
            pump.output(J17.pin6,1)
        if time4 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin8,1) 
            time.sleep(0.1)
            pump.output(J17.pin8,0)
            time.sleep(time4)
            doorB.output(J17.pin8,0)
            time.sleep(0.1)
            pump.output(J17.pin8,1)
        if time5 !=0 :
            time.sleep(0.1)
            doorB.output(J33.pin2,1)  
            time.sleep(0.1)
            pump.output(J33.pin2,0)
            time.sleep(time5)
            doorB.output(J33.pin2,0)
            time.sleep(0.1)
            pump.output(J33.pin2,1)

def main():
    
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        sys.exit(1)
        open("./done/s1.done", 'w').close()
        
    usbpath =""
    with open("./TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    if os.path.isfile("./run/s1.run"):
                sys.exit(1)
    open("./run/s1.run", 'w').close()
    p1=usbpath[Track.ATrainID]
    p2=usbpath[Track.BTrainID]
    with serial.Serial(p1, 57600) as ser:
        if track == "A":
            if os.path.isfile("./run/s1B.run"):
                sys.exit(1)
            open("./run/s1A.run", 'w').close()
            ser.write(bytes(Track.PositionS1 + "\r\n" , "utf-8"))
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
            os.remove("./run/s1A.run")
    with serial.Serial(p2, 57600) as ser2:
        if track == "B":
            if os.path.isfile("./run/s1A.run"):
                sys.exit(1)
            open("./run/s1B.run", 'w').close()
            ser2.write(bytes(Track.PositionS1 + "\r\n" , "utf-8"))
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
            os.remove("./run/s1B.run")
    os.remove("./run/s1.run")
    open("./done/s1.done", 'w').close()

if __name__ == "__main__":
    main()