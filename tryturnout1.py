import time
import pigpio
import sys
import serial
import json
from AllConfig import J17,J33,J34,J3,Track
from pca9675 import PCA9675I2C

pcaR=PCA9675I2C(address=0x26,busnum=1)
for pin in range(16):
    pcaR.setup(pin,1)
    
pca=PCA9675I2C(address=0x18,busnum=1)
for i in range(16):
    pca.setup(i,0)
pca.output(J17.pin2,1)  ### A道第一管落杯   ###
pca.output(J17.pin4,1)  ### B道第一管落杯   ###
pca.output(J17.pin6,1)  ### A道第二管落杯   ###
pca.output(J17.pin8,1)  ### B道第二管落杯   ###
pca.output(J34.pin9,1)  ### 爪夾   ###
pca.output(J33.pin4,1)  ### 落冰推桿    ###
PWM_CONTROL_PIN = 13
PWM_FREQ = 10000
pi = pigpio.pi()
pi.hardware_PWM(PWM_CONTROL_PIN, PWM_FREQ, 90000)

ordernumber=sys.argv[2]
asciinum = [] 
for e in ordernumber:
   asciinum.append(ord(e))
def countA():
    a1=asciinum[0]-65
    a2=asciinum[1]-48
    a3=asciinum[2]-48
    a4=asciinum[3]-48
    a5=asciinum[4]-48
    sum=a1+a2+a3+a4+a5
    return sum
def counta():
    a1=asciinum[0]-97
    a2=asciinum[1]-48
    a3=asciinum[2]-48
    a4=asciinum[3]-48
    a5=asciinum[4]-48
    sum=a1+a2+a3+a4+a5
    return sum
if ordernumber[0].isupper() :
   testcode= 77
   Verificationcode=testcode+countA()
else:
   testcode= 109
   Verificationcode=testcode+counta()
def main():
    with open("./TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    with open("./PrinterUsb.json", "r") as obj1:
        printerusb = json.load(obj1)
    TrackY = usbpath[Track.YTrackID]
    serY=serial.Serial(TrackY,57600)
    TrackZ = usbpath[Track.ZTrackID]
    serZ=serial.Serial(TrackZ,57600)
    Printer = printerusb
    serP=serial.Serial(Printer,57600)
    serP.bytesize=serial.EIGHTBITS
    serP.open()
    serY.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 20%speed    ###
    time.sleep(0.1)
    serY.write(bytes(Track.YTrackEnd + "\r\n" , "utf-8"))
    time.sleep(0.1) 
    serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
    time.sleep(8)   #1:5 2:10 3:25
    serY.flushInput() 
    serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
    time.sleep(0.1)
    address8=serY.read(13).decode("utf-8")
    na8=address8[11:13]
    bc8 = " ".join(format(ord(c), "b") for c in na8)
    bin8=bc8[13]
    if  bin8 == "1":    ### Z道下至轉盤(250)並張爪 ###
        serY.close()
        if pcaR.input(J3.pin2) != 0 :
            while pcaR.input(J3.pin5) != 0 :   ###滿盤###
                pca.output(J34.pin4,1)
                time.sleep(9.9865)   ###180度###
                pca.output(J34.pin4,0)
                time.sleep(5)   ###停五秒###
                if  pcaR.input(J3.pin2) == 0 :
                    break
                
            while pcaR.input(J3.pin5) == 0 :   ###有異物###
                pca.output(J34.pin4,1)
                time.sleep(2.9)   ###一個杯子距離###
                pca.output(J34.pin4,0)
                time.sleep(5)   ###停五秒###
                if  pcaR.input(J3.pin2) == 0 :
                    break
        if pcaR.input(J3.pin2) == 0 :
            time.sleep(0.1)
            serZ.write(bytes(Track.ZTrackDown + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
            time.sleep(5)   #1:5 2:10 3:25
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address9=serZ.read(13).decode("utf-8")
            na9=address9[11:13]
            bc9 = " ".join(format(ord(c), "b") for c in na9)
            bin9=bc9[13]
            if  bin9 == "1":    ### 出杯sensor感應到杯子，張爪，Z道上至0 ###
                while pcaR.input(J3.pin2) != 0 :
                    pca.output(J34.pin9,1)  
                    time.sleep(0.5)
                    serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))
                    time.sleep(0.1) 
                    serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                    time.sleep(5)   #1:5 2:10 3:25
                    serZ.flushInput() 
                    serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                    time.sleep(0.1)
                    address10=serZ.read(13).decode("utf-8")
                    na10=address10[11:13]
                    bc10 = " ".join(format(ord(c), "b") for c in na10)
                    bin10=bc10[13]
                    if  bin10 == "1":
                        pca.output(J34.pin4,1)     ## 1啟動,0停止  ##  
                        time.sleep(0.1) 
                        #stop
                        serP.write([2,0,6,1,70,0,0,0,0,77,3])
                        time.sleep(0.1)
                        #訂單編號
                        # testchk(ser)
                        serP.write([2,0,9,0,61,1,5,asciinum[0],asciinum[1],asciinum[2],asciinum[3],asciinum[4],Verificationcode,3])
                        time.sleep(0.5)
                        #print out
                        serP.write([2,0,6,1,70,4,0,0,0,81,3])
                        time.sleep(0.5)
                        serP.write([2,0,6,1,70,0,0,0,0,77,3])
                        time.sleep(9.9865)   ### 轉盤轉到客人取杯位置之時間(須測試)  ###
                        while pcaR.input(J3.pin4) != 0 : ###   截斷sensor偵測到杯子    ###
                            pca.output(J34.pin4,0)
                            time.sleep(5)    ### 等客人拿杯子的時間 ###
                        pca.output(J34.pin4,0)
                        serZ.close()
                        serP.close()
if __name__ == "__main__":
    main()