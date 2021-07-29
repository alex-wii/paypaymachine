import serial
from time import sleep
# from setting import tdic1,tdic2
import json
import time
import os
import sys
from AllConfig import J2,J3,J17,J33,J34,Track
from pca9675 import PCA9675I2C

pcaR=PCA9675I2C(address=0x27,busnum=1)
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
pca.output(J33.pin2,1)  ### 落冰推桿  ###
pca.output(J33.pin4,1)  ### 冰電磁閥    ###


track=sys.argv[1]
ice=sys.argv[2]
opentime=int(ice)


def main():
    usbpath =''
    with open("/home/pi/paypaymachine/TrackUsb.json", 'r') as obj1:
        usbpath = json.load(obj1)
    if os.path.isfile("/home/pi/paypaymachine/run/s0.run"):
            sys.exit(1)
    open("/home/pi/paypaymachine/run/s0.run", 'w').close()
    p1=usbpath[Track.ATrainID] ###  W2  ###
    p2=usbpath[Track.BTrainID]     ###  W4  ###
    with serial.Serial(p1, 57600) as ser:
        if track == "A":
            if os.path.isfile("/home/pi/paypaymachine/run/s0B.run"):
                sys.exit(1)
            open("/home/pi/paypaymachine/run/s0A.run", 'w').close()
            if pcaR.input(J3.pin2) != 0 :       ### A道第一管有杯子先用第一管 ###
                ser.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
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
                while pcaR.input(J3.pin8) != 0 :
                    sys.exit(1) ###A道已經有杯子###
                while pcaR.input(J3.pin8) == 0 :
                    if pcaR.input(J3.pin2) != 0 :
                        pca.output(J17.pin2,0)      ### 捲杯器動作 ###
                        time.sleep(0.1)
                        pca.output(J33.pin2,1)      ### 推桿到A ###
                        while True:
                            if pcaR.input(J3.pin8) != 0 :
                                pca.output(J17.pin2,1)  ### 關閉落杯器  ###
                                break
                        time.sleep(1)
                        ser.write(bytes(Track.PositionIce + "\r\n" , "utf-8"))
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
                        time.sleep(1)
                        pca.output(J33.pin4,0)  ###電磁閥開啟###
                        time.sleep(opentime)   ###0,3,6,9###
                        pca.output(J33.pin4,1)  ###電磁閥關閉###
                        time.sleep(5)
                        print("A1做完囉")
                        os.remove("/home/pi/paypaymachine/run/s0A.run")
            if pcaR.input(J3.pin2) == 0 :
                ser.write(bytes(Track.PositionCup2 + "\r\n" , "utf-8"))
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
                if pcaR.input(J3.pin5) != 0 :   
                    pca.output(J17.pin4,0)      ### 捲杯器動作 ###
                    time.sleep(0.1)
                    pca.output(J33.pin2,1)      ### 推桿到A ###
                    while True:
                        if pcaR.input(J3.pin8) != 0 :
                            pca.output(J17.pin4,1)  ### 關閉落杯器 ###
                            break
                    time.sleep(1)
                    ser.write(bytes(Track.PositionIce + "\r\n" , "utf-8"))
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
                    time.sleep(1)
                    pca.output(J33.pin4,0)  ###電磁閥開啟###
                    time.sleep(opentime)   ###0,3,6,9###
                    pca.output(J33.pin4,1)  ###電磁閥關閉###
                    time.sleep(5)
                    print("A2做完囉")
                    os.remove("/home/pi/paypaymachine/run/s0A.run")
    with serial.Serial(p2, 57600) as ser2:
        if track == "B":
            if os.path.isfile("/home/pi/paypaymachine/run/s0A.run"):
                sys.exit(1)
            open("/home/pi/paypaymachine/run/s0B.run", 'w').close()
            if pcaR.input(J2.pin2) != 0 :   ### B道第一管有杯子先用第一管 ###
                ser2.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
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
                while pcaR.input(J2.pin8) != 0 :
                    sys.exit(1) ###B道已經有杯子###
                while pcaR.input(J2.pin8) == 0 :
                    if pcaR.input(J2.pin2) != 0 :  
                        pca.output(J17.pin6,0)    ### 捲杯器動作 ###
                        time.sleep(0.1)
                        pca.output(J33.pin2,0)      ### 推桿到B ###
                        while True:
                            if pcaR.input(J2.pin8) != 0 :
                                pca.output(J17.pin6,1)  ### 關閉落杯器 ###
                                break
                        time.sleep(1)
                        ser2.write(bytes(Track.PositionIce + "\r\n" , "utf-8"))
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
                        time.sleep(1)
                        pca.output(J33.pin4,0)  ###電磁閥開啟###
                        time.sleep(opentime)   ###0,3,6,9###
                        pca.output(J33.pin4,1)  ###電磁閥關閉###
                        time.sleep(5)
                        print("B1做完囉")
                        os.remove("/home/pi/paypaymachine/run/s0B.run")
            if pcaR.input(J2.pin2) == 0 :
                ser2.write(bytes(Track.PositionCup2 + "\r\n" , "utf-8"))
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
                if pcaR.input(J2.pin5) != 0 :   
                    pca.output(J17.pin8,0)      ### 捲杯器動作 ###
                    time.sleep(0.1)
                    pca.output(J33.pin2,0)      ### 推桿到A ###
                    while True:
                        if pcaR.input(J2.pin8) != 0 :
                            pca.output(J17.pin8,1)  ### 關閉落杯器 ###
                            break
                    time.sleep(1)
                    ser2.write(bytes(Track.PositionIce + "\r\n" , "utf-8"))
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
                    time.sleep(1)
                    pca.output(J33.pin4,0)  ###電磁閥開啟###
                    time.sleep(opentime)   ###0,3,6,9###
                    pca.output(J33.pin4,1)  ###電磁閥關閉###
                    time.sleep(5)
                    print("B2做完囉")
                    os.remove("/home/pi/paypaymachine/run/s0B.run")
    time.sleep(1)
    os.remove("/home/pi/paypaymachine/run/s0.run")
    open("/home/pi/paypaymachine/done/s0.done", 'w').close()
    
if __name__ == "__main__":
    main()