#!/usr/bin/python3
import multiprocessing as mp
import serial
from time import sleep
import time
from jsonrpcserver import method,serve
import Adafruit_GPIO as GPIO
import pigpio
import os
import sys
import random
import subprocess
import shutil
from alexloger import *
from paypayorder import PayPayOrder
from PayPayCupOrder import PayPayCupOrder,pay_pay_cup_order_from_dict
import json
#import tkinter as tk ## 顯示視窗測試 ##
from AllConfig import J2,J3,J17,PCA9535J17,J33,PCA9535J33,J34,PCA9535J34,Track
from pca9675 import PCA9675I2C
from pca9535 import PCA9535I2C
from test_api import sendAPItoken

IN = GPIO.IN
OUT = GPIO.OUT
HIGH = GPIO.HIGH
LOW = GPIO.LOW

pcaW11=PCA9675I2C(address=0x11,busnum=1)
pcaW11_Data = 0xFFFF
pcaW15=PCA9675I2C(address=0x15,busnum=1)
pcaW15_Data = 0xFFFF
#pcaW18=PCA9675I2C(address=0x18,busnum=1)
#pcaW18_Data = 0xFFFF
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

pcaW21=PCA9535I2C(address=0x21,busnum=1)
##pcaW22=PCA9535I2C(address=0x22,busnum=1)
##pcaW24=PCA9535I2C(address=0x24,busnum=1)

#config and init
### 冰塊推桿到B ### 防卡冰?
pcaW21.config(PCA9535J33.pin2,OUT)
pcaW21.output(PCA9535J33.pin2,LOW)
### 出杯轉盤停轉   ###
pcaW21.config(PCA9535J34.pin4,OUT)
pcaW21.output(PCA9535J34.pin4,LOW)
### 出杯轉盤方向    ###
pcaW21.config(PCA9535J34.pin2,OUT)
pcaW21.output(PCA9535J34.pin2,LOW)
### 爪夾 ###開爪
pcaW21.config(PCA9535J34.pin9,OUT)
pcaW21.output(PCA9535J34.pin9,HIGH)
##time.sleep(2)
###給冰電磁閥關閉###
pcaW21.config(PCA9535J33.pin4,OUT)
pcaW21.output(PCA9535J33.pin4,HIGH)
### A道第一管落杯器關閉  ###
pcaW21.config(PCA9535J17.pin2,OUT)
pcaW21.output(PCA9535J17.pin2,HIGH)
### A道第二管落杯器關閉  ###
pcaW21.config(PCA9535J17.pin4,OUT)
pcaW21.output(PCA9535J17.pin4,HIGH)
### B道第一管落杯器關閉  ###
pcaW21.config(PCA9535J17.pin6,OUT)
pcaW21.output(PCA9535J17.pin6,HIGH)
### B道第二管落杯器關閉  ###
pcaW21.config(PCA9535J17.pin8,OUT)
pcaW21.output(PCA9535J17.pin8,HIGH)

PWM_CONTROL_PIN = 13
PWM_FREQ = 10000
pi = pigpio.pi()
pi.hardware_PWM(PWM_CONTROL_PIN, PWM_FREQ, 90000)

usbpath =''
with open("/home/pi/paypaymachine/TrackUsb.json", 'r') as obj1:
        usbpath = json.load(obj1)
with open("/home/pi/paypaymachine/PrinterUsb.json", "r") as obj1:
        Printer = json.load(obj1)
fa = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
fa.write("NoRun")
fa.close()
fb = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
fb.write("NoRun")
fb.close()

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

## 熱感印表機設定
serP.write(b"^Q25,3\r")
serP.write(b"^W35\r")
serP.write(b"^H8\r")
serP.write(b"^P1\r")
serP.write(b"^S3\r")
serP.write(b"^AD\r")
serP.write(b"^C1\r")
serP.write(b"^R0\r")
serP.write(b"~Q+0\r")
serP.write(b"^O0\r")
serP.write(b"^D1\r")
serP.write(b"^E28\r")
serP.write(b"~R255\r")

iocontrolsleep = 0.5
CleanTimecount = 0

#def WindosDisplay(): ## 顯示視窗測試 ##
#    window = tk.Tk()
#    window.title('已收單')
#    window.geometry('1080x760+0+0')
#    lbl_1 = tk.Label(window, text=f'飲料 正在出杯', bg='yellow', fg='#263238', font=('Arial', 80))
#   lbl_1.grid(column=0, row=0)
#    window.attributes('-topmost', 1)
#    # window.attributes('-topmost', 0)
#   window.after(20000, lambda: window.destroy()) # Destroy the widget after 30 seconds
#   window.mainloop()

def CheckTrainA_Cup():
    if pcaR27.input(J3.pin2) == 0 : ### A道第一管沒杯子###
        if pcaR27.input(J3.pin5) == 0 : ### A道第二管沒杯子###
            return True
    return False
def CheckTrainB_Cup():
    if pcaR27.input(J2.pin2) == 0 : ### B道第一管沒杯子###
        if pcaR27.input(J2.pin5) == 0 : ### B道第二管沒杯子###
            return True
    return False

