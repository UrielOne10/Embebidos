import machine
import time

# Configuración del Pin 8
p8 = machine.Pin(8, machine.Pin.OUT)
MASK = 1 << 8
ADDR_SET = 0x60091008
ADDR_CLR = 0x6009100C

@micropython.asm_rv
def led_on(r0, r1): # r0 = dirección, r1 = máscara
    sw(r1, 0(r0))   # "Store Word": guarda el bit en la dirección de memoria

@micropython.asm_rv
def led_off(r0, r1):
    sw(r1, 0(r0))

while True:
    led_on(ADDR_SET, MASK)
    print("Encendido")
    time.sleep(1)
    
    led_off(ADDR_CLR, MASK)
    print("Apagado")
    time.sleep(1)