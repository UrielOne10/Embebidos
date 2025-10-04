# i2c_lcd.py code from theoryCIRCUIT

from lcd_api import LcdApi
from machine import I2C
import time

class I2cLcd(LcdApi):
    LCD_I2C_ADDR = 0x27
    LCD_WIDTH = 16
    LCD_CHR = 1
    LCD_CMD = 0
    LCD_BACKLIGHT = 0x08

    ENABLE = 0b00000100

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = self.LCD_BACKLIGHT
        self.num_lines = num_lines
        self.num_columns = num_columns
        time.sleep_ms(20)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(5)
        self.hal_write_init_nibble(0x03)
        time.sleep_ms(1)
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x02)
        cmd = self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)
        self.hal_write_command(self.LCD_CLR)
        time.sleep_ms(2)
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)

    def hal_write_init_nibble(self, nibble):
        byte = (nibble << 4) | self.backlight
        self.i2c.writeto(self.i2c_addr, bytes([byte | self.ENABLE]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))

    def hal_write_command(self, cmd):
        self.hal_write_byte(cmd, self.LCD_CMD)

    def hal_write_data(self, data):
        self.hal_write_byte(data, self.LCD_CHR)

    def hal_write_byte(self, data, mode):
        high = mode | (data & 0xF0) | self.backlight
        low = mode | ((data << 4) & 0xF0) | self.backlight
        self.i2c.writeto(self.i2c_addr, bytes([high | self.ENABLE]))
        self.i2c.writeto(self.i2c_addr, bytes([high]))
        self.i2c.writeto(self.i2c_addr, bytes([low | self.ENABLE]))
        self.i2c.writeto(self.i2c_addr, bytes([low]))

    def hal_sleep_ms(self, ms):
        time.sleep_ms(ms)