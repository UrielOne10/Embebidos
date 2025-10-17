from machine import ADC, Pin, lightsleep
from time import sleep

VREF = 3.3
ADC_MAX = 4095
UMBRAL_V = 2.0
UMBRAL_RAW = int((UMBRAL_V / VREF) * ADC_MAX)

def leer_adc():
    adc = ADC(Pin(0))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)
    lectura = adc.read()
    voltaje = (lectura * VREF) / ADC_MAX
    return lectura, voltaje

print(f"Umbral de activación: {UMBRAL_V:.2f} V (≈ {UMBRAL_RAW})")

while True:
    lectura, voltaje = leer_adc()
    print("Voltaje: {:.2f} V".format(voltaje))

    if lectura >= UMBRAL_RAW:
        print("⚡ Umbral superado → ¡Despierto!")
        sleep(1)
    else:
        print("💤 Durmiendo (light sleep)...")
        lightsleep(1000)

