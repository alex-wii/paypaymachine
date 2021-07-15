from time import sleep
# from setting import tdic1,tdic2
import time
import sys
# sys.path.append('/home/pi/machineT/machine/pca9675')
from pca9675 import PCA9675I2C
from AllConfig import J17,J33,J34,Track


###     給料模組    ###
pump=PCA9675I2C(address=0x28,busnum=1)      ###     幫浦      ###
doorA=PCA9675I2C(address=0x2c,busnum=1)      ###     A道電磁閥    ###
doorB=PCA9675I2C(address=0x2a,busnum=1)      ###     B道電磁閥    ###
###     沖茶模組    ###
teapump=PCA9675I2C(address=0x2e,busnum=1)      ###     幫浦1     ###
teadoorA=PCA9675I2C(address=0x2e,busnum=1)      ###     A道電磁閥    ###
teadoorB=PCA9675I2C(address=0x2e,busnum=1)      ###     B道電磁閥    ###
for i in range(16):
        # print(f'setup pin{i} is 0')    
        pump.setup(i,0)
        doorA.setup(i,0)
        doorB.setup(i,0)
        teapump.setup(i,0)
        teadoorA.setup(i,0)
        teadoorB.setup(i,0)
    
for i in range(16):
        # print(f'setup pin{i} is 1')    
    pump.output(i,1)
    doorA.output(i,1)
    doorB.output(i,1)
    teapump.output(i,1)
    teadoorA.output(i,1)
    teadoorB.output(i,1)
# pcaR=PCA9675I2C(address=0x26,busnum=1)


track=sys.argv[1]

