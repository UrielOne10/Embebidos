from machine import Pin, SoftI2C, ADC, UART
from utime import ticks_diff, ticks_ms
from max30102._init_ import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from lib.i2c_lcd import I2cLcd
import time, math

# =================== CONFIGURACION LCD ===================
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = SoftI2C(sda=Pin(6), scl=Pin(7), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# =================== CONFIGURACION ADC ===================
adc1 = ADC(Pin(0))  
adc1.atten(ADC.ATTN_0DB)        # rango ~0 a 1.1V
adc1.width(ADC.WIDTH_12BIT)     # resolución 12 bits
VREF = 1.1
ADC_MAX = 4095


adc2 = ADC(Pin(34))             
adc2.atten(ADC.ATTN_11DB)       # rango hasta 3.3V
adc2.width(ADC.WIDTH_12BIT)

# =================== CONFIGURACION UART ===================
uart = UART(1, baudrate=9600, tx=17, rx=16)

# =================== CONFIGURACION MAX30102 ===================
sensor = MAX30102(i2c=i2c)
sensor.setup_sensor()
sensor.set_pulse_amplitude_red(MAX30105_PULSE_AMP_MEDIUM)
sensor.set_pulse_amplitude_ir(MAX30105_PULSE_AMP_MEDIUM)

# =================== VARIABLES GLOBALES ===================
vector = []
tamano = 10
ventana_red = []
ventana_ir = []
VENTANA_SIZE = 30

estado = "APAGADO"
activo = None

# =================== FUNCIONES ===================
def leer_temperatura():
    lectura = adc1.read()
    voltaje = (lectura * VREF) / ADC_MAX
    temperatura = ((voltaje * 1000) / 10)
    return temperatura, voltaje, lectura

# =================== FUNCIONES ===================
def leer_temperatura_lcd():
    valor_adc = adc2.read()
    voltaje = (valor_adc / 4095.0) * 3.3
    temp_c = voltaje * 100
    return temp_c

def mostrar_apagado():
    lcd.clear()
    lcd.putstr("   APAGADO   ")
    lcd.move_to(0, 1)
    lcd.putstr("Esperando dato")

def mostrar_estado(temp, red=None, spo2=None):
    lcd.clear()
    if activo == "F":
        lcd.putstr("Foco encendido")
    elif activo == "V":
        lcd.putstr("Ventilador ON")
    else:
        lcd.putstr("Desconocido")

    lcd.move_to(0, 1)
    lcd.putstr("T:{:.1f}C ".format(temp))
    if red is not None:
        lcd.putstr("R:{:04d}".format(red))
    if spo2 is not None:
        lcd.putstr(" SpO2:{:.1f}".format(spo2))

# =================== MAIN LOOP===================
try:
    lcd.clear()
    mostrar_apagado()
    print("Iniciando adquisicion: TEMP, RED, SpO2")

    while True:
        # ===== UART: revisar estado =====
        if uart.any():
            dato = uart.read(1).decode('utf-8').strip()
            if dato == "F":
                activo, estado = "F", "ENCENDIDO"
            elif dato == "V":
                activo, estado = "V", "ENCENDIDO"
            else:
                activo, estado = None, "APAGADO"

        # ===== Temperatura ADC1  =====
        temp1, v, l = leer_temperatura()
        vector.append(temp1 * 3)
        if len(vector) == tamano:
            promedio = math.sqrt(sum(x**2 for x in vector)) / tamano
            print(" Temp1 = {:.2f} °C".format(promedio))
            vector = []

        # ===== Temperatura ADC2  =====
        temp2 = leer_temperatura_lcd()

        # ===== MAX30102 =====
        sensor.check()
        red = None
        spo2 = None
        if sensor.available():
            red = sensor.pop_red_from_storage()
            ir = sensor.pop_ir_from_storage()
            ventana_red.append(red)
            ventana_ir.append(ir)

            if len(ventana_red) > VENTANA_SIZE:
                ventana_red.pop(0)
                ventana_ir.pop(0)

            # Ejemplo: SpO2 estimado
            if len(ventana_red) == VENTANA_SIZE:
                spo2 = sum(ventana_red)/VENTANA_SIZE
                print("RED: {:04d}, SpO2*: {:.2f}".format(red, spo2))
            else:
                print("RED: {:04d}".format(red))

        # ===== LCD =====
        if estado == "APAGADO":
            mostrar_apagado()
        else:
            mostrar_estado(temp2, red, spo2)

        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    lcd.putstr("Programa detenido")
    lcd.backlight_off()

