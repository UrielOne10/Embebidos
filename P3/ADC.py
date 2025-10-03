from machine import ADC, Pin
import time
import math


# Configuración del ADC en GPIO0 (ADC1_CH0)
adc = ADC(Pin(0))  

# Configurar la atenuación a 0dB → rango ~0 a 1.1V
adc.atten(ADC.ATTN_0DB)

# Configurar resolución de 12 bits (0–4095)
adc.width(ADC.WIDTH_12BIT)

#varaibles y/o constantes globales
VREF = 1.1  # referencia en voltios
ADC_MAX = 4095
vector=[]
tamano=100

#funciones
def leer_temperatura():
    lectura = adc.read()              # Guardamos el valor de la lectura en una variable
    voltaje = (lectura*VREF)/ADC_MAX  # Conversion a voltaje (usando el 1.1 de referencia)
    temperatura = ((voltaje*1000)/10)    # Conversion a temperatura
    return temperatura, voltaje,lectura

def promedio():
    global vector
    if len(vector) == tamano:
        #promedio=math.sqrt(sum(x**2 for  x in vector))/tamano
        promedio = sum(vector)/tamano
        vector=[]
        return promedio, True
    else:
       return 0, False
    


while True:
    temp, v, l = leer_temperatura()
    vector.append(temp)
    temp_promedio,jala=promedio()
    if jala == False:
        None
    else:
        print("Temp={:0.1f}".format(temp_promedio))
    time.sleep(0.01)


