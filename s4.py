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
from AllConfig import J17,J33,J34,Track


###     給料模組    ###
pump=PCA9675I2C(address=0x28,busnum=1)      ###     幫浦      ###
doorA=PCA9675I2C(address=0x2c,busnum=1)      ###     A道電磁閥    ###
doorB=PCA9675I2C(address=0x2a,busnum=1)      ###     B道電磁閥    ###
###     沖茶模組    ###
teapump=PCA9675I2C(address=0x2e,busnum=1)      ###     幫浦1     ###
teadoorA=PCA9675I2C(address=0x2e,busnum=1)      ###     A道電磁閥    ###
teadoorB=PCA9675I2C(address=0x2e,busnum=1)      ###     B道電磁閥    ###
for i in range(16):
        # print(f'setup pin{i} is 0')    
        pump.setup(i,0)
        doorA.setup(i,0)
        doorB.setup(i,0)
        teapump.setup(i,0)
        teadoorA.setup(i,0)
        teadoorB.setup(i,0)
    
for i in range(16):
        # print(f'setup pin{i} is 1')    
    pump.output(i,1)
    doorA.output(i,1)
    doorB.output(i,1)
    teapump.output(i,1)
    teadoorA.output(i,1)
    teadoorB.output(i,1)
# pcaR=PCA9675I2C(address=0x26,busnum=1)


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
            doorA.output(J17.pin4,0) 
            time.sleep(0.1)
            pump.output(J17.pin4,0) 
            time.sleep(time1)
            pump.output(J17.pin4,1)
            time.sleep(0.1)
            doorA.output(J17.pin4,1)
        if time2 !=0 :
            time.sleep(0.1)
            doorA.output(J17.pin6,0) 
            time.sleep(0.1)
            pump.output(J17.pin6,0)
            time.sleep(time2)
            pump.output(J17.pin6,1)
            time.sleep(0.1)
            doorA.output(J17.pin6,1)
        if time3 !=0 :
            time.sleep(0.1)
            doorA.output(J17.pin8,0)  
            time.sleep(0.1)
            pump.output(J17.pin8,0)
            time.sleep(time3)
            pump.output(J17.pin8,1)
            time.sleep(0.1)
            doorA.output(J17.pin8,1)
        if time4 !=0 :
            time.sleep(0.1)
            teadoorA.output(J33.pin6,0) 
            time.sleep(0.1)
            teapump.output(J17.pin6,0)
            time.sleep(time4)
            teapump.output(J17.pin6,1)
            time.sleep(0.1)
            teadoorA.output(J33.pin6,1)
        if time5 !=0 :
            time.sleep(0.1)
            teadoorA.output(J33.pin8,0)  
            time.sleep(0.1)
            teapump.output(J17.pin8,0)
            time.sleep(time5)
            teapump.output(J17.pin8,1)
            time.sleep(0.1)
            teadoorA.output(J33.pin8,1)

def Btrain():
        if time1 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin4,0) 
            time.sleep(0.1)
            pump.output(J17.pin4,0) 
            time.sleep(time1)
            pump.output(J17.pin4,1)
            time.sleep(0.1)
            doorB.output(J17.pin4,1)
        if time2 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin6,0) 
            time.sleep(0.1)
            pump.output(J17.pin6,0)
            time.sleep(time2)
            pump.output(J17.pin6,1)
            time.sleep(0.1)
            doorB.output(J17.pin6,1)
        if time3 !=0 :
            time.sleep(0.1)
            doorB.output(J17.pin8,0)  
            time.sleep(0.1)
            pump.output(J17.pin8,0)
            time.sleep(time3)
            pump.output(J17.pin8,1)
            time.sleep(0.1)
            doorB.output(J17.pin8,1)
        if time4 !=0 :
            time.sleep(0.1)
            teadoorB.output(J34.pin6,0) 
            time.sleep(0.1)
            teapump.output(J17.pin6,0)
            time.sleep(time4)
            teapump.output(J17.pin6,1)
            time.sleep(0.1)
            teadoorB.output(J34.pin6,1)
        if time5 !=0 :
            time.sleep(0.1)
            teadoorB.output(J34.pin7,0)  
            time.sleep(0.1)
            teapump.output(J17.pin8,0)
            time.sleep(time5)
            teapump.output(J17.pin8,1)
            time.sleep(0.1)
            teadoorB.output(J34.pin7,1)
            
def main():
    
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        sys.exit(1)
        open("./done/s4.done", 'w').close()
    
    usbpath =""
    with open("./TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    if os.path.isfile("./run/s4.run"):
                sys.exit(1)
    open("./run/s4.run", 'w').close()
    with serial.Serial() as ser:
        if track == "A":
            if os.path.isfile("./run/s4B.run"):
                sys.exit(1)
            p1=usbpath[Track.ATrainID]
            open("./run/s4A.run", 'w').close()
            ser.baudrate = 57600
            ser.port =p1
            ser.open()
            ser.write(bytes(Track.PositionS4 + "\r\n" , "utf-8"))
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
            os.remove("./run/s4A.run")
    with serial.Serial() as ser2:
        if track == "B":
            if os.path.isfile("./run/s4A.run"):
                sys.exit(1)
            p2=usbpath[Track.BTrainID]
            open("./run/s4B.run", 'w').close()
            ser2.baudrate = 57600
            ser2.port =p2
            ser2.open()
            ser2.write(bytes(Track.PositionS4 + "\r\n" , "utf-8"))
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
            os.remove("./run/s4B.run")
    os.remove("./run/s4.run")
    open("./done/s4.done", 'w').close()
    
if __name__ == "__main__":
    main()