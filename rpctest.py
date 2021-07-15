from jsonrpcclient import request
from time import sleep
import random
while True:
    num=random.randint(0,1000)
    a = {"ordernum":f"a{num:04}","resp":"010002000300040000500"}
    
    response = request("http://localhost:5000","jsonrpc_addorder",order=a)
    sleep(2)