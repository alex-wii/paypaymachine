import subprocess
import random
import os
import time
from multiprocessing import Process
import queue  
import threading
import multiprocessing as mp
import logging


text = b'''
hello world
this is a test message
good bye
'''

A_is_run = False
B_is_run = False
notTrain = 999
Atrain =100
Btrain =200
 
dicTrain ={Atrain:"A",Btrain:"B"}
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
logger = setup_logger('first_logger', 'first_logfile.log')
trainA_logger = setup_logger('TrainA_logger', 'TrainA_logger.log')
trainB_logger = setup_logger('TrainB_logger', 'TrainB_logger.log')
order_logger = setup_logger('order_logger', 'order_logger.log')

def calls1(T,name,sec):
    p = subprocess.Popen(['python3','s1.py',f'{T}',f'{name}',f'{sec}'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    stdout,stderr=p.communicate(text)
    out = stdout.decode('utf-8')
    print(out)    
    if "erError:1" in out:
        return False
    return True

def calls1_2(T,name,sec):
    p = subprocess.Popen(['python3','s1.py',f'{T}',f'{name}',f'{sec}'])
    return p
    

# err = stderr.decode('utf-8')
def setAisrun():
    global A_is_run
    A_is_run = True
def setBisrun():
    global B_is_run
    B_is_run = True
def setAisdone():
    global A_is_run
    A_is_run = False
def setBisdone():
    global B_is_run
    B_is_run = False
    
dicSetTrainRun={Atrain:setAisrun,Btrain:setBisrun}
dicSetTrainDone={Atrain:setAisdone,Btrain:setBisdone}
def setTrainRun(T):
    print("setTrain")
    dicSetTrainRun[T]()
    print( A_is_run,B_is_run)
def setTrainDone(T):
    print("setTrain")
    dicSetTrainDone[T]()
    print( A_is_run,B_is_run)
def checkAB():
    print( A_is_run,B_is_run)
    return A_is_run,B_is_run
def choiceAB():
    A,B = checkAB()
    
    if A == False :
        return Atrain
    if B == False:
        return Btrain
    return notTrain
def trainToString(T):
        return dicTrain[T]
def pushordertoqueen(order):
    global orderqueue
    orderqueue.put(order)
    print(orderqueue)
def oneCup(orderData):
    print(f'oneCup is running')
    a = {"ordernum":"a1000","resp":"010002000300040000500"}
    station = ["s1","s2","s3","s4","s5"]
    # station = ["s1"]
    train=choiceAB()
    if train == notTrain :
        pushordertoqueen(orderData)
        
    strTrain = trainToString(train)
    setTrainRun(train)
    
    for sta in station:
        sec = random.randint(1,6)
        print(f'p={p_name} train={strTrain},sta={sta},sec={sec}')
        if calls1(strTrain,sta,sec) is True :
            print("hello")
            continue
def getStationtoRun(set_station):
    for s in set_station:
        if checkSisruning(s) is False:
            return s
        
def checkSisruning(sta):
    filename = f'./run/{sta}.run'
    if os.path.isfile(filename):
        return True
    return False

            
def stationRunWaitT(T,order):
    print(stationRunWaitT.__name__)
    
    station = ["s0","s1","s2","s3","s4","s5","s6"]
    for sta in station:
        while checkSisruning(sta) is True:
            print(f'wait 1 sec for {sta}')
            time.sleep(1)
        print(f'do {sta} {T}')
        sec = random.randint(1,6)
        p = subprocess.run(['python3','s1.py',f'{T}',f'{sta}',f'{sec}'])
    print('stationRunWaitT done')    
    
def doCupB(order):
    print(f'doCupB {order}')
    train=choiceAB()
    if train == notTrain :
        print("wait notTrain")
        return 999
    
    strTrain = trainToString(train)
    setTrainRun(train)
    print('start stationProcess')
    
    stationProcess = mp.Process(target=stationRunWaitT, args=(strTrain,order,))
    stationProcess.start()
    print('end stationProcess')
    setTrainDone(train)
                             
def doCupA(order):
    print(f'doCupA {order}')
    train=choiceAB()
    if train == notTrain :
        print("wait notTrain")
        return 999
    
    strTrain = trainToString(train)
    setTrainRun(train)
    print('start stationProcess')
    
    stationProcess = mp.Process(target=stationRunWaitT, args=(strTrain,order,))
    stationProcess.start()
    print('end stationProcess')
    setTrainDone(train)
    # stationProcess.join()
    # stationRunWaitT(strTrain,order)
    
def docupThreadA(orderqueue):
    print(docupThreadA.__name__)
    while orderqueue.empty() is False:
        order = orderqueue.get()
        print(f'start do {order}')
        doCupA(order)
    print("end do cup")

def docupThreadB(orderqueue):
    print(docupThreadB.__name__)
    while orderqueue.empty() is False:
        order = orderqueue.get()
        print(f'start do {order}')
        doCupB(order)
    print("end do cup")
    
def pushToqueueThread(orderqueue):
    print(pushToqueueThread.__name__)
    while True:
        a = {"ordernum":"a1000","resp":"010002000300040000500"}
        a1 = {"ordernum":"a1001","resp":"010002000300040000500"}
        a2 = {"ordernum":"a1002","resp":"010002000300040000500"}    
        arrayOrder = [a,a1,a2]
        index=random.randint(0,2)
        orderqueue.put(arrayOrder[index])
        # print(orderqueue.qsize)
        order_logger.info(arrayOrder[index])
        time.sleep(2)


    
    
def main():
    orderqueue = mp.Queue()
    a = {"ordernum":"a1000","resp":"010002000300040000500"}
    orderProcess = mp.Process(target=pushToqueueThread,args=(orderqueue,))
    orderProcess.start()
    time.sleep(2)
    docupProcessA = mp.Process(target=docupThreadA,args=(orderqueue,))
    docupProcessB = mp.Process(target=docupThreadB,args=(orderqueue,))
    docupProcessA.start()
    docupProcessB.start()
    
    docupProcessA.join()
    docupProcessB.join()
if __name__ == '__main__':
   main()