def AutoClean(modenum):
    global pcaW2c_Data
    global pcaW28_Data
    global pcaW2a_Data
    global CleanTimecount

    CleanTimecount += 1
    ##print(CleanTimecount)
    if modenum == "reset":
       CleanTimecount = 0
       return True
    if modenum == "manual":
       CleanTimecount = 2400
    if CleanTimecount == 2400:
       CleanTimecount = 0
    else:
       return False
    
    f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'r')
    BRunstate = f.read()
    f.close()
    if BRunstate != "NoRun":
        CleanTimecount = 0
        return False
    
    f = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
    f.write('Clean')
    f.close()
    ##f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
    ##f.write('Clean')
    ##f.close()

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    hour_time = time.strftime("%H", t)
    hour_time_int = int(hour_time)
    print(hour_time)
    print('== 定時清潔啟動 ==')
    ## 攪動冰塊 ##
    pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ###
    time.sleep(1)
    pcaW21.output(PCA9535J33.pin4,LOW) ###給冰電磁閥開啟###
    time.sleep(1)
    pcaW21.output(PCA9535J33.pin4,HIGH) ###給冰電磁閥關閉###
    time.sleep(1)
    ## 牛奶清潔 A道##    
    time.sleep(1)
    pcaW2c_Data=pcaW2c.output(J34.pin7,0,pcaW2c_Data) 
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin7,0,pcaW28_Data)
    time.sleep(8)
    pcaW28_Data=pcaW28.output(J34.pin7,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2c_Data=pcaW2c.output(J34.pin7,1,pcaW2c_Data)
    time.sleep(3)
    ## 牛奶清潔 B道## 
    pcaW2a_Data=pcaW2a.output(J34.pin7,0,pcaW2a_Data) 
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin7,0,pcaW28_Data)
    time.sleep(5)
    pcaW28_Data=pcaW28.output(J34.pin7,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2a_Data=pcaW2a.output(J34.pin7,1,pcaW2a_Data)
    time.sleep(1)
    ##==============================================
    if hour_time_int >= 1 and hour_time_int < 10:
        print('== 時間範圍內不清茶 ==')
        f = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
        f.write('NoRun')
        f.close()
        f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
        f.write('NoRun')
        f.close()
        print('== 定時清潔結束 ==')
        return True
       
    ##==============================================
    ## 茶液清潔 紅茶 ## AS4-1
    pcaW2c_Data=pcaW2c.output(J34.pin4,0,pcaW2c_Data)
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin4,0,pcaW28_Data)
    if hour_time == "07":##早7:00總清排
        print('== 總清排 AS4-1 ==')
        time.sleep(40)
    time.sleep(7)
    pcaW28_Data=pcaW28.output(J34.pin4,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2c_Data=pcaW2c.output(J34.pin4,1,pcaW2c_Data)
    time.sleep(1)
    ## 茶液清潔 紅茶 ## BS4-1
    pcaW2a_Data=pcaW2a.output(J34.pin4,0,pcaW2a_Data)
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin4,0,pcaW28_Data)
    if hour_time == "07": ##早7:00總清排
        print('== 總清排 AS4-1 ==')
        time.sleep(40)
    time.sleep(5)
    pcaW28_Data=pcaW28.output(J34.pin4,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2a_Data=pcaW2a.output(J34.pin4,1,pcaW2a_Data)
    time.sleep(1)
    ##===============================================
    ## 茶液清潔 青茶 ## AS4-4
    pcaW2c_Data=pcaW2c.output(J34.pin2,0,pcaW2c_Data)
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin2,0,pcaW28_Data)
    if hour_time == "07":##早7:00總清排
        print('== 總清排 AS4-4 ==')
        time.sleep(40)
    time.sleep(7)
    pcaW28_Data=pcaW28.output(J34.pin2,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2c_Data=pcaW2c.output(J34.pin2,1,pcaW2c_Data)
    time.sleep(1)
    ## 茶液清潔 青茶 ## BS4-4
    pcaW2a_Data=pcaW2a.output(J34.pin2,0,pcaW2a_Data)
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin2,0,pcaW28_Data)
    if hour_time == "07":##早7:00總清排
        print('== 總清排 AS4-4 ==')
        time.sleep(40)
    time.sleep(5)
    pcaW28_Data=pcaW28.output(J34.pin2,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2a_Data=pcaW2a.output(J34.pin2,1,pcaW2a_Data)
    ##===============================================
    ## 茶液清潔 特殊茶 ## AS5-3
    pcaW2c_Data=pcaW2c.output(J34.pin6,0,pcaW2c_Data)
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin6,0,pcaW28_Data)
    if hour_time == "07":##早7:00總清排
        print('== 總清排 AS5-3 ==')
        time.sleep(40)
    time.sleep(7)
    pcaW28_Data=pcaW28.output(J34.pin6,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2c_Data=pcaW2c.output(J34.pin6,1,pcaW2c_Data)
    time.sleep(1)
    ## 茶液清潔 特殊茶 ## BS5-3
    pcaW2a_Data=pcaW2a.output(J34.pin6,0,pcaW2a_Data)
    time.sleep(0.5)
    pcaW28_Data=pcaW28.output(J34.pin6,0,pcaW28_Data)
    if hour_time == "07":##早7:00總清排
        print('== 總清排 AS5-3 ==')
        time.sleep(40)
    time.sleep(5)
    pcaW28_Data=pcaW28.output(J34.pin6,1,pcaW28_Data)
    time.sleep(0.5)
    pcaW2a_Data=pcaW2a.output(J34.pin6,1,pcaW2a_Data)
    time.sleep(2)
    
    ##先讓B道製作飲料，所以先把A道設定成noRun
    f = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
    f.write('NoRun')
    f.close()
    print('== 定時清潔結束 ==')
    time.sleep(2) ## A道多等一些時間
    ##f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
    ##f.write('NoRun')
    ##f.close()
    return True
    

def StationA_S0(track,opentimeStr):
    opentime=int(opentimeStr)
    print('S0 Start')
    if track == "A":
        if pcaR27.input(J3.pin2) != 0 : ### A道第1管有杯子###
            if pcaR27.input(J3.pin5) != 0 : ### A道第2管也有杯子###
                SelCupA = random.randint(1,10)
                print('A:randint cup ' f'{SelCupA}')
            else:
                SelCupA = 1 ### A道第2管沒有杯子，所以直接用第1管###
                print('A:指定1管: ' f'{SelCupA}')
        else:
            SelCupA = 9 ### A道第1管沒有杯子，所以直接用第2管###
            print('A:指定2管: ' f'{SelCupA}')

        if SelCupA < 7: ##pcaR27.input(J3.pin2) != 0 :       ### A道第一管有杯子先用第一管 ###
            serA.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
            while True: ## 等待A軌道到位信號 ##
                serA.flushInput() 
                serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=serA.read(13).decode("utf-8")
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
            pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ### 防卡冰?
            time.sleep(0.5)
            pcaW21.output(PCA9535J33.pin2,HIGH) ### 冰塊推桿到A ###
            if pcaR27.input(J3.pin8) == 0 : ## A道杯架沒有杯子 ##
                pcaW21.output(PCA9535J17.pin2,LOW) ### A道第一管落杯器動作 ###
                time.sleep(0.1)
                ## pcaW21.output(PCA9535J33.pin2,HIGH) ### 冰塊推桿到A ###
                while True: ## 等待杯子落下
                    if pcaR27.input(J3.pin8) != 0 :
                        pcaW21.output(PCA9535J17.pin2,HIGH)  ### A道第一管落杯器關閉  ###
                        break
        elif SelCupA > 6: ##pcaR27.input(J3.pin5) != 0 : ### A道第二管有杯子 ###
            serA.write(bytes(Track.PositionCup2 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
            while True: ## 等待A軌道到位信號 ##
                serA.flushInput() 
                serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=serA.read(13).decode("utf-8")
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
            pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ### 防卡冰?
            time.sleep(0.5)
            pcaW21.output(PCA9535J33.pin2,HIGH) ### 冰塊推桿到A ###
            if pcaR27.input(J3.pin8) == 0 : ## A道杯架沒有杯子 ##
                pcaW21.output(PCA9535J17.pin4,LOW) ### A道第二管落杯器動作 ###
                time.sleep(0.1)
                ## pcaW21.output(PCA9535J33.pin2,HIGH) ### 冰塊推桿到A ###
                while True: ## 等待杯子落下
                    if pcaR27.input(J3.pin8) != 0 :
                        pcaW21.output(PCA9535J17.pin4,HIGH)  ### A道第二管落杯器關閉  ###
                        break
        time.sleep(1)
        serA.write(bytes(Track.PositionIce + "\r\n" , "utf-8")) ## 移動到A道落冰處 ##
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        
        if opentime > 0:
            pcaW21.output(PCA9535J33.pin4,LOW) ###給冰電磁閥開啟###
            for i in range(opentime): #Evan 點放出冰
                time.sleep(0.3)
                pcaW21.output(PCA9535J33.pin4,LOW) ###給冰電磁閥開啟###
                pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ### 防卡冰?
                time.sleep(0.3)
                pcaW21.output(PCA9535J33.pin2,HIGH) ### 冰塊推桿到A ### 防卡冰?
                pcaW21.output(PCA9535J33.pin4,HIGH) ###給冰電磁閥關閉###
            time.sleep(3) ## 等待冰塊滑落 ##
        print("S0A道做完囉")
    elif track == "B":
        if  pcaR27.input(J2.pin2) != 0 : ### B道第1管有杯子###
            if pcaR27.input(J2.pin5) != 0 : ### B道第2管也有杯子###
                SelCupB = random.randint(1,10)
                print('B:randint cup ' f'{SelCupB}')
            else:
                SelCupB = 1 ### B道第2管沒有杯子，所以直接用第1管###
                print('B:指定1管: ' f'{SelCupB}')
        else:
            SelCupB = 9 ### B道第1管沒有杯子，所以直接用第2管###
            print('B:指定2管: ' f'{SelCupB}')

        if SelCupB < 7: ##pcaR27.input(J2.pin2) != 0 : ### B道第一管有杯子先用第一管 ###
            serB.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
            while True: ## 等待B軌道到位信號 ##
                serB.flushInput() 
                serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=serB.read(13).decode("utf-8")
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
            pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ###
            if pcaR27.input(J2.pin8) == 0 : ## B道杯架沒有杯子 ##
                pcaW21.output(PCA9535J17.pin6,LOW) ### B道第一管落杯器動作 ###
                time.sleep(0.1)
                ## pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ###
                while True: ## 等待杯子落下
                    if pcaR27.input(J2.pin8) != 0 :
                        pcaW21.output(PCA9535J17.pin6,HIGH)  ### B道第一管落杯器關閉  ###
                        break
        elif SelCupB > 6: ##pcaR27.input(J2.pin5) != 0 : ### B道第二管有杯子 ###
            serB.write(bytes(Track.PositionCup2 + "\r\n" , "utf-8"))
            time.sleep(0.1) 
            serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
            while True: ## 等待A軌道到位信號 ##
                serB.flushInput() 
                serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
                time.sleep(0.1)
                address=serB.read(13).decode("utf-8")
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
            pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ###
            if pcaR27.input(J2.pin8) == 0 : ## B道杯架沒有杯子 ##
                pcaW21.output(PCA9535J17.pin8,LOW) ### B道第二管落杯器動作 ###
                time.sleep(0.1)
                ## pcaW21.output(PCA9535J33.pin2,LOW) ### 冰塊推桿到B ###
                while True: ## 等待杯子落下
                    if pcaR27.input(J2.pin8) != 0 :
                        pcaW21.output(PCA9535J17.pin8,HIGH)  ### B道第二管落杯器關閉  ###
                        break
        time.sleep(1)
        serB.write(bytes(Track.PositionIce + "\r\n" , "utf-8")) ## 移動到B道落冰處 ##
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        if opentime > 0:
            pcaW21.output(PCA9535J33.pin4,LOW) ###給冰電磁閥開啟###
            for i in range(opentime): #Evan 點放出冰
                time.sleep(0.3)
                pcaW21.output(PCA9535J33.pin4,LOW) ###給冰電磁閥開啟###
                time.sleep(0.3)
                pcaW21.output(PCA9535J33.pin4,HIGH) ###給冰電磁閥關閉###
            time.sleep(3) ## 等待冰塊滑落 ##
        print("S0B道做完囉")
    print('S0 END')    
def StationB_S1_Atrain(time1,time2,time3,time4,time5):
    global pcaW1c_Data
    global pcaW15_Data
    global pcaW11_Data
    pump = pcaW15
    doorA = pcaW1c
    print('AS1 Start')
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

def StationB_S1_Btrain(time1,time2,time3,time4,time5):
    global pcaW1c_Data
    global pcaW15_Data
    global pcaW11_Data
    pump = pcaW15
    doorB = pcaW11
    print('BS1 Start')
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

def StationB_S1(track,timedata):
    time1=int(timedata[2:4])
    time2=int(timedata[6:8])
    time3=int(timedata[10:12])
    time4=int(timedata[14:16])
    time5=int(timedata[18:20])
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        return True
    if track == "A":
        serA.write(bytes(Track.PositionS1 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        StationB_S1_Atrain(time1,time2,time3,time4,time5)
    elif track == "B":
        serB.write(bytes(Track.PositionS1 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        StationB_S1_Btrain(time1,time2,time3,time4,time5)
    time.sleep(4)

def StationC_S2_Atrain(time1,time2,time3,time4,time5):
    global pcaW1c_Data
    global pcaW15_Data
    pump = pcaW15
    doorA = pcaW1c
    print('AS2 Start')
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

def StationC_S2_Btrain(time1,time2,time3,time4,time5):
    global pcaW15_Data
    global pcaW11_Data
    pump = pcaW15
    doorB = pcaW11
    print('BS2 Start')
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

def StationC_S2(track,timedata):
    time1=int(timedata[2:4])
    time2=int(timedata[6:8])
    time3=int(timedata[10:12])
    time4=int(timedata[14:16])
    time5=int(timedata[18:20])
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        return True
    if track == "A":
        serA.write(bytes(Track.PositionS2 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        StationC_S2_Atrain(time1,time2,time3,time4,time5)
    elif track == "B":
        serB.write(bytes(Track.PositionS2 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        StationC_S2_Btrain(time1,time2,time3,time4,time5)
    time.sleep(4)
def StationD_S3_Atrain(time1,time2,time3,time4,time5): 
    global pcaW15_Data
    global pcaW1c_Data
    global pcaW28_Data
    global pcaW2c_Data
    pump = pcaW15
    doorA = pcaW1c
    pump1 = pcaW28
    doorA1 = pcaW2c
    print('AS3 Start')
    if time1 !=0 :
        time.sleep(iocontrolsleep)
        pcaW1c_Data=doorA.output(J34.pin6,0,pcaW1c_Data)
        time.sleep(iocontrolsleep)
        pcaW15_Data=pump.output(J34.pin6,0,pcaW15_Data)
        time.sleep(time1)
        pcaW15_Data=pump.output(J34.pin6,1,pcaW15_Data)
        time.sleep(iocontrolsleep)
        pcaW1c_Data=doorA.output(J34.pin6,1,pcaW1c_Data)
    if time2 !=0 : ### 鮮奶  ###
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
        pcaW1c_Data=doorA.output(J34.pin7,0,pcaW1c_Data)
        time.sleep(iocontrolsleep)
        pcaW15_Data=pump.output(J34.pin7,0,pcaW15_Data)
        time.sleep(time3)
        pcaW15_Data=pump.output(J34.pin7,1,pcaW15_Data)
        time.sleep(iocontrolsleep)
        pcaW1c_Data=doorA.output(J34.pin7,1,pcaW1c_Data)
    if time4 !=0 :      ### 甜度糖_蔗糖_寡糖  ###
        time.sleep(iocontrolsleep)
        pcaW2c_Data=doorA1.output(J34.pin9,0,pcaW2c_Data)
        time.sleep(iocontrolsleep)
        pcaW28_Data=pump1.output(J34.pin9,0,pcaW28_Data)
        time.sleep(time4)
        pcaW28_Data=pump1.output(J34.pin9,1,pcaW28_Data)
        time.sleep(iocontrolsleep)
        pcaW2c_Data=doorA1.output(J34.pin9,1,pcaW2c_Data)
        time.sleep(2)
    #if time5 !=0 :
    #time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin4,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin4,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin4,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorA.output(J33.pin4,1)
def StationD_S3_Btrain(time1,time2,time3,time4,time5):
    global pcaW15_Data
    global pcaW11_Data
    global pcaW28_Data
    global pcaW2a_Data
    pump = pcaW15
    doorB = pcaW11
    pump1 = pcaW28
    doorB1 = pcaW2a
    print('BS3 Start')
    if time1 !=0 :
        time.sleep(iocontrolsleep)
        pcaW11_Data=doorB.output(J34.pin6,0,pcaW11_Data)
        time.sleep(iocontrolsleep)
        pcaW15_Data=pump.output(J34.pin6,0,pcaW15_Data)
        time.sleep(time1)
        pcaW15_Data=pump.output(J34.pin6,1,pcaW15_Data)
        time.sleep(iocontrolsleep)
        pcaW11_Data=doorB.output(J34.pin6,1,pcaW11_Data)
    if time2 !=0 :  ### 鮮奶  ###
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
        pcaW11_Data=doorB.output(J34.pin7,0,pcaW11_Data)
        time.sleep(iocontrolsleep)
        pcaW15_Data=pump.output(J34.pin7,0,pcaW15_Data)
        time.sleep(time3)
        pcaW15_Data=pump.output(J34.pin7,1,pcaW15_Data)
        time.sleep(iocontrolsleep)
        pcaW11_Data=doorB.output(J34.pin7,1,pcaW11_Data)
    if time4 !=0 :      ### 甜度糖_蔗糖_寡糖  ###
        time.sleep(iocontrolsleep)
        pcaW2a_Data=doorB1.output(J34.pin9,0,pcaW2a_Data)
        time.sleep(iocontrolsleep)
        pcaW28_Data=pump1.output(J34.pin9,0,pcaW28_Data)
        time.sleep(time4)
        pcaW28_Data=pump1.output(J34.pin9,1,pcaW28_Data)
        time.sleep(iocontrolsleep)
        pcaW2a_Data=doorB1.output(J34.pin9,1,pcaW2a_Data)
        time.sleep(2)
    # if time5 !=0 :
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin4,0)  
    #     time.sleep(iocontrolsleep)
    #     teapump.output(J17.pin4,0)
    #     time.sleep(time5)
        # teapump.output(J17.pin4,1)
    #     time.sleep(iocontrolsleep)
    #     teadoorB.output(J34.pin4,1)
def StationD_S3(track,timedata):
    time1=int(timedata[2:4])
    time2=int(timedata[6:8])
    time3=int(timedata[10:12])
    time4=int(timedata[14:16])
    time5=int(timedata[18:20])
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        return True
    if track == "A":
        serA.write(bytes(Track.PositionS3 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        StationD_S3_Atrain(time1,time2,time3,time4,time5)
    elif track == "B":
        serB.write(bytes(Track.PositionS3 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        StationD_S3_Btrain(time1,time2,time3,time4,time5)
    time.sleep(2)
def StationE_S4_Atrain(time1,time2,time3,time4,time5):
    global pcaW28_Data
    global pcaW2c_Data
    pump = pcaW28
    doorA = pcaW2c
    print('AS4 Start')
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

def StationE_S4_Btrain(time1,time2,time3,time4,time5):
    global pcaW28_Data
    global pcaW2a_Data
    pump = pcaW28
    doorB = pcaW2a
    print('BS4 Start')
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
def StationE_S4(track,timedata):
    time1=int(timedata[2:4])
    time2=int(timedata[6:8])
    time3=int(timedata[10:12])
    time4=int(timedata[14:16])
    time5=int(timedata[18:20])
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        return True
    if track == "A":
        serA.write(bytes(Track.PositionS4 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        StationE_S4_Atrain(time1,time2,time3,time4,time5)
    elif track == "B":
        serB.write(bytes(Track.PositionS4 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        StationE_S4_Btrain(time1,time2,time3,time4,time5)
    time.sleep(4)
def StationF_S5_Atrain(time1,time2,time3,time4,time5): 
    global pcaW28_Data
    global pcaW2c_Data
    pump = pcaW28
    doorA = pcaW2c
    print('AS5 Start')
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
    if time4 !=0 : ## 純淨水 ##
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

def StationF_S5_Btrain(time1,time2,time3,time4,time5):
    global pcaW28_Data
    global pcaW2a_Data
    pump = pcaW28
    doorB = pcaW2a
    print('BS5 Start')
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
    if time4 !=0 : ## 純淨水 ##
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
def StationF_S5(track,timedata,iceSec):
    time1=int(timedata[2:4])
    time2=int(timedata[6:8])
    time3=int(timedata[10:12])
    time4=int(timedata[14:16])
    time5=int(timedata[18:20])
    
    if iceSec == "01":
        print('=== 冰塊水量調節01')
        time4 += 4
    elif iceSec == "02":
        print('=== 冰塊水量調節02')
        time4 += 4
    elif iceSec == "03":
        print('=== 冰塊水量調節03')
        time4 += 3
    elif iceSec == "04":
        print('=== 冰塊水量調節04')
        time4 += 2
    elif iceSec == "05":
        print('=== 冰塊水量調節05')
        time4 += 1
    elif iceSec == "06":
        print('=== 冰塊水量調節06')
        time4 += 0
        
    if time1 == 0 and time2 == 0 and time3 == 0 and time4 == 0 and time5 == 0:
        return True
    if track == "A":
        serA.write(bytes(Track.PositionS5 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        StationF_S5_Atrain(time1,time2,time3,time4,time5)
    elif track == "B":
        serB.write(bytes(Track.PositionS5 + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        StationF_S5_Btrain(time1,time2,time3,time4,time5)

def StationEnd_S6(track,ordernumber):
    print('S6 Start')
    ##asciinum = [] 
    ##for e in ordernumber:
    ##    asciinum.append(ord(e))

    ##if ordernumber[0].isupper() :
    ##    testcode= 77
    ##    a0=asciinum[0]-65
    ##    a1=asciinum[1]-48
    ##    a2=asciinum[2]-48
    ##    a3=asciinum[3]-48
    ##    a4=asciinum[4]-48
    ##    a5=asciinum[5]-48
    ##    a6=asciinum[6]-48
        ##Verificationcode=testcode+a1+a2+a3+a4+a5
    ##    Verificationcode=testcode+a0+a2+a3+a5+a6
    ##else:
    ##    testcode= 109
    ##    a0=asciinum[0]-97
    ##    a1=asciinum[1]-48
    ##    a2=asciinum[2]-48
    ##    a3=asciinum[3]-48
    ##    a4=asciinum[4]-48
    ##    a5=asciinum[5]-48
    ##    a6=asciinum[6]-48
        ##Verificationcode=testcode+a1+a2+a3+a4+a5
    ##    Verificationcode=testcode+a0+a2+a3+a5+a6
    ##============= Print stop ====================== ====================
    ##serP.write([2,0,6,1,70,0,0,0,0,77,3])
    ##icount = 1
    ##while True:
    ##    PrtReturnValue=serP.read(1).decode("Ascii")
    ##    print(PrtReturnValue)
    ##    time.sleep(0.1)
    ##    icount += 1
    ##    if PrtReturnValue == "O":
    ##        break
    ##    if icount >= 20:
    ##        break 
    ## Print == 訂單編號 ======================
    ##serP.write([2,0,9,0,61,1,5,asciinum[5],asciinum[6],asciinum[3],asciinum[2],asciinum[0],Verificationcode,3])
    ##icount = 1
    ##while True:
    ##    PrtReturnValue=serP.read(1).decode("Ascii")
    ##    print(PrtReturnValue)
    ##    time.sleep(0.1)
    ##    icount += 1
    ##    if PrtReturnValue == "O":
    ##        break
    ##    if icount >= 20:
    ##        break
    #print out
    ##serP.write([2,0,6,1,70,4,0,0,0,81,3])
    ##icount = 1
    ##while True:
    ##    PrtReturnValue=serP.read(1).decode("Ascii")
    ##    print(PrtReturnValue)
    ##    time.sleep(0.1)
    ##    icount += 1
    ##    if PrtReturnValue == "O":
    ##        break
    ##    if icount >= 20:
    ##        break
    ##===================================================================
    pcaW21.output(PCA9535J34.pin9,HIGH) ## 爪夾開啟 ##
    if track == "A":
        serA.write(bytes(Track.PositionEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serA.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待A軌道到位信號 ##
            serA.flushInput() 
            serA.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serA.read(13).decode("utf-8")
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
        time.sleep(0.1)
        serY.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 50%speed    ###
        time.sleep(0.1) 
        serY.write(bytes(Track.YTrackA + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待Y軌道到位信號 ##
            serY.flushInput() 
            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serY.read(13).decode("utf-8")
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
    elif track == "B":
        serB.write(bytes(Track.PositionEnd + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serB.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待B軌道到位信號 ##
            serB.flushInput() 
            serB.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serB.read(13).decode("utf-8")
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
        time.sleep(0.1)
        serY.write(bytes(Track.YSpeed + "\r\n" , "utf-8"))      ### 50%speed    ###
        time.sleep(0.1) 
        serY.write(bytes(Track.YTrackB + "\r\n" , "utf-8"))
        time.sleep(0.1) 
        serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
        while True: ## 等待Y軌道到位信號 ##
            serY.flushInput() 
            serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
            time.sleep(0.1)
            address=serY.read(13).decode("utf-8")
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
    else:
        return False    
    time.sleep(0.1)
    serZ.write(bytes(Track.ZTrackDown + "\r\n" , "utf-8"))
    time.sleep(0.1) 
    serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
    while True:  ## 等待Z軌道到位信號 ##
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
    pcaW21.output(PCA9535J34.pin9,LOW) ## 爪夾閉合 ##
    time.sleep(1)
    serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8")) ## 夾杯後升起 Z軌 ##
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
            if  bin2 == "1": 
                break
    time.sleep(0.1)
    if track == "A":
        serTemp=serA
    elif track == "B":
        serTemp=serB
    else:
        print('S6,AB軌道不明確')
        return False
    ## 讓AorB道回到S0 原點    
    serTemp.write(bytes(Track.PositionStart + "\r\n" , "utf-8"))
    time.sleep(0.1)
    serTemp.write(bytes(Track.Move + "\r\n" , "utf-8"))

    time.sleep(0.1)
    serY.write(bytes(Track.YTrackCup + "\r\n" , "utf-8")) ## Y軌移動到封膜機位置 ##
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
            if  bin3 == "1":    
                break
    time.sleep(0.1)
    serZ.write(bytes(Track.ZTrackPutCup + "\r\n" , "utf-8")) ### Z道下至封杯位置(197) ###
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
            if  bin4 == "1": 
                break
    time.sleep(0.1)
    pcaW21.output(PCA9535J34.pin9,HIGH) ## 爪夾開啟 ##
    time.sleep(0.1)
    serZ.write(bytes(Track.ZTrackWaitCup + "\r\n" , "utf-8")) ### Z道上至50 ###
    time.sleep(0.1) 
    serZ.write(bytes(Track.Move + "\r\n" , "utf-8"))
    time.sleep(8) ## 等待封膜機 ##
    while True:
        serZ.flushInput() 
        serZ.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
        time.sleep(0.1)
        address5=serZ.read(13).decode("utf-8")
        na5=address5[11:13]
        bc5 = " ".join(format(ord(c), "b") for c in na5)
        if len(bc5) == 15:
            bin5=bc5[13]
            if  bin5 == "1":    
                break
    time.sleep(0.1)
    serZ.write(bytes(Track.ZTrackPutCup + "\r\n" , "utf-8"))### Z道下至封杯位置(197) ###
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
            if  bin6 == "1":    
                break
    time.sleep(0.1)
    pcaW21.output(PCA9535J34.pin9,LOW) ## 爪夾關閉 ##
    time.sleep(1)
    serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8"))### Z道上至0 ###
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
            if  bin7 == "1":    
                break
    time.sleep(0.1)
    serY.write(bytes(Track.YTrackEnd + "\r\n" , "utf-8")) ### Y道至轉盤(600) ###
    time.sleep(0.1) 
    serY.write(bytes(Track.Move + "\r\n" , "utf-8"))

    #if pcaR26.input(J3.pin2) != 0 : ##偵測放杯處有杯子##
    #    #while pcaR26.input(J3.pin5) != 0 :   ##偵測進杯處沒有杯子## 
    #    pcaW21.output(PCA9535J34.pin4,HIGH) ## 轉盤啟動 ##
    #    time.sleep(2.9)   ##一個杯子距離### 
    #    pcaW21.output(PCA9535J34.pin4,LOW) ## 轉盤關閉 ##
    pcaW21.output(PCA9535J34.pin4,HIGH) ## 轉盤啟動 ##
    cupcount = 0
    while True:
        if pcaR26.input(J3.pin5) == 0 :   ###偵測進杯處沒有異物###
            cupcount += 1
        else:
            cupcount = 0
        if cupcount >= 10000 :
            break

    while True: ### Y道至轉盤(600)  確認Y軸到位信號###
        serY.flushInput() 
        serY.write(bytes(Track.CheckSign + "\r\n" , "utf-8"))
        time.sleep(0.1)
        address8=serY.read(13).decode("utf-8")
        na8=address8[11:13]
        bc8 = " ".join(format(ord(c), "b") for c in na8)
        if len(bc8) == 15:
            bin8=bc8[13]
            if  bin8 == "1":    
                break 
    #pcaW21.output(PCA9535J34.pin4,HIGH) ## 轉盤啟動 ##
    #cupcount = 0
    while True:
        if pcaR26.input(J3.pin5) == 0 :   ###偵測進杯處沒有異物###
            cupcount += 1
        else:
            cupcount = 0
        if cupcount >= 3000 :
            break
    pcaW21.output(PCA9535J34.pin4,LOW) ## 轉盤關閉 ##
    
    if pcaR26.input(J3.pin2) == 0 :
        time.sleep(0.1)
        serZ.write(bytes(Track.ZTrackDown + "\r\n" , "utf-8")) ### Z道下至轉盤(250)並張爪 ###
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
                if  bin9 == "1":    
                    break
    if pcaR26.input(J3.pin2) != 0 :
        print('有飲料杯完成了') ## 出杯sensor偵測到杯子##
    else:
        print('奇怪，怎麼沒有杯子呢')
    pcaW21.output(PCA9535J34.pin9,HIGH) ## 爪夾開啟 ##
    time.sleep(1)
    serZ.write(bytes(Track.ZTrackUp + "\r\n" , "utf-8")) ### Z道上至0 ###
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
    serY.write(bytes(Track.YTrackA + "\r\n" , "utf-8")) ## Y軌回到A道上方 ##
    time.sleep(0.1) 
    serY.write(bytes(Track.Move + "\r\n" , "utf-8"))
    time.sleep(0.1)
    pcaW21.output(PCA9535J34.pin4,HIGH) ##轉盤 HIGH啟動,LOW停止  ##
    time.sleep(2)   ### 轉盤轉到印標機位置(須測試)  ###
    ##Printer##
    serP.write(b"^L\r")
    serP.write(b"Dy2-me-dd\r")
    serP.write(b"Th:m:s\r")
    serP.write(b"W22,26,5,2,M0,8,4,28,0\r")
    serP.write(b"https://www.paypaydrink.com\r")
    array2 = bytearray('配配飲', 'big5') 
    serP.write(b"AZ1,154,26,2,2,0,0,")
    serP.write(array2)
    serP.write(b"\r")
    array2 = bytearray('取餐編號:', 'big5')
    serP.write(b"AZ1,18,148,1,2,0,0,")
    serP.write(array2)
    serP.write(b"\r") 
    array2 = bytearray(ordernumber, 'big5')
    serP.write(b"AZ1,92,148,1,2,0,0,")
    serP.write(array2)
    serP.write(b"\r")
    t = time.localtime()
    current_time = time.strftime("%Y/%m/%d,%H:%M:%S", t)
    array2 = bytearray(current_time, 'big5')
    serP.write(b"AZ1,18,180,1,1,0,0,")
    serP.write(array2)
    serP.write(b"\r") 
    array2 = bytearray('祝 您有個美好', 'big5')
    serP.write(b"AZ1,146,70,1,2,0,0,")
    serP.write(array2)
    serP.write(b"\r")
    array2 = bytearray(' 的一天', 'big5')
    serP.write(b"AZ1,146,110,1,2,0,0,")
    serP.write(array2)
    serP.write(b"\r")
    array2 = bytearray('*請搖杯30秒喔*', 'big5')
    serP.write(b"AZ1,150,148,1,2,0,0,")
    serP.write(array2)
    serP.write(b"\r")
    serP.write(b"E\r")
    time.sleep(7)   ### 轉盤轉到客人取杯位置之時間(須測試)  ###
    pcaW21.output(PCA9535J34.pin4,LOW) ##轉盤 HIGH啟動,LOW停止  ##
    if ordernumber != "0999-02":
         sendAPItoken(ordernumber) ## 回報Server完成 ##

def checkSisruning(sta,Runstate):
    print(f'{sta}:{Runstate}')
    if Runstate == "Clean":
        return True
    if sta == Runstate:
        return True 
    if sta == "s0": 
        if Runstate == "s6":
            return True
    if sta == "s1": 
        if Runstate == "s2":
            return True
    if sta == "s1": 
        if Runstate == "s3":
            return True
    if sta == "s2": 
        if Runstate == "s3":
            return True
    if sta == "s3": 
        if Runstate == "s4":
            return True
    if sta == "s3": 
        if Runstate == "s5":
            return True
    if sta == "s4": 
        if Runstate == "s5":
            return True
    return False
    #filename = f'./run/{sta}.run'
    #if os.path.isfile(filename):
    #    return True
    #if sta == "s0": #解決爪夾誤開的問題
    #   if os.path.isfile("/home/pi/paypaymachine/run/s6.run"):
    #      return True
    #if sta == "s6": #解決爪夾誤開的問題
    #   if os.path.isfile("/home/pi/paypaymachine/run/s0.run"):
    #    return True
    #return False
def getS0o(orderTxt):
    print(orderTxt)
def getS1o(orderTxt):
    print(orderTxt)

def processA(bitArray,order,Trainvalue):
    print(f'A: pid={pid()}')
    while True:
        if order.empty():
            logger.info('A empty')
            time.sleep(1)
            AutoClean('all')
            continue
        if CheckTrainA_Cup():
            print('A道完全沒杯子了')
            continue
        o=order.get()
        AutoClean('reset')
        ##f = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
        ##f.write('s0')
        ##f.close()
        #print(o)
        #print(f'{o}')
        #WindosDisplay()
        logger.info(f'A:processA {list(bitArray)},order={o}')
        bitArray[0]=1
        logger.info(f'A:aprocessA-1 {list(bitArray)},order={o}')   
        recp_dic = {"stationa":o.stationa,"stationb":o.stationb,"stationc":o.stationc,"stationd":o.stationd,"statione":o.statione,"stationf":o.stationf,"endpoint":o.cupnum}
        station_dic = {"s0":"stationa","s1":"stationb","s2":"stationc","s3":"stationd","s4":"statione","s5":"stationf","s6":"endpoint"}
        station = ["s0","s1","s2","s3","s4","s5","s6"]

        for sta in station:
            f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'r')
            BRunstate = f.read()
            f.close()
            while checkSisruning(sta,BRunstate) is True:
                logger.info(f'A:{sta} B is running , wait 1 sec for {sta} B')
                print(f'A:{sta} B is running , wait 1 sec for {BRunstate} B')
                f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'r')
                BRunstate = f.read()
                f.close()
                time.sleep(1)
            #print(f'hello-{sta}-{recp_dic[station_dic[sta]]}')
            #logger.info(f'hello-{sta}-{recp_dic[station_dic[sta]]}')   
            if os.uname()[0] == 'Linux' :
                print(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                #p = subprocess.run(['python3',f'{sta}.py',f'A',f'{recp_dic[station_dic[sta]]}'])
                print('A道開始製作飲品')
                f = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
                f.write(f'{sta}')
                f.close()
                if sta == "s0":
                    StationA_S0(f'A',f'{recp_dic[station_dic[sta]]}') 
                elif sta == "s1":
                    StationB_S1(f'A',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s2":
                    StationC_S2(f'A',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s3":
                    StationD_S3(f'A',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s4":
                    StationE_S4(f'A',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s5":
                    StationF_S5(f'A',f'{recp_dic[station_dic[sta]]}',f'{recp_dic[station_dic["s0"]]}')
                elif sta == "s6":
                    StationEnd_S6(f'A',f'{recp_dic[station_dic[sta]]}')
            else:
                sec = random.randint(5,10) 
                logger.info(f'A:do {sta} A {sec} sec')
                print(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                p = subprocess.run(['python3',f'{sta}ta.py',f'A',f'{recp_dic[station_dic[sta]]}',f'{sec}'])
            # p = subprocess.run(['python3','s1.py',f'A',f'{sta}',f'{sec}'])
        f = open("/home/pi/paypaymachine/sysArunstate.txt", 'w')
        f.write("NoRun")
        f.close()
        time.sleep(2)
        print('=== A 道飲品製作完成 === !!')
        bitArray[0]=0
        logger.info(f'A:processA-E {list(bitArray)},order={o}')

def processB(bitArray,order,Trainvalue):
    print(f'B: pid={pid()}')
    while True:
        time.sleep(2)
        if order.empty():
            logger.info('B:B empty')
            time.sleep(1)
            continue
        if CheckTrainB_Cup():
            print('B道完全沒杯子了')
            continue

        o=order.get()
        ##f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
        ##f.write('s0')
        ##f.close()
        #WindosDisplay()
        logger.info(f'B:processB show train AB is available {list(bitArray)},order={o}')
        bitArray[1]=1
        logger.info(f'B:processB-1 set train B{list(bitArray)},order={o}')
        recp_dic = {"stationa":o.stationa,"stationb":o.stationb,"stationc":o.stationc,"stationd":o.stationd,"statione":o.statione,"stationf":o.stationf,"endpoint":o.cupnum}
        station_dic = {"s0":"stationa","s1":"stationb","s2":"stationc","s3":"stationd","s4":"statione","s5":"stationf","s6":"endpoint"}
        station = ["s0","s1","s2","s3","s4","s5","s6"]
        
        for sta in station:
            f = open("/home/pi/paypaymachine/sysArunstate.txt", 'r')
            ARunstate = f.read()
            f.close()
            while checkSisruning(sta,ARunstate) is True:
                logger.info(f'B:{sta} A is running , wait 1 sec for {sta} A')
                print(f'B:{sta} A is running , wait 1 sec for {ARunstate} A')
                f = open("/home/pi/paypaymachine/sysArunstate.txt", 'r')
                ARunstate = f.read()
                f.close()
                time.sleep(1)
            #print(f'hello-{sta}-{recp_dic[station_dic[sta]]}')
            #logger.info(f'hello-{sta}-{recp_dic[station_dic[sta]]}')   
            if os.uname()[0] == 'Linux' :
                #p = subprocess.run(['python3',f'{sta}.py',f'B',f'{recp_dic[station_dic[sta]]}'])
                print(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}') 
                print('B道開始製作飲品')
                f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
                f.write(f'{sta}')
                f.close()
                if sta == "s0":
                    StationA_S0(f'B',f'{recp_dic[station_dic[sta]]}')  
                elif sta == "s1":
                    StationB_S1(f'B',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s2":
                    StationC_S2(f'B',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s3":
                    StationD_S3(f'B',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s4":
                    StationE_S4(f'B',f'{recp_dic[station_dic[sta]]}')
                elif sta == "s5":
                    StationF_S5(f'B',f'{recp_dic[station_dic[sta]]}',f'{recp_dic[station_dic["s0"]]}')
                elif sta == "s6":
                    StationEnd_S6(f'B',f'{recp_dic[station_dic[sta]]}')
            else:
                sec = random.randint(5,10)
                logger.info(f'B:{sta} free do {sta} on B {sec} sec')
                p = subprocess.run(['python3',f'{sta}ta.py',f'B',f'{recp_dic[station_dic[sta]]}',f'{sec}'])
                print(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')         
        f = open("/home/pi/paypaymachine/sysBrunstate.txt", 'w')
        f.write("NoRun")
        f.close()
        time.sleep(2)
        print('=== B 道飲品製作完成 === !!')
        bitArray[1]=0
        logger.info(f'B:processB-End done {list(bitArray)},order={o}')

def jsonrpcserver(q):
    @method
    def jsonrpc_addorder(order):
        print(order)
        # order='{"ordernum":"RSAP21071400002","cupcount":1,"content":[{"cupnum":"A0001","stationa":"02","stationb":"01010200030004000500","stationc":"01010200030004000500","stationd":"01000200030004000503","statione":"01010200030004000500","stationf":"01010200030004000500"}]}'
        # orderjson = json.loads(order)
        # print(orderjson)
        orderobj=PayPayOrder.from_json(order)
        # orderinfo=pay_pay_order_from_dict(order)
        print(orderobj.content)
        for cup in orderobj.content:
            ss = cup.to_dict()
            # ss=json.dumps(cup)
            cupOrder=pay_pay_cup_order_from_dict(ss)
            print('put')
            q.put(cup)
            print('put ok')
            
    serve(port=9000)

##StationA_S0('B',5)
##StationB_S1('A','01000200030004000508')###百香1,西柚2,黑糖3,葡萄4,芒果5
##StationC_S2('A','01080200030004000500')##柳橙1,荔枝2,粉桃3,草莓4,蔓越莓5
##StationD_S3('B','01080200030004050500')##鳳梨荔枝1,牛奶2,哈密瓜3,甜度糖第4,
##StationE_S4('B','01000200030004140500')##紅茶1,青茶4
##StationF_S5('B','01000200031704000500','05')##特殊茶3,純水4
##StationEnd_S6('B','0999-02')
##AutoClean('manual')
##t = time.localtime()
##hour_time = time.strftime("%H", t)
##print(hour_time)

#if os.environ.get('DISPLAY','') == '': ## 顯示視窗測試 ##
#    print('no display found. Using :0.0')
#    os.environ.__setitem__('DISPLAY', ':0.0')

order_queue=mp.Queue()
Value_queue=mp.SimpleQueue()
pid = os.getpid    
if __name__ == '__main__':
    os.remove('station_logger.log')
    os.remove('first_logfile.log')
    logger.info(order_queue)
    
    train_bit=mp.Array('i', 2)
    if os.path.isdir(f"./run") == True:
        shutil.rmtree('./run')
    os.mkdir('./run')

    rpcservprocess = mp.Process(target=jsonrpcserver,args=(order_queue,)) 
     
    aprocess=mp.Process(target=processA,args=(train_bit,order_queue,Value_queue))
    bprocess=mp.Process(target=processB,args=(train_bit,order_queue,Value_queue))
    rpcservprocess.start()
    aprocess.start()
    bprocess.start()

    #logger.info('add 5 test order to queue')
    # for i in range(2):
    #      order_queue.put(i)
    aprocess.join()
    bprocess.join()
