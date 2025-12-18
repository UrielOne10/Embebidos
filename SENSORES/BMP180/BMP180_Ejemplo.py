import machine
import time
from bmp180_library import BMP180 # Importamos tu clase recién guardada

# Configuración I2C para ESP32-C6
i2c = machine.I2C(0, scl=machine.Pin(7), sda=machine.Pin(6))

# Crear instancia del sensor
try:
    sensor = BMP180(i2c)
    print("Sistema BMP180 activo.")
except Exception as e:
    print("Fallo de hardware:", e)
    sensor = None

while sensor:
    t = sensor.temperature
    p = sensor.pressure / 100
    a = sensor.get_altitude()
    
    print(f"T: {t:.1f}°C | P: {p:.1f}hPa | A: {a:.1f}m")
    time.sleep(2)