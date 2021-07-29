


import multiprocessing as mp
import time
from jsonrpcserver import method,serve
import os
import random
import subprocess
import shutil
from alexloger import *




def checkSisruning(sta):
    filename = f'./run/{sta}.run'
    if os.path.isfile(filename):
        return True
    return False

def processA(bitArray,order):
    print(f'A: pid={pid()}')
    while True:
        
        if order.empty():
            logger.info('A empty')
            time.sleep(1)
            continue
        o=order.get()
        logger.info(f'A:processA {list(bitArray)},order={o}')
        bitArray[0]=1
        logger.info(f'A:aprocessA-1 {list(bitArray)},order={o}')
        
        station = ["s0","s1","s2","s3","s4","s5","s6"]
        for sta in station:
            while checkSisruning(sta) is True:
                logger.info(f'A:wait 1 sec for {sta}')
                time.sleep(1)
                
            
            sec = random.randint(5,10)
            
            logger.info(f'A:do {sta} A {sec} sec')
            p = subprocess.run(['python3',f'{sta}ta.py',f'A',f'{sta}',f'{sec}'])
        time.sleep(2)
        bitArray[0]=0
        logger.info(f'A:processA-E {list(bitArray)},order={o}')
def processB(bitArray,order):
    print(f'B: pid={pid()}')
    while True:
        time.sleep(2)
        if order.empty():
            logger.info('B:B empty')
            time.sleep(1)
            continue
        o=order.get()
        logger.info(f'B:processB show train AB is available {list(bitArray)},order={o}')
        bitArray[1]=1
        logger.info(f'B:processB-1 set train B{list(bitArray)},order={o}')
        
        station = ["s0","s1","s2","s3","s4","s5","s6"]
        for sta in station:
            while checkSisruning(sta) is True:
                
                logger.info(f'B:{sta} A is running , wait 1 sec for {sta} A')
                time.sleep(1)
                
            
            sec = random.randint(5,10)
            
            logger.info(f'B:{sta} free do {sta} on B {sec} sec')
            p = subprocess.run(['python3',f'{sta}ta.py',f'B',f'{sta}',f'{sec}'])
            
        time.sleep(2)
        bitArray[1]=0
        logger.info(f'B:processB-End done {list(bitArray)},order={o}')
a=mp.Queue()


def jsonrpcserver(q):
    @method
    def jsonrpc_addorder(order):
        logger.info(f'json add order {order} from rpc')
        q.put(order)
    
    serve(port=9000)    
pid = os.getpid    
if __name__ == '__main__':
    
    os.remove('station_logger.log')
    os.remove('first_logfile.log')
    logger.info(a)
    
    train_bit=mp.Array('i', 2)
    shutil.rmtree('./run')
    os.mkdir('./run')
    
    rpcservprocess = mp.Process(target=jsonrpcserver,args=(a,))
    
    aprocess=mp.Process(target=processA,args=(train_bit,a))
    bprocess=mp.Process(target=processB,args=(train_bit,a))
    rpcservprocess.start()
    aprocess.start()
    bprocess.start()
    logger.info('add 5 test order to queue')
    for i in range(5):
        a.put(i)
    
    aprocess.join()
    bprocess.join()
