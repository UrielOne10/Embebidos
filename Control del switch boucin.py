#librerias
from machine import Pin
import time

# Configurar el botón
button = Pin(22, Pin.IN, Pin.PULL_DOWN)

# Variables globales
estado_anterior = 0
conteo = 0
presiones=0

def eliminacion():
    global estado_anterior, conteo,presiones
    estado_actual = button.value()

    # Si se presiona (flanco de subida)
    if estado_actual == 1 and estado_anterior == 0:
        conteo += 1
        presiones += 1
        print(conteo)

    # Si se suelta (flanco de bajada)
    if estado_actual == 0 and estado_anterior == 1:
        conteo = 0
        print(conteo)
        print("Presiones:", presiones)

    estado_anterior = estado_actual

def int1(pin):  # filtro antirrebote más rápido
    eliminacion()
    time.sleep_ms(50) #itiempo limitado para no vizualizar los rebotes

# Configurar interrupción
button.irq(handler=int1, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

print("Esperando a que el botón se presione...")

while True:
    None
