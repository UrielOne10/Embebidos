from machine import Pin
import time

pin_uno = Pin(1, Pin.IN, Pin.PULL_DOWN)

estado = False

def cambiar_estado(pin):
    global estado    
    estado = not estado   
    print(estado)

pin_uno.irq(handler=cambiar_estado, trigger=Pin.IRQ_FALLING)

while True:
    print(estado)
    time.sleep(1)
