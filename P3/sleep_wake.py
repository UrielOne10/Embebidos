# from machine import Pin, lightsleep, DEEPSLEEP,SLEEP
# from time import sleep
# # Configurar pin de entrada con wake-up
# boton = Pin(2, Pin.IN, Pin.PULL_UP,hold = True)
# boton.irq(trigger=Pin.IRQ_FALLING, wake = SLEEP|DEEPSLEEP)
# 
# print("Entrando en light sleep...")
# sleep(0.1)
# lightsleep()  # o deepsleep()
# print("Despertó!")
#

# from machine import Pin, lightsleep
# from time import sleep
# 
# # Usa un pin adecuado (GPIO4 o GPIO9, NO GPIO2)
# boton = Pin(4, Pin.IN, Pin.PULL_UP)
# 
# def despertar(boton):
#     print("¡Interrupción detectada, despertando!")
# 
# # Configura la interrupción ANTES de entrar en sueño
# boton.irq(trigger=Pin.IRQ_FALLING, handler=despertar)
# 
# print("Entrando en light sleep...")
# sleep(0.1)
# lightsleep()
# print("Despertó del light sleep")

from machine import Pin, deepsleep, DEEPSLEEP

# Botón conectado de GPIO9 a GND
boton = Pin(10, Pin.IN, Pin.PULL_UP,hold=True)
boton.irq(trigger=Pin.IRQ_FALLING, wake=DEEPSLEEP)

print("Entrando en deep sleep...")
deepsleep()
print("saliendo")