def main():
    if track == "A" :
        doorA.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,1)
        doorA.output(J33.pin2,1)
        input("")
        doorA.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(2)
        pump.output(J33.pin2,1)
        doorA.output(J33.pin2,1)
        input("")
        doorA.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(3)
        pump.output(J33.pin2,1)
        doorA.output(J33.pin2,1)
        input("")
        doorA.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(4)
        pump.output(J33.pin2,1)
        doorA.output(J33.pin2,1)
        input("")
        doorA.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(5)
        pump.output(J33.pin2,1)
        doorA.output(J33.pin2,1)
        input("")
        doorA.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(1)
        pump.output(J33.pin4,1)
        doorA.output(J33.pin4,1)
        input("")
        doorA.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(2)
        pump.output(J33.pin4,1)
        doorA.output(J33.pin4,1)
        input("")
        doorA.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(3)
        pump.output(J33.pin4,1)
        doorA.output(J33.pin4,1)
        input("")
        doorA.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(4)
        pump.output(J33.pin4,1)
        doorA.output(J33.pin4,1)
        input("")
        doorA.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(5)
        pump.output(J33.pin4,1)
        doorA.output(J33.pin4,1)
        input("")
        doorA.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(1)
        pump.output(J33.pin6,1)
        doorA.output(J33.pin6,1)
        input("")
        doorA.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(2)
        pump.output(J33.pin6,1)
        doorA.output(J33.pin6,1)
        input("")
        doorA.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(3)
        pump.output(J33.pin6,1)
        doorA.output(J33.pin6,1)
        input("")
        doorA.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(4)
        pump.output(J33.pin6,1)
        doorA.output(J33.pin6,1)
        input("")
        doorA.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(5)
        pump.output(J33.pin6,1)
        doorA.output(J33.pin6,1)
        input("")
        doorA.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(1)
        pump.output(J33.pin8,1)
        doorA.output(J33.pin8,1)
        input("")
        doorA.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(2)
        pump.output(J33.pin8,1)
        doorA.output(J33.pin8,1)
        input("")
        doorA.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(3)
        pump.output(J33.pin8,1)
        doorA.output(J33.pin8,1)
        input("")
        doorA.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(4)
        pump.output(J33.pin8,1)
        doorA.output(J33.pin8,1)
        input("")
        doorA.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(5)
        pump.output(J33.pin8,1)
        doorA.output(J33.pin8,1)
        input("")
        teadoorA.output(J33.pin10,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(1)
        teapump.output(J17.pin10,1)
        teadoorA.output(J33.pin10,1)
        input("")
        teadoorA.output(J33.pin10,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(2)
        teapump.output(J17.pin10,1)
        teadoorA.output(J33.pin10,1)
        input("")
        teadoorA.output(J33.pin10,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(3)
        teapump.output(J17.pin10,1)
        teadoorA.output(J33.pin10,1)
        input("")
        teadoorA.output(J33.pin10,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(4)
        teapump.output(J17.pin10,1)
        teadoorA.output(J33.pin10,1)
        input("")
        teadoorA.output(J33.pin10,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(5)
        teapump.output(J17.pin10,1)
        teadoorA.output(J33.pin10,1)
    if track == "B":
        doorB.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,1)
        doorB.output(J33.pin2,1)
        input("")
        doorB.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(2)
        pump.output(J33.pin2,1)
        doorB.output(J33.pin2,1)
        input("")
        doorB.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(3)
        pump.output(J33.pin2,1)
        doorB.output(J33.pin2,1)
        input("")
        doorB.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(4)
        pump.output(J33.pin2,1)
        doorB.output(J33.pin2,1)
        input("")
        doorB.output(J33.pin2,0) 
        time.sleep(1)
        pump.output(J33.pin2,0) 
        time.sleep(5)
        pump.output(J33.pin2,1)
        doorB.output(J33.pin2,1)
        input("")
        doorB.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(1)
        pump.output(J33.pin4,1)
        doorB.output(J33.pin4,1)
        input("")
        doorB.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(2)
        pump.output(J33.pin4,1)
        doorB.output(J33.pin4,1)
        input("")
        doorB.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(3)
        pump.output(J33.pin4,1)
        doorB.output(J33.pin4,1)
        input("")
        doorB.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(4)
        pump.output(J33.pin4,1)
        doorB.output(J33.pin4,1)
        input("")
        doorB.output(J33.pin4,0) 
        time.sleep(1)
        pump.output(J33.pin4,0)
        time.sleep(5)
        pump.output(J33.pin4,1)
        doorB.output(J33.pin4,1)
        input("")
        doorB.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(1)
        pump.output(J33.pin6,1)
        doorB.output(J33.pin6,1)
        input("")
        doorB.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(2)
        pump.output(J33.pin6,1)
        doorB.output(J33.pin6,1)
        input("")
        doorB.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(3)
        pump.output(J33.pin6,1)
        doorB.output(J33.pin6,1)
        input("")
        doorB.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(4)
        pump.output(J33.pin6,1)
        doorB.output(J33.pin6,1)
        input("")
        doorB.output(J33.pin6,0)  
        time.sleep(1)
        pump.output(J33.pin6,0)
        time.sleep(5)
        pump.output(J33.pin6,1)
        doorB.output(J33.pin6,1)
        input("")
        doorB.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(1)
        pump.output(J33.pin8,1)
        doorB.output(J33.pin8,1)
        input("")
        doorB.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(2)
        pump.output(J33.pin8,1)
        doorB.output(J33.pin8,1)
        input("")
        doorB.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(3)
        pump.output(J33.pin8,1)
        doorB.output(J33.pin8,1)
        input("")
        doorB.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(4)
        pump.output(J33.pin8,1)
        doorB.output(J33.pin8,1)
        input("")
        doorB.output(J33.pin8,0) 
        time.sleep(1)
        pump.output(J33.pin8,0)
        time.sleep(5)
        pump.output(J33.pin8,1)
        doorB.output(J33.pin8,1)
        input("")
        teadoorB.output(J34.pin9,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(1)
        teapump.output(J17.pin10,1)
        teadoorB.output(J34.pin9,1)
        input("")
        teadoorB.output(J34.pin9,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(2)
        teapump.output(J17.pin10,1)
        teadoorB.output(J34.pin9,1)
        input("")
        teadoorB.output(J34.pin9,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(3)
        teapump.output(J17.pin10,1)
        teadoorB.output(J34.pin9,1)
        input("")
        teadoorB.output(J34.pin9,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(4)
        teapump.output(J17.pin10,1)
        teadoorB.output(J34.pin9,1)
        input("")
        teadoorB.output(J34.pin9,0)  
        time.sleep(1)
        teapump.output(J17.pin10,0)
        time.sleep(5)
        teapump.output(J17.pin10,1)
        teadoorB.output(J34.pin9,1)
if __name__ == "__main__":
    main()