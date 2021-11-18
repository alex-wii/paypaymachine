import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C
from time import sleep
from AllConfig import J2,J3,J17,J33,J34,Track

# For the PCA 953X and 955X series, the chips with 8 GPIO's have these port numbers
# The chips with 16 GPIO's have the first port for each type at double these numbers
# IE The first config port is 6

INPUT_PORT = 0
OUTPUT_PORT = 2
POLARITY_PORT = 2
CONFIG_PORT = 3

IN = GPIO.IN
OUT = GPIO.OUT
HIGH = GPIO.HIGH
LOW = GPIO.LOW


class PCA9675I2C(GPIO.BaseGPIO):
    """Class to represent a PCA9555  GPIO extender. Compatible
    with the Adafruit_GPIO BaseGPIO class so it can be used as a custom GPIO
    class for interacting with device.
    """
    NUM_GPIO = 16

    def __init__(self, address=0x27, busnum=None, i2c=None, num_gpios=16, **kwargs):
        address = int(address)
        self.__name__ = "PCA955"
        # Create I2C device.
        i2c = i2c or I2C
        busnum = busnum or i2c.get_default_bus()
        self._device = i2c.get_i2c_device(address, busnum, **kwargs)
        self.num_gpios = num_gpios
        if self.num_gpios <= 8:
            self.iodir = 0xFF #self._device.readU8(CONFIG_PORT)
            self.outputvalue = self._device.readRaw8()
        elif self.num_gpios > 8 and self.num_gpios <= 16:
            self.iodir = 0xFFFF #self._device.readU16(CONFIG_PORT<< 1)
            self.outputvalue = 0xFFFF #value1 | (value2 << 8)
            
    def _changebit(self, bitmap, bit, value):
        assert value == 1 or value == 0, "Value is %s must be 1 or 0" % value
        if value == 0:
            return bitmap & ~(1 << bit)
        elif value == 1:
            return bitmap | (1 << bit)

    # Change the value of bit PIN on port PORT to VALUE.  If the
    # current pin state for the port is passed in as PORTSTATE, we
    # will avoid doing a read to get it.  The port pin state must be
    # complete if passed in (IE it should not just be the value of the
    # single pin we are trying to change)
    def _readandchangepin(self, port, pin, value, portstate = None):
        assert pin >= 0 and pin < self.num_gpios, "Pin number %s is invalid, only 0-%s are valid" % (pin, self.num_gpios)
        if not portstate:
          if self.num_gpios <= 8:
             portstate = self._device.readRaw8()
          elif self.num_gpios > 8 and self.num_gpios <= 16:
             portstate = self._device.readU16(port << 1)

        newstate = self._changebit(portstate, pin, value)
        if self.num_gpios <= 8:
            self._device.write8(port, newstate)
        else:
            self._device.write16(port << 1, newstate)
        return newstate

    # Polarity inversion
    def polarity(self, pin, value):
        return self._readandchangepin(POLARITY_PORT, pin, value)

    # Pin direction
    def config(self, pin, mode):
        self.iodir = self._readandchangepin(CONFIG_PORT, pin, mode, self.iodir)
        return self.iodir

    def output(self, pin, value, portstate):
        #assert self.iodir & (1 << pin) == 0, "Pin %s not set to output" % pin
        #self.outputvalue = self._readandchangepin(OUTPUT_PORT, pin, value, self.outputvalue)
        
        newstate = self._changebit(portstate, pin, value)
        #print(newstate)
        self._device.write16(OUTPUT_PORT << 1, newstate)
        self.outputvalue = newstate;
        return self.outputvalue

    def input(self, pin):
        #assert self.iodir & (1 << pin) != 0, "Pin %s not set to input" % pin
        value = self._device.readRaw8()
        
        # if self.num_gpios <= 8:
        #     value = self._device.readU8(INPUT_PORT)
        # elif self.num_gpios > 8 and self.num_gpios <= 16:
        #     value = self._device.readU16(INPUT_PORT << 1)
        #     # print(f'pin{pin}:{value}')
        return value & (1 << pin)

    def setup(self, pin, mode):
        self.config(pin, mode)

    def cleanup(self, pin=None):
        # nothing to cleanup
        pass


def writedemo9675():
    pca=PCA9675I2C(address=0x18,busnum=1)


    for i in range(16):
        print(f'setup pin{i} is 0')    
        pca.setup(i,0)
    input('')
    for i in range(16):
        print(f'setup pin{i} is 1')    
        pca.output(i,1)
    input('')
    # for i in range(16):
    #     pca.polarity(i,1)
    for i in range(16):
        print(f'open {i}pin on/off')
        # input('start .. press enter..')
        sleep(0.2)
        pca.output(i,0)
        # input('its on .. press enter..')
        sleep(0.2)
        pca.output(i,1)
        # input('its off .. press enter..')
        sleep(0.2)

