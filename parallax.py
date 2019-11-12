from machine import UART
import utime


class LCD:
    def __init__(self, tx_pin=1, baud_rate=19200, backlight=1):
        utime.sleep_ms(100)
        self.uart = UART(tx_pin, baud_rate)
        # 22 for no cursor, 23 for cursor off and flashing block, 24 for flat horizontal, 25 for flashing block
        self.setCursorType(22)
        self.backlight(backlight)
        self.clearScreen()

    def write(self, string):
        self.uart.write(str(string))

    def clearScreen(self):
        self.write('\f')
        utime.sleep_ms(5)

    def cursorLeft(self):
        self.write('\b')

    def cursorRight(self):
        self.write('\t')

    def newLine(self):
        self.write('\n')

    def carriageReturn(self):
        self.write('\r')

    def display(self, state):
        if(state):
            self.write(chr(self.cursor_type))
        else:
            self.write(chr(21))

    def setCursorType(self, cursor_type):
        self.cursor_type = cursor_type
        self.write(chr(self.cursor_type))

    def goto(self, location=0):
        # 128-217
        home = 128
        self.write(chr(home + location))

    def backlight(self, state):
        if(state):
            self.write(chr(17))
        else:
            self.write(chr(18))
