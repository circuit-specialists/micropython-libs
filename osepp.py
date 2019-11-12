"""
written by Jake Pring from CircuitSpecialists.com
licensed as GPLv3
"""

from machine import Pin, ADC
import nodeMCU
import utime


class LCD:
    def __init__(self, uC='esp8266', bits=4):
        self.bit_length = bits
        utime.sleep_us(40000)
        # RS is connected to GND, A is Backlight Pos, K is Backlight GND
        if(uC == 'esp8266'):
            device = nodeMCU.ESP8266()

        try:
            self.initPins(device)
            self.initDisplay()
        except Exception as e:
            print(e)

    def initPins(self, device):
        self.E = device.D1
        self.RS = device.D2
        self.D7 = device.D3
        self.D6 = device.D4
        self.D5 = device.D7
        self.D4 = device.D8
        self.button = device.A0

    def initDisplay(self):
        utime.sleep_us(40000)
        if(self.bit_length == 4):
            self.write2LCD_4bits(0, 0x2C, 15200)
        else:
            self.write2LCD_8bits(0, 0x3C, 15200)

    def write2LCD(self, register_select, byte_block, wait_time):
        print(byte_block)
        if(self.bit_length == 4):
            self.write2LCD_4bits(register_select, byte_block, wait_time)
        else:
            self.write2LCD_8bits(register_select, byte_block, wait_time)

    def write2LCD_4bits(self, register_select, byte_block, wait_time):
        time = utime.ticks_us()
        if(register_select):
            self.RS.on()

        # MSB
        if(byte_block & 128 > 0):
            self.D7.on()
        if(byte_block & 64 > 0):
            self.D6.on()
        if(byte_block & 32 > 0):
            self.D5.on()
        if(byte_block & 16 > 0):
            self.D4.on()

        self.E.on()
        if((time + wait_time) - utime.ticks_us() > 0):
            utime.sleep_us((time + wait_time) - utime.ticks_us())
        time = utime.ticks_us()
        self.E.off()
        self.RS.off()
        self.D7.off()
        self.D6.off()
        self.D5.off()
        self.D4.off()

        # LSB
        if(byte_block & 8 > 0):
            self.D7.on()
        if(byte_block & 4 > 0):
            self.D6.on()
        if(byte_block & 2 > 0):
            self.D5.on()
        if(byte_block & 1 > 0):
            self.D4.on()

        self.E.on()
        if((time + wait_time) - utime.ticks_us() > 0):
            utime.sleep_us((time + wait_time) - utime.ticks_us())
        self.E.off()
        self.RS.off()
        self.D7.off()
        self.D6.off()
        self.D5.off()
        self.D4.off()

    def write2LCD_8bits(self, register_select, byte_block, wait_time):
        time = utime.ticks_us()
        if(register_select):
            self.RS.on()

        # MSB
        if(byte_block & 128 > 0):
            self.D7.on()
        if(byte_block & 64 > 0):
            self.D6.on()
        if(byte_block & 32 > 0):
            self.D5.on()
        if(byte_block & 16 > 0):
            self.D4.on()

        # LSB
        if(byte_block & 8 > 0):
            self.D3.on()
        if(byte_block & 4 > 0):
            self.D2.on()
        if(byte_block & 2 > 0):
            self.D1.on()
        if(byte_block & 1 > 0):
            self.D0.on()

        self.E.on()
        if((time + wait_time) - utime.ticks_us() > 0):
            utime.sleep_us((time + wait_time) - utime.ticks_us())
        self.E.off()
        self.RS.off()
        self.D7.off()
        self.D6.off()
        self.D5.off()
        self.D4.off()

    def clearDisplay(self):
        self.write2LCD(0, 0x01, 1520)

    def returnHome(self):
        self.write2LCD(0, 0x20, 1520)

    def entry_mode_set(self, mode=1, shift=1):
        temp = 0
        temp |= (mode << 1)
        temp |= shift

    def display_cursor_blink(self, display=1, cursor=1, blink=1):
        temp = 0
        temp |= (display << 2)
        temp |= (display << 1)
        temp |= display
        self.write2LCD(0, temp, 38)

    def cursor_display_shift(self, s_c=1, r_l=1):
        temp = 0
        temp |= (s_c << 3)
        temp |= (r_l << 2)
        self.write2LCD(0, temp, 38)

    def functionSet(self, bit_length=4, lines=2, font_size=1):
        temp = 0

        # number of lanes connected to lcd
        if(bit_length == 4):
            temp |= 0x20
        elif(bit_length == 8):
            temp |= 0x30

        # lines to display on screen
        if(lines == 2):
            temp |= 8

        # font size displayed
        temp |= (font_size << 2)
        self.write2LCD(0, temp, 38)

    def write2RAM(self, char):
        self.write2LCD(1, ord(char), 38)
