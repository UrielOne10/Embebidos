import time
import ustruct

class BMP180:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x77 # Dirección estándar de Adafruit
        self._load_calibration()

    def _load_calibration(self):
        try:
            cal = self.i2c.readfrom_mem(self.addr, 0xAA, 22)
            self.AC1, self.AC2, self.AC3, self.AC4, self.AC5, self.AC6, \
            self.B1, self.B2, self.MB, self.MC, self.MD = ustruct.unpack(">hhhHHHhhhhh", cal)
        except Exception:
            raise Exception("No se pudo conectar con el BMP180.")

    @property
    def temperature(self):
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x2E')
        time.sleep(0.005)
        ut = ustruct.unpack(">h", self.i2c.readfrom_mem(self.addr, 0xF6, 2))[0]
        
        x1 = (ut - self.AC6) * self.AC5 >> 15
        x2 = (self.MC << 11) // (x1 + self.MD)
        self.b5 = x1 + x2
        return ((self.b5 + 8) >> 4) / 10.0

    @property
    def pressure(self):
        # Asegura que b5 esté actualizado para el cálculo de presión
        self.temperature 
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x34')
        time.sleep(0.005)
        up = self.i2c.readfrom_mem(self.addr, 0xF6, 3)
        up = ((up[0] << 16) | (up[1] << 8) | up[2]) >> 8
        
        b6 = self.b5 - 4000
        x1 = (self.B2 * (b6 * b6 >> 12)) >> 11
        x2 = self.AC2 * b6 >> 11
        x3 = x1 + x2
        b3 = (((self.AC1 * 4 + x3) << 0) + 2) >> 2
        
        x1 = self.AC3 * b6 >> 13
        x2 = (self.B1 * (b6 * b6 >> 12)) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self.AC4 * (x3 + 32768)) >> 15
        b7 = (up - b3) * (50000 >> 0)
        p = (b7 * 2) // b4
        x1 = (p >> 8) * (p >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        return p + ((x1 + x2 + 3791) >> 4)

    def get_altitude(self, baseline=1013.25):
        """Calcula la altitud basada en una presión de referencia (hPa)"""
        p_hpa = self.pressure / 100
        return 44330 * (1 - (p_hpa / baseline)**(1/5.255))