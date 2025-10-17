from machine import Pin
import time

# # # # # # variables INT EXT
estado = False
# # # # # # vectores de interrupciones
def cambiar_estado(pin):
    global estado
    estado = not estado
# # # # # # config Interrupciones externas
pin_uno = Pin(1, Pin.IN, Pin.PULL_DOWN)
pin_uno.irq(handler=cambiar_estado, trigger=Pin.IRQ_FALLING)


# # # # # # APOYO
salida = Pin(5,Pin.OUT)

while True:
    salida.value(estado)    
