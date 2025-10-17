from machine import Pin, lightsleep, SLEEP,DEEPSLEEP
from time import sleep_ms
from neopixel import NeoPixel

# Estado global
dormir = False

# Handler para el botón en GPIO4
def inter(pin):
    global dormir
    dormir = not dormir
    print("Cambio de estado:", "Dormir" if dormir else "Despierto")

# Configurar el botón en GPIO4 como wake source
PIN4 = Pin(4, Pin.IN, Pin.PULL_UP)
PIN4.irq(trigger=Pin.IRQ_FALLING, wake=SLEEP|DEEPSLEEP, handler=inter)


PIN5 = Pin(5, Pin.IN, Pin.PULL_DOWN)


pinrgb = Pin(8, Pin.OUT)
RGB = NeoPixel(pinrgb, 3)

while True:
    if dormir:
        print("Entrando en light sleep...")
        lightsleep()  # Aquí el ESP32-C6 duerme hasta evento en PIN4
        print("Desperté del light sleep")
        dormir = False   # Resetear el estado
    else:
        # Animación simple en NeoPixel
        for i in range(32):
            RGB[0] = (i * 8, i * 2, i * 3)
            RGB.write()
            sleep_ms(20)
