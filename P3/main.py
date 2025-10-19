from machine import ADC, Pin, SoftI2C
from time import sleep
from lib.i2c_lcd import I2cLcd
import math

# CONFIG LCD
def CONFIG_LCD():
    global lcd
    I2C_ADDR = 0x27
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16
    i2c = SoftI2C(sda=Pin(7), scl=Pin(6), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# VARIABLES GLOBALES
estado = False
vector = []
Foco = Pin(3, Pin.OUT)
Ventilador = Pin(2, Pin.OUT)
tiempo_sleep_ms = 5000  # tiempo de sleep en milisegundos (5 segundos)

# INTERRUPCION EXTERNA
def cambiar_estado(pin):
    global estado
    estado = not estado
    print("Estado cambiado:", estado)

BtnEstado = Pin(1, Pin.IN, Pin.PULL_DOWN)
BtnEstado.irq(handler=cambiar_estado, trigger=Pin.IRQ_FALLING)

# CONFIG ADC
def CONFIG_ADC():
    global adc
    adc = ADC(Pin(0))
    adc.atten(ADC.ATTN_0DB)      # rango ~0 - 1.1 V
    adc.width(ADC.WIDTH_12BIT)   # resolución 0 - 4095

def leer_temperatura():
    VREF = 1.1
    ADC_MAX = 4095
    lectura = adc.read()
    voltaje = (lectura * VREF) / ADC_MAX
    temperatura = ((voltaje * 1000) / 10)   # ejemplo: 10 mV/°C
    return temperatura, voltaje, lectura

def promedio():
    tamano = 100
    global vector
    if len(vector) == tamano:
        prom = sum(vector) / tamano
        vector = []
        return prom, True
    else:
        return 0, False

def Mostrar(temp_promedio):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Temp: {:.2f}".format(temp_promedio) + chr(223) + "C")

    # Estado del foco
    FOCO = Foco.value()
    VENTILADOR = Ventilador.value()

    lcd.move_to(0, 1)
    if FOCO == 1 and VENTILADOR == 0:
        lcd.putstr("Foco: ENCENDIDO ")
    elif FOCO == 0 and VENTILADOR == 1:
        lcd.putstr("Vent: ENCENDIDO ")
    elif FOCO == 1 and VENTILADOR == 1:
        lcd.putstr("Ambos encendidos")
    else:
        lcd.putstr("Todo apagado   ")

# PROGRAMA PRINCIPAL
CONFIG_ADC()
CONFIG_LCD()

margen = 2
temp_deseada = 35

while True:
    temp, volt, lec = leer_temperatura()
    vector.append(temp)
    temp_promedio, listo = promedio()

    if listo:
        # ---- Lógica de control ----
        if temp_promedio < temp_deseada - (margen / 2):
            Foco.on()
            Ventilador.off()
        elif temp_promedio > temp_deseada + (margen / 2):
            Foco.off()
            Ventilador.on()
        else:
            # Dentro del margen, no cambia estado
            pass

        # ---- Mostrar en consola y LCD ----
        print("Temp promedio: {:.2f} °C".format(temp_promedio))
        print("Foco:", Foco.value(), "| Ventilador:", Ventilador.value())
        Mostrar(temp_promedio)
        
        if estado:
             # ---- Entra en modo ahorro ----
            print("Entrando en modo sleep por", tiempo_sleep_ms / 1000, "s...")
            lightsleep(tiempo_sleep_ms)
            # Al terminar el sleep, se despierta y repite el ciclo

    sleep(0.01)
    


            

    
