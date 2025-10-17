# lcd_api.py code from theoryCIRCUIT

class LcdApi:
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_ENTRY_INC = 0x02
    LCD_ENTRY_SHIFT = 0x01
    LCD_ON_CTRL = 0x08
    LCD_ON_DISPLAY = 0x04
    LCD_ON_CURSOR = 0x02
    LCD_ON_BLINK = 0x01
    LCD_MOVE = 0x10
    LCD_MOVE_DISP = 0x08
    LCD_MOVE_RIGHT = 0x04
    LCD_FUNCTION = 0x20
    LCD_FUNCTION_2LINES = 0x08
    LCD_FUNCTION_5x10DOTS = 0x04
    LCD_FUNCTION_8BIT = 0x10
    LCD_CGRAM = 0x40
    LCD_DDRAM = 0x80

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        if self.num_lines > 1:
            self.displayfunction = self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES
        else:
            self.displayfunction = self.LCD_FUNCTION
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_sleep_ms(2)

    def home(self):
        self.hal_write_command(self.LCD_HOME)
        self.hal_sleep_ms(2)

    def set_cursor(self, col, row):
        self.cursor_x = col
        self.cursor_y = row
        addr = col & 0x3F
        if row & 1:
            addr += 0x40
        self.hal_write_command(self.LCD_DDRAM | addr)

    def write(self, s):
        for char in s:
            self.hal_write_data(ord(char))

    def putstr(self, string):
        self.write(string)

    def move_to(self, col, row):
        self.set_cursor(col, row)

    # Override in subclass
    def hal_write_command(self, cmd):
        pass

    def hal_write_data(self, data):
        pass

    def hal_sleep_ms(self, ms):
        pass