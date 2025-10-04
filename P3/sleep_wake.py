import esp32
from machine import Pin, lightsleep

# Botón en GPIO 4
btn = Pin(4, Pin.IN, Pin.PULL_UP)

# Configura wake-up por EXT0
# level=esp32.WAKEUP_ALL_LOW → despierta cuando el pin está LOW
esp32.wake_on_ext0(pin=btn, level=esp32.WAKEUP_ALL_LOW)

print("Entrando en lightsleep, presiona el botón para despertar...")
lightsleep()
print("¡Despertó por el botón!")