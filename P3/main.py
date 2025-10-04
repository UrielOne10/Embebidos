from machine import ADC, Pin
from time import sleep
import math

# # # # # # # # # # # # # # # # # # # # # # # # #  INT EXT
# # # variables
estado = False
# # # vectores de interrupciones
def cambiar_estado(pin):
    global estado
    estado = not estado
# # # config Interrupciones externas
BtnEstado = Pin(1, Pin.IN, Pin.PULL_DOWN)
BtnEstado.irq(handler=cambiar_estado, trigger=Pin.IRQ_FALLING)

# # # # # # # # # # # # # # # # # # # # # # # # # ADC
adc = ADC(Pin(0))  
#atenuación rango ~0 a 1.1V
adc.atten(ADC.ATTN_0DB)
#resolución de 12 bits (0–4095)
adc.width(ADC.WIDTH_12BIT)
#varaibles y/o constantes globales
VREF = 1.1
ADC_MAX = 4095
vector=[]
tamano=100
#funciones
def leer_temperatura():
    lectura = adc.read()             
    voltaje = (lectura*VREF)/ADC_MAX  
    temperatura = ((voltaje*1000)/10)   
    return temperatura, voltaje,lectura

def promedio():
    global vector
    if len(vector) == tamano:
        #promedio=math.sqrt(sum(x**2 for  x in vector))/tamano
        promedio = sum(vector)/tamano
        vector=[]
        return promedio
    else:
       return 0
    
while 1:
    if estado:
        temp,volt,lec=leer_temperatura()
        vector.append(temp)
        temp = promedio()
        if temp != 0:
            print("temp:{:0.2f}".format(temp))
        sleep(0.1)
    