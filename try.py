from AllConfig import J2,J3,J17,J33,J34,Track
from pca9675 import PCA9675I2C
import time
# pcaR=PCA9675I2C(address=0x27,busnum=1)
# for pin in range(16):
#     pcaR.setup(pin,1)
# pca=PCA9675I2C(address=0x18,busnum=1)
# for i in range(16):
#     pca.setup(i,0)
# pca.output(J17.pin2,1)  ### A道第一管落杯   ###
# pca.output(J17.pin4,1)  ### B道第一管落杯   ###
# pca.output(J17.pin6,1)  ### A道第二管落杯   ###
# pca.output(J17.pin8,1)  ### B道第二管落杯   ###
# pca.output(J34.pin9,1)  ### 爪夾   ###
# # pca.output(J33.pin2,1)
# pca.output(J33.pin4,1)
# # pca.output(J33.pin2,0)  ### 落冰推桿    ###
pump=PCA9675I2C(address=0x28,busnum=1)      ###     幫浦      ###
#for i in range(16):
    #pump.setup(i,0)
    # time.sleep(0.1)
    #pump.output(i,1)
doorA=PCA9675I2C(address=0x2c,busnum=1)      ###     A道電磁閥    ###
#for i in range(16):
    # print(i)
    #doorA.setup(i,0)
    # time.sleep(2)
    # print(i)
    #doorA.output(i,1)
    # time.sleep(2)
    # doorA.output(i,0)
doorB=PCA9675I2C(address=0x2a,busnum=1)      ###     B道電磁閥    ###
#for i in range(16):
    # print(i)
    #doorB.setup(i,0)
    # time.sleep(2)
    # print(i)
    #doorB.output(i,1)
    # time.sleep(2)
    # doorB.output(i,0)
def main():
    #pcaR=PCA9675I2C(address=0x26,busnum=1)
    #pcaR.input(J3.pin2)
    i=6
    time.sleep(1)
    doorA.output(i,0)#開電磁閥
    time.sleep(1)
    doorB.output(i,0)#開電磁閥
    time.sleep(1)
    pump.output(i,0)
    time.sleep(1)
    doorB.output(i,1)
    time.sleep(5)
    doorB.output(i,0)
    time.sleep(1)
    doorA.output(i,1)
    time.sleep(5)
    doorA.output(i,0)
    time.sleep(1)
    pump.output(i,1)
    time.sleep(1)
    doorA.output(i,1)
    time.sleep(1)
    doorB.output(i,1)
if __name__ == "__main__":
    main()