def read9675demo():
    oldarray={}
    pinarray={}
    pcaR=PCA9675I2C(address=0x26,busnum=1)
    for pin in range(16):
        pcaR.setup(pin,1)
    while True:
        sleep(1)

        print("-"*50)
        io=[]
        for i in range(16):
            io.append(pcaR.input(i))
        print(io)
        # for i in range(16):
        #     pinarray[i]=pcaR.input(i)
        # if pinarray is not oldarray :
        #     print(pinarray)
        #     oldarray = pinarray

# print('run write demo')
# writedemo9675()
def I2CWriteBoardID():
    pcaW11=PCA9675I2C(address=0x11,busnum=1)
    pcaW15=PCA9675I2C(address=0x15,busnum=1)
    pcaW18=PCA9675I2C(address=0x18,busnum=1)
    pcaW1c=PCA9675I2C(address=0x1c,busnum=1)
    pcaW28=PCA9675I2C(address=0x28,busnum=1)
    pcaW2a=PCA9675I2C(address=0x2a,busnum=1)
    pcaW2c=PCA9675I2C(address=0x2c,busnum=1)
    # pcaW27=PCA9675I2C(address=0x27,busnum=1)
    for i in range(16):   
            pcaW11.setup(i,0)
            pcaW15.setup(i,0)
            # pcaW18.setup(i,0)
            pcaW1c.setup(i,0)
            pcaW28.setup(i,0)
            pcaW2a.setup(i,0)
            pcaW2c.setup(i,0)
            # pcaW27.setup(i,0)
    for i in range(16): 
            pcaW11.output(i,1)
            pcaW15.output(i,1)
            pcaW18.output(i,1)
            pcaW1c.output(i,1)
            pcaW28.output(i,1)
            pcaW2a.output(i,1)
            pcaW2c.output(i,1)
            # pcaW27.output(i,1)
    pcaW18.output(J34.pin2,0)
    pcaW18.output(J34.pin4,0)

def testiopca(pca):
    for i in range(16):
        print(f'setup pin{i} is 0')    
        pca.setup(i,0)
    for i in range(16):
        pca.output(i,1)
    
    # for i in range(16):
    #     print(f'setup pin{i} is 1')    
    #     input('press on done')
    #     pca.output(i,1)
    #     input('press off')
    #     pca.output(i,0)
    #     input('press off done')

def testIO():
    # pcaR=PCA9675I2C(address=0x1c,busnum=1)
    # testiopca(pcaR)
    # pcaR.output(3,0)
    # pcaR.output(2,0)
    # pcaR.output(1,0)
    # pcaR.output(0,0)
    # pcaR=PCA9675I2C(address=0x11,busnum=1)
    # testiopca(pcaR)
    # pcaR=PCA9675I2C(address=0x15,busnum=1)
    # testiopca(pcaR)
    # pcaR.output(0,0)
    # sleep(10)
    # # pcaR.output(0,1)
    # pcaR=PCA9675I2C(address=0x28,busnum=1)
    # # testiopca(pcaR)
    

    # pcaR=PCA9675I2C(address=0x26,busnum=1)
    # pcaR=PCA9675I2C(address=0x27,busnum=1)
    # # testiopca(pcaR)
    # pcaR=PCA9675I2C(address=0x2a,busnum=1)
    # # testiopca(pcaR)
    # pcaR=PCA9675I2C(address=0x2c,busnum=1)
    # # testiopca(pcaR)
    # # pcaR=PCA9675I2C(address=0x1c,busnum=1)
    # # testiopca(pcaR)
    # pcaR=PCA9675I2C(address=0x18,busnum=1)
    input('start off')
    pcaR=PCA9675I2C(address=0x28,busnum=1)
    testiopca(pcaR)
    pcaR=PCA9675I2C(address=0x2c,busnum=1)
    testiopca(pcaR)
    pcaR=PCA9675I2C(address=0x2A,busnum=1)
    testiopca(pcaR)
    
    input('0x2C ')
    pcaR=PCA9675I2C(address=0x2C,busnum=1)
    testiopca(pcaR)
    pcaR.output(J34.pin4,0)
    input('0x2A')
    pcaR=PCA9675I2C(address=0x2A,busnum=1)
    testiopca(pcaR)
    pcaR.output(J34.pin4,0)
    input('start 0x28')
    pcaR=PCA9675I2C(address=0x28,busnum=1)
    testiopca(pcaR)
    pcaR.output(J34.pin4,0)
    input('off all')
    pcaR=PCA9675I2C(address=0x28,busnum=1)
    testiopca(pcaR)
    pcaR=PCA9675I2C(address=0x2c,busnum=1)
    testiopca(pcaR)
    pcaR=PCA9675I2C(address=0x2A,busnum=1)
    testiopca(pcaR)
    # 冰電磁閥    ###
if __name__ == '__main__':
    testIO()