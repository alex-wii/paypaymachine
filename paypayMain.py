#!/usr/bin/python3


import multiprocessing as mp
import time
from jsonrpcserver import method,serve
import os
import random
import subprocess
import shutil
from alexloger import *
from paypayorder import PayPayOrder
from PayPayCupOrder import PayPayCupOrder,pay_pay_cup_order_from_dict
import json


def checkSisruning(sta):
    filename = f'./run/{sta}.run'
    if os.path.isfile(filename):
        return True
    return False
def getS0o(orderTxt):
    print(orderTxt)
def getS1o(orderTxt):
    print(orderTxt)

    
def processA(bitArray,order):
    print(f'A: pid={pid()}')
    while True:
        
        if order.empty():
            logger.info('A empty')
            time.sleep(1)
            continue
        o=order.get()
        print(o)
        print(f'{o}')
        logger.info(f'A:processA {list(bitArray)},order={o}')
        bitArray[0]=1
        logger.info(f'A:aprocessA-1 {list(bitArray)},order={o}')   
        recp_dic = {"stationa":o.stationa,"stationb":o.stationb,"stationc":o.stationc,"stationd":o.stationd,"statione":o.statione,"stationf":o.stationf,"s6":"endpoint"}
        station_dic = {"s0":"stationa","s1":"stationb","s2":"stationc","s3":"stationd","s4":"statione","s5":"stationf","s6":"endpoint"}
        station = ["s0","s1","s2","s3","s4","s5","s6"]
        for sta in station:
            while checkSisruning(sta) is True:
                logger.info(f'A:wait 1 sec for {sta}')
                time.sleep(1)
            
            print(f'hello-{sta}-{recp_dic[station_dic[sta]]}')
            logger.info(f'hello-{sta}-{recp_dic[station_dic[sta]]}')   
            sec = random.randint(5,10) 
            logger.info(f'A:do {sta} A {sec} sec')
            if os.uname()[0] == 'Linux' :
                print(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                p = subprocess.run(['python3',f'{sta}.py',f'A',f'{recp_dic[station_dic[sta]]}'])
            else:
                print(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py A {recp_dic[station_dic[sta]]}')
                p = subprocess.run(['python3',f'{sta}ta.py',f'A',f'{recp_dic[station_dic[sta]]}',f'{sec}'])
            # p = subprocess.run(['python3','s1.py',f'A',f'{sta}',f'{sec}'])
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
        recp_dic = {"stationa":o.stationa,"stationb":o.stationb,"stationc":o.stationc,"stationd":o.stationd,"statione":o.statione,"stationf":o.stationf,"s6":"endpoint"}
        station_dic = {"s0":"stationa","s1":"stationb","s2":"stationc","s3":"stationd","s4":"statione","s5":"stationf","s6":"endpoint"}
        station = ["s0","s1","s2","s3","s4","s5","s6"]
        
        for sta in station:
            while checkSisruning(sta) is True:
                
                logger.info(f'B:{sta} A is running , wait 1 sec for {sta} A')
                time.sleep(1)
            logger.info(f'hello-{sta}-{recp_dic[station_dic[sta]]}')
            print(f'hello-{sta}-{recp_dic[station_dic[sta]]}')
            logger.info(f'hello-{sta}-{recp_dic[station_dic[sta]]}')   
            sec = random.randint(5,10)
            
            logger.info(f'B:{sta} free do {sta} on B {sec} sec')
            
            if os.uname()[0] == 'Linux' :
                p = subprocess.run(['python3',f'{sta}.py',f'B',f'{recp_dic[station_dic[sta]]}'])
                print(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')   
                
            else:
                p = subprocess.run(['python3',f'{sta}ta.py',f'B',f'{recp_dic[station_dic[sta]]}',f'{sec}'])
                print(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')
                logger.info(f'send cmd python3 {sta}.py B {recp_dic[station_dic[sta]]}')   
                
                
        time.sleep(2)
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
    
    
order_queue=mp.Queue()
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
    
    aprocess=mp.Process(target=processA,args=(train_bit,order_queue))
    bprocess=mp.Process(target=processB,args=(train_bit,order_queue))
    rpcservprocess.start()
    aprocess.start()
    bprocess.start()
    logger.info('add 5 test order to queue')
    # for i in range(2):
    #      order_queue.put(i)
    
    aprocess.join()
    bprocess.join()
