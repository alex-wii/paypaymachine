
import subprocess
import random
import os
import time
from multiprocessing import Process
import queue  
import threading
import multiprocessing as mp
import logging
import sys


A_is_run = False
B_is_run = False
notTrain = 999
Atrain =100
Btrain =200
dicTrain ={Atrain:"A",Btrain:"B"}
trainBit=[0,0]
def setAisrun(trainBit):
    global A_is_run
    trainBit[0]=1
    A_is_run = True
def setBisrun(trainBit):
    global B_is_run
    trainBit[1]=1
    B_is_run = True
def setAisdone(trainBit):
    global A_is_run
    trainBit[0]=0
    A_is_run = False
def setBisdone(trainBit):
    global B_is_run
    trainBit[1]=0
    B_is_run = False
    
dicSetTrainRun={Atrain:setAisrun,Btrain:setBisrun}
dicSetTrainDone={Atrain:setAisdone,Btrain:setBisdone}

def setTrainRun(T,train_bit):
    print("setTrainRun")
    dicSetTrainRun[T](train_bit)
    print(trainBit)
    print( A_is_run,B_is_run)
def setTrainDone(T):
    
    print("setTrainDone")
    dicSetTrainDone[T](trainBit)
    print(trainBit)
    print( A_is_run,B_is_run)
def checkAB():
    print( A_is_run,B_is_run)
    print(trainBit)
    return A_is_run,B_is_run
def choiceAB(trainBit):
    if trainBit[0]==0 :
        return Atrain
    if trainBit[1]==0 :
        return Btrain
    return notTrain
def trainToString(T):
    return dicTrain[T]
    


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
train_logger = setup_logger('TrainB_logger', 'train_logger.log')
order_logger = setup_logger('order_logger', 'order_logger.log')
do_order_logger = setup_logger('do_order_logger', 'do_order_logger.log')
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

def make_order(orderqueue):
    orderProcess = mp.Process(target=pushToqueueThread,args=(orderqueue,))
    orderProcess.start()
    time.sleep(2)
def checkSisruning(sta):
    filename = f'./run/{sta}.run'
    if os.path.isfile(filename):
        return True
    return False

def trainFactory(order,train,train_bit):
    strTrain=trainToString(train)
    print(f'1trainFactory {order},{strTrain}')
    train_logger.info(f'trainFactory {order},{strTrain}')
    time.sleep(3)
    print(f'2trainFactory done {order},{strTrain}')
    print(f"3train_bit={train_bit}")
    if train == Atrain :
        train_bit[0]=0
    else :
        train_bit[1]=0
    print(f"4trainFactory done train_bit={train_bit}")
    train_logger.info(f'5trainFactory done {order},{strTrain}')
         
def do_cup(order,train,train_bit):
    print(f'do_cup train_bit={train_bit}')
    print('do trainProcess')
    calltrainProcess(order,train,train_bit)
    print('do trainProcess next')
def calltrainProcess(order,train,train_bit):
    print(f'calltrainProcess_ train_bit={train_bit}')
    trainProcess=mp.Process(target=trainFactory,args=(order,train,train_bit))
    trainProcess.start()
    trainProcess.join()
    

    
        
def do_order(orderqueue,train_bit):
    while True:
        while orderqueue.empty() is False:
            train=choiceAB(train_bit)
            print(f'do_order train_bit={train_bit}')
            if train == notTrain:
                print('wait 1 sec for train free')
                time.sleep(1)
                continue
            order = orderqueue.get()
            do_order_logger.info(f'train{train}:{order}')
            setTrainRun(train,train_bit)
            print(f'do_order train_bit={train_bit}')
            do_cup(order,train,train_bit)
            
            
def main():
    
    global trainBit
    train_bit=mp.Array('i', 2)
    train_bit=trainBit
    orderqueue = mp.Queue()
    make_order(orderqueue)
    print(f'main:{trainBit}')
    do_orderProcess = mp.Process(target=do_order,args=(orderqueue,train_bit,))
    do_orderProcess.start()
    
    do_orderProcess.join()
    
        
if __name__ == '__main__':
     main()