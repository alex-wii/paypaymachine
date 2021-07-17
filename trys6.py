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
from AllConfig import J3,J17,J33,J34,Track


PWM_CONTROL_PIN = 13
PWM_FREQ = 10000
pi = pigpio.pi()
pi.hardware_PWM(PWM_CONTROL_PIN, PWM_FREQ, 90000)

# pcaR=PCA9675I2C(address=0x26,busnum=1)
# for pin in range(16):
#     pcaR.setup(pin,1)
    
pca=PCA9675I2C(address=0x18,busnum=1)
for i in range(16):
    pca.setup(i,0)
pca.output(J17.pin2,1)  ### A道第一管落杯   ###
pca.output(J17.pin4,1)  ### B道第一管落杯   ###
pca.output(J17.pin6,1)  ### A道第二管落杯   ###
pca.output(J17.pin8,1)  ### B道第二管落杯   ###
pca.output(J34.pin9,1)  ### 爪夾   ###
pca.output(J33.pin4,1)  ### 落冰推桿    ###


track=sys.argv[1]
# ordernumber=sys.argv[2]
# asciinum = [] 
# for e in ordernumber:
#    asciinum.append(ord(e))
# def countA():
#     a1=asciinum[0]-65
#     a2=asciinum[1]-48
#     a3=asciinum[2]-48
#     a4=asciinum[3]-48
#     a5=asciinum[4]-48
#     sum=a1+a2+a3+a4+a5
#     return sum
# def counta():
#     a1=asciinum[0]-97
#     a2=asciinum[1]-48
#     a3=asciinum[2]-48
#     a4=asciinum[3]-48
#     a5=asciinum[4]-48
#     sum=a1+a2+a3+a4+a5
#     return sum
# if ordernumber[0].isupper() :
#    testcode= 77
#    Verificationcode=testcode+countA()
# else:
#    testcode= 109
#    Verificationcode=testcode+counta()

