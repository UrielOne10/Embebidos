from machine import ADC, Pin
from time import sleep

adc = ADC(Pin(0))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

V= 5
ADC_MAX = 4095

while True:
    lectura = adc.read()
    voltaje = (lectura * V) / ADC_MAX
    print("Voltaje: {:.2f} V".format(voltaje))
    sleep(1)
