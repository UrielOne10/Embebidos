#importar librerias
from machine import Pin
import time

# Configurar el botón
button = Pin(22, Pin.IN, Pin.PULL_DOWN)

# Variables
estado_anterior = 0  # Estado anterior del botón

print("Esperando a que el botón se presione...")

while True:
    
    #Declarando el estado actual en el quwe se encuentar el boton
    estado_actual = button.value()

    # Detectar cambio de 0 → 1, comparandolo con el valor anterior y el actual
    if estado_actual == 1 and estado_anterior == 0:
        print(1)
        time.sleep(0.05)  # Anti-rebote (50 ms)

    # Detectar cambio de 1 → 0 (soltado)
    elif estado_actual == 0 and estado_anterior == 1:
        print(0)
        time.sleep(0.05)  # Anti-rebote

    # Actualizar el estado anterior
    estado_anterior = estado_actual