def main():

    usbpath =""
    with open("./TrackUsb.json", "r") as obj1:
        usbpath = json.load(obj1)
    with open("./PrinterUsb.json", "r") as obj1:
        printerusb = json.load(obj1)
    # if os.path.isfile("./run/s6.run"):
    #             sys.exit(1)
    # open("./run/s6.run", 'w').close()
    TrainA = usbpath[Track.ATrainID]
    serA=serial.Serial(TrainA,57600)
    TrainB = usbpath[Track.BTrainID]
    serB=serial.Serial(TrainB,57600)
    TrackY = usbpath[Track.YTrackID]
    serY=serial.Serial(TrackY,57600)
    TrackZ = usbpath[Track.ZTrackID]
    serZ=serial.Serial(TrackZ,57600)
    # Printer = printerusb
    # serP=serial.Serial(Printer,57600)
    # serP.bytesize=serial.EIGHTBITS
    # serP.open()
    if track == "A":
        # if os.path.isfile("./run/s6B.run"):
        #     sys.exit(1)
        # open("./run/s6A.run", 'w').close()
        # serA.open()
        serA.write(bytes(Track.PositionEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            addressa=serA.read(13).decode("utf-8")
            # print(address)
            naa=addressa[11:13]
            # print(na)
            bca = " ".join(format(ord(c), "b") for c in naa)
            # print(bc,type(bc))
            if len(bca) == 15:
                bina=bca[13]
            # print(bin,type(bin))
                if  bina == "1":
                    break
                # serY.open()
                # serZ.open()
                # serP.open()
        time.sleep(0.1)
        serY.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 20%speed    ###
        time.sleep(0.1) 
        serY.write(bytes(Track.YTrackA + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serY.flushInput() 
            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serY.read(13).decode("utf-8")
            na0=address[11:13]
            bc0 = " ".join(format(ord(c), "b") for c in na0)
            if len(bc0) == 15:
                bin0=bc0[13]
                if  bin0 == "1":         ### Z道下去抓杯位置(250)並收爪 ###
                    break
        time.sleep(0.1)
        serZ.write(bytes(Track.ZTrackDown + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address1=serZ.read(13).decode("utf-8")
            na1=address1[11:13]
            bc1 = " ".join(format(ord(c), "b") for c in na1)
            if len(bc1) == 15:
                bin1=bc1[13]
                if  bin1 == "1":    ### Z道回0位置 ###
                    break
        time.sleep(0.1)
        pca.output(J34.pin9,0)
        time.sleep(1)
        serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))
        time.sleep(0.1)
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address2=serZ.read(13).decode("utf-8")
            na2=address2[11:13]
            bc2 = " ".join(format(ord(c), "b") for c in na2)
            if len(bc2) == 15:
                bin2=bc2[13]
                if  bin2 == "1":    ### A道回原點 ###
                    break
        time.sleep(0.1)
        serA.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
        time.sleep(0.1)
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        time.sleep(0.1)
        serY.write(bytes(Track.YTrackCup + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serY.flushInput() 
            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address3=serY.read(13).decode("utf-8")
            na3=address3[11:13]
            bc3 = " ".join(format(ord(c), "b") for c in na3)
            if len(bc3) == 15:
                bin3=bc3[13]
                if  bin3 == "1":    ### Z道下至封杯位置(197) ### 
                    break
        time.sleep(0.1)
        serZ.write(bytes(Track.ZTrackPutCup + "\r\n" , "utf-8"))
        time.sleep(0.1)
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address4=serZ.read(13).decode("utf-8")
            na4=address4[11:13]
            bc4 = " ".join(format(ord(c), "b") for c in na4)
            if len(bc4) == 15:
                bin4=bc4[13]
                if  bin4 == "1":    ### 張爪並Z道上至50 ###
                    break
        time.sleep(0.1)
        pca.output(J34.pin9,1)
        time.sleep(0.1)
        serZ.write(bytes(Track.ZTrackWaitCup + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        time.sleep(8)
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address5=serZ.read(13).decode("utf-8")
            na5=address5[11:13]
            bc5 = " ".join(format(ord(c), "b") for c in na5)
            if len(bc5) == 15:
                bin5=bc5[13]
                if  bin5 == "1":    ### Z道下至封杯位置(197) ###
                    break
        time.sleep(0.1)   
        serZ.write(bytes(Track.ZTrackPutCup + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address6=serZ.read(13).decode("utf-8")
            na6=address6[11:13]
            bc6 = " ".join(format(ord(c), "b") for c in na6)
            if len(bc6) == 15:
                bin6=bc6[13]
                if  bin6 == "1":    ### 收爪並Z道上至0 ###
                    break
        time.sleep(0.1)
        pca.output(J34.pin9,0)
        time.sleep(1)
        serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address7=serZ.read(13).decode("utf-8")
            na7=address7[11:13]
            bc7 = " ".join(format(ord(c), "b") for c in na7)
            if len(bc7) == 15:
                bin7=bc7[13]
                if  bin7 == "1":    ### Y道至轉盤(600) ###
                    break
        time.sleep(0.1)
        serY.write(bytes(Track.YTrackEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serY.flushInput() 
            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address8=serY.read(13).decode("utf-8")
            na8=address8[11:13]
            bc8 = " ".join(format(ord(c), "b") for c in na8)
            if len(bc8) == 15:
                bin8=bc8[13]
                if  bin8 == "1":    ### Z道下至轉盤(250)並張爪 ###
                    break
        # serY.close()
        # if pcaR.input(J3.pin2) != 0 :
        #     while pcaR.input(J3.pin5) != 0 :   ###滿盤###
        #         pca.output(J34.pin4,1)
        #         time.sleep(9.9865)   ###180度###
        #         pca.output(J34.pin4,0)
        #         time.sleep(5)   ###停五秒###
        #         if  pcaR.input(J3.pin2) == 0 :
        #             break
                
        #     while pcaR.input(J3.pin5) == 0 :   ###有異物###
        #         pca.output(J34.pin4,1)
        #         time.sleep(2.9)   ###一個杯子距離###
        #         pca.output(J34.pin4,0)
        #         time.sleep(5)   ###停五秒###
        #         if  pcaR.input(J3.pin2) == 0 :
        #             break
        # if pcaR.input(J3.pin2) == 0 :
        time.sleep(0.1)
        serZ.write(bytes(Track.ZTrackDown + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address9=serZ.read(13).decode("utf-8")
            na9=address9[11:13]
            bc9 = " ".join(format(ord(c), "b") for c in na9)
            if len(bc9) == 15:
                bin9=bc9[13]
                if  bin9 == "1":    ### 出杯sensor感應到杯子，張爪，Z道上至0 ###
                    break
        # while pcaR.input(J3.pin2) != 0 :
        time.sleep(0.1) 
        pca.output(J34.pin9,1)  
        time.sleep(1)
        serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True:
            serZ.flushInput() 
            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address10=serZ.read(13).decode("utf-8")
            na10=address10[11:13]
            bc10 = " ".join(format(ord(c), "b") for c in na10)
            if len(bc10) == 15:
                bin10=bc10[13]
                if  bin10 == "1":
                    break
        time.sleep(0.1)
        serY.write(bytes(Track.YTrackA + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
        #     pca.output(J34.pin4,1)     ## 1啟動,0停止  ##  
        #     time.sleep(0.1) 
        #     #stop
        #     serP.write([2,0,6,1,70,0,0,0,0,77,3])
        #     time.sleep(0.1) 
        #     #訂單編號
        #     # testchk(ser)
        #     serP.write([2,0,9,0,61,1,5,asciinum[0],asciinum[1],asciinum[2],asciinum[3],asciinum[4],Verificationcode,3])
        #     time.sleep(0.5)
        #     #print out
        #     serP.write([2,0,6,1,70,4,0,0,0,81,3])
        #     time.sleep(0.5)
        #     serP.write([2,0,6,1,70,0,0,0,0,77,3])
        #     time.sleep(9.9865)   ### 轉盤轉到客人取杯位置之時間(須測試)  ###
        #     while pcaR.input(J3.pin4) != 0 : ###   截斷sensor偵測到杯子    ###
        #         pca.output(J34.pin4,0)
        #         time.sleep(5)    ### 等客人拿杯子的時間 ###
        #     pca.output(J34.pin4,0)
        serZ.close()
        serY.close()
            # serP.close()
            # os.remove("./run/s6A.run")
    if track == "B":
        if os.path.isfile("./run/s6A.run"):
            sys.exit(1)
        open("./run/s6B.run", 'w').close()
        serB.open()
        serB.write(bytes(Track.PositionEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        time.sleep(8)  #1:5 2:10 3:25
        serB.flushInput() 
        serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
        time.sleep(0.1)
        addressb=serB.read(13).decode("utf-8")
        # print(address)
        na=addressb[11:13]
        # print(na)
        bc = " ".join(format(ord(c), "b") for c in na)
        # print(bc,type(bc))
        bin=bc[13]
        # print(bin,type(bin))
        if  bin == "1":
            serY.open()
            serZ.open()
            serP.open()
            serY.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 20%speed    ###
            time.sleep(0.1) 
            serY.write(bytes(Track.YTrackB + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
            time.sleep(5)   #1:5 2:10 3:25
            serY.flushInput() 
            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serY.read(13).decode("utf-8")
            na=address[11:13]
            bc = " ".join(format(ord(c), "b") for c in na)
            bin=bc[13]
            if  bin == "1":         ### Z道下去抓杯位置(250)並收爪 ###
                time.sleep(0.1)
                serZ.write(bytes(Track.ZTrackDown + "\r\n" , "utf-8"))
                time.sleep(0.1) 
                serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                time.sleep(5)   #1:5 2:10 3:25
                serZ.flushInput() 
                serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address1=serZ.read(13).decode("utf-8")
                na1=address1[11:13]
                bc1 = " ".join(format(ord(c), "b") for c in na1)
                bin1=bc1[13]
                if  bin1 == "1":    ### Z道回0位置 ###
                    pca.output(J34.pin9,0)
                    time.sleep(1)
                    serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))
                    time.sleep(0.1)
                    serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                    time.sleep(5)   #1:5 2:10 3:25
                    serZ.flushInput() 
                    serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                    time.sleep(0.1)
                    address2=serZ.read(13).decode("utf-8")
                    na2=address2[11:13]
                    bc2 = " ".join(format(ord(c), "b") for c in na2)
                    bin2=bc2[13]
                    if  bin2 == "1":    ### B道回原點 ###
                        serB.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
                        time.sleep(0.1)
                        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
                        time.sleep(10)
                        serB.flushInput() 
                        serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                        time.sleep(0.1)
                        addressB=serB.read(13).decode("utf-8")
                        naB=addressB[11:13]
                        bcB = " ".join(format(ord(c), "b") for c in naB)
                        binB=bcB[13]
                        if  binB == "1":    ### Y道到封杯位置(0) ###
                            time.sleep(0.1)
                            serY.write(bytes(Track.YTrackCup + "\r\n" , "utf-8"))
                            time.sleep(0.1) 
                            serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
                            time.sleep(5)   #1:5 2:10 3:25
                            serY.flushInput() 
                            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                            time.sleep(0.1)
                            address3=serY.read(13).decode("utf-8")
                            na3=address3[11:13]
                            bc3 = " ".join(format(ord(c), "b") for c in na3)
                            bin3=bc3[13]
                            if  bin3 == "1":    ### Z道下至封杯位置(197)並張爪 ###
                                time.sleep(0.1)
                                serZ.write(bytes(Track.ZTrackPutCup + "\r\n" , "utf-8"))
                                time.sleep(0.1)
                                serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                                time.sleep(2.5)
                                pca.output(J34.pin9,1)
                                time.sleep(1.5)
                                serZ.flushInput() 
                                serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                                time.sleep(0.1)
                                address4=serZ.read(13).decode("utf-8")
                                na4=address4[11:13]
                                bc4 = " ".join(format(ord(c), "b") for c in na4)
                                bin4=bc4[13]
                                if  bin4 == "1":    ### Z道上至50 ###
                                    time.sleep(0.1)
                                    serZ.write(bytes(Track.ZTrackWaitCup + "\r\n" , "utf-8"))
                                    time.sleep(0.1) 
                                    serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                                    time.sleep(5)   #1:5 2:10 3:25
                                    serZ.flushInput() 
                                    serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                                    time.sleep(0.1)
                                    address5=serZ.read(13).decode("utf-8")
                                    na5=address5[11:13]
                                    bc5 = " ".join(format(ord(c), "b") for c in na5)
                                    bin5=bc5[13]
                                    if  bin5 == "1":    ### Z道下至封杯位置(197)並收爪 ###
                                        time.sleep(10)   
                                        serZ.write(bytes(Track.ZTrackPutCup + "\r\n" , "utf-8"))
                                        time.sleep(0.1) 
                                        serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                                        time.sleep(5)   #1:5 2:10 3:25
                                        serZ.flushInput() 
                                        serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                                        time.sleep(0.1)
                                        address6=serZ.read(13).decode("utf-8")
                                        na6=address6[11:13]
                                        bc6 = " ".join(format(ord(c), "b") for c in na6)
                                        bin6=bc6[13]
                                        if  bin6 == "1":    ### Z道上至0 ###
                                            pca.output(J34.pin9,0)
                                            time.sleep(0.3)
                                            serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))
                                            time.sleep(0.1) 
                                            serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
                                            time.sleep(5)   #1:5 2:10 3:25
                                            serZ.flushInput() 
                                            serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                                            time.sleep(0.1)
                                            address7=serZ.read(13).decode("utf-8")
                                            na7=address7[11:13]
                                            bc7 = " ".join(format(ord(c), "b") for c in na7)
                                            bin7=bc7[13]
                                            if  bin7 == "1":    ### Y道至轉盤(600) ###
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
    #                                                                 os.remove("./run/s6B.run")
    # os.remove("./run/s6.run")
    # open("./done/s6.done", 'w').close()
    
if __name__ == "__main__":
    main()