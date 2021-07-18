from time import sleep
import sys
import os
import stat
from alexloger import *
print("*"*50)
print("s1ta run")
name = sys.argv[2]
train = sys.argv[1]
sec = int(sys.argv[3])
filename = f'./run/{name}.run'
fileTrainName =  f'./run/{name}{train}.run'
if os.path.exists(filename):
    station_logger.info(f"Error:1 , {filename} is run")
    sys.exit(1)

station_logger.info(f'{filename},{fileTrainName}')
open(filename, 'w').close()
open(fileTrainName, 'w').close()


station_logger.info(f'{"*"*10}')
station_logger.info(f"ss:{name}{train}")

station_logger.info(f"{name}{train}start wait {sec} sec")
sleep(sec)
station_logger.info(f"{name}{train} end wait {sec} sec")
station_logger.info(f"{sys.argv[1]}{name}done")
os.remove(filename)
os.remove(fileTrainName)
