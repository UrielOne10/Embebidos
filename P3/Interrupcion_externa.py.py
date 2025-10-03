from machine import Pin
import time

pin_uno = Pin(1, Pin.IN, Pin.PULL_DOWN)

estado = False
last_time = 0

def cambiar_estado(pin):
    global estado, last_time
    #Devuelve el número de milisegundos que han pasado desde que el ESP se encendió
    now = time.ticks_ms()
    if time.ticks_diff(now, last_time) > 200: 
        estado = not estado
        print(estado)
        last_time = now

pin_uno.irq(handler=cambiar_estado, trigger=Pin.IRQ_FALLING)

while True:
    time.sleep(0.2)
