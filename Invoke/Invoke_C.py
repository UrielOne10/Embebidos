import machine
import time

# Direcciones de registros del ESP32-C6 (Arquitectura RISC-V)
# Registro para poner pines en ALTO y BAJO
GPIO_OUT_W1TS = 0x60091008 
GPIO_OUT_W1TC = 0x6009100C
PIN_8_MASK = 1 << 8

@micropython.viper
def blink_fast_c_style(cycles: int):
    # Creamos punteros a los registros de hardware
    set_reg = ptr32(GPIO_OUT_W1TS)
    clr_reg = ptr32(GPIO_OUT_W1TC)
    
    for i in range(cycles):
        set_reg[0] = PIN_8_MASK  # Equivale a digitalWrite(8, HIGH) en C
        # Un pequeño delay manual
        for _ in range(1000000): pass
        
        clr_reg[0] = PIN_8_MASK  # Equivale a digitalWrite(8, LOW) en C
        for _ in range(1000000): pass

# Configurar el pin antes de usar Viper
p8 = machine.Pin(8, machine.Pin.OUT)

print("Parpadeo")
blink_fast_c_style(10)