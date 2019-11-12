from machine import I2C
from machine import Pin

class PCA9534:
    def __init__(self, address=0x20, SCL=None, SDA=None):
        ## pin 1 = Vcc
        ## pin 2 = sDATA
        ## pin 3 = GND
        ## pin 4 = sCLK
        self.fixed = 0x40
        self.sensor_address = address
        self.i2c = I2C(-1, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
        self.input_reg = 0
        self.output_reg = 1
        self.invert_reg = 2
        self.config_reg = 3
        #self.configure()

    def scan(self):
        return self.i2c.scan()

    def configure(self):
        self.i2c.writeto_mem(self.sensor_address, self.config_reg, b'\xFE')
    
    def readValue(self):
        self.i2c.writeto_mem(self.sensor_address, self.input_reg, b'\x00')
        return self.i2c.readfrom_mem(self.sensor_address, self.input_reg, 2)