from time import sleep
# from setting import tdic1,tdic2
import sys
from AllConfig import J2,J3,J17,J33,J34,Track,Icedata
from pca9675 import PCA9675I2C

pcaR=PCA9675I2C(address=0x27,busnum=1)
for pin in range(16):
    pcaR.setup(pin,1)
    
pca=PCA9675I2C(address=0x18,busnum=1)
for i in range(16):
    pca.setup(i,0)
pca.output(J17.pin2,1)  ### A道第一管落杯   ###
pca.output(J17.pin4,1)  ### B道第一管落杯   ###
pca.output(J17.pin6,1)  ### A道第二管落杯   ###
pca.output(J17.pin8,1)  ### B道第二管落杯   ###
pca.output(J34.pin9,1)  ### 爪夾   ###
pca.output(J33.pin4,1)  ### 落冰推桿    ###

track=sys.argv[1]

def main():
    if track == "A":
        pca.output(J17.pin4,0)
        if pcaR.input(J3.pin8) != 0 :
            pca.output(J17.pin4,1)
    if track == "B":
        pca.output(J17.pin8,0)
        if pcaR.input(J3.pin8) != 0 :
            pca.output(J17.pin8,1)

if __name__ == "__main__":
    main()