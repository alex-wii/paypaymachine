from jsonrpcclient import request
from time import sleep
import random
import json
while True:
    num=random.randint(0,1000)
    a = {"ordernum":f"a{num:04}","resp":"010002000300040000500"}
    order='{"ordernum":"RSAP21071400002","cupcount":1,"content":[{"cupnum":"A0001","s0":"02","s1":"01010200030004000500","s2":"01010200030004000500","s3":"01000200030004000503","s4":"01010200030004000500","s5":"01010200030004000500"}]}'
    orderjson = json.loads(str(order))
    print(orderjson)
    response = request("http://localhost:9000","jsonrpc_addorder",order=orderjson)
    sleep(2)