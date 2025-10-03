from machine import ADC, Pin
import time
import math
# Configuración del ADC en GPIO0 (ADC1_CH0)
adc = ADC(Pin(0))  

# Configurar la atenuación a 0dB → rango ~0 a 1.1V
adc.atten(ADC.ATTN_0DB)

# Configurar resolución de 12 bits (0–4095)
adc.width(ADC.WIDTH_12BIT)

VREF = 1.1  # referencia en voltios
ADC_MAX = 4095

def leer_temperatura():
    lectura = adc.read()              # Guardamos el valor de la lectura en una variable
    voltaje = (lectura*VREF)/ADC_MAX  # Conversion a voltaje (usando el 1.1 de referencia)
    temperatura = ((voltaje*1000)/10)    # Conversion a temperatura
    return temperatura, voltaje,lectura

vector=[]
tamano=10

while True:
    temp, v, l = leer_temperatura()
    vector.append(temp*3	)
    if len(vector) == tamano:
        promedio=math.sqrt(sum(x**2 for  x in vector))/tamano
        print(" Temp = {:.2f} °C".format( promedio))
        vector=[]
    
    time.sleep(0.1) 