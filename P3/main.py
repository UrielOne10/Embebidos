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
        promedio = sum(vector) / tamano
        vector = []
        return promedio, True
    else:
        return 0, False 

def Mostrar(temp_promedio):
    lcd.clear()
    lcd.putstr("Temp: "+"{:.2f} ".format(temp_promedio)+chr(223)+"C")
    
# =============================
# PROGRAMA PRINCIPAL
# =============================
CONFIG_ADC()
CONFIG_LCD()


margen =4
temp_deseada = 35

while True:
    temp, volt, lec = leer_temperatura()
    vector.append(temp)
    temp_promedio, listo = promedio()
    if listo:
        
# # # # # # #         logica
        if temp_promedio < temp_deseada - (margen/2):
            foco.on()
            ventilador.off()
        else if temp_promedio > temp_deseada - (margen/2) and temp_promedio < temp_deseada + (margen/2):
            None
        else if temp_promedio > temp_deseada +(margen/2):
            foco.off()
            ventilador.on()
        
        
        print("temp:{:0.2f}".format(temp_promedio))
        Mostrar(temp_promedio)   # <<< ahora sí muestra en LCD
    sleep(0.01)

            

    
