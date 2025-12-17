
from machine import Pin,lightsleep
import time
import neopixel

pines = {}
btns = {
    "b1": {"pin": 3, "pull": Pin.PULL_DOWN, "activo": 1},
    "b2": {"pin": 4, "pull": Pin.PULL_DOWN, "activo": 1},
    "b3": {"pin": 1, "pull": Pin.PULL_UP,   "activo": 0},
}

colores = [0,0,0]
def def_color_fijo():
    colores[0] = 0 if colores[0] else 255
    pines["rgb"][0] = colores
    pines["rgb"].write()
    
fase = 0
def def_secuencia():
    global fase
    step = 10
    if fase == 0:   # R -> Y
        colores[1] += step
        if colores[1] >= 255:
            colores[1] = 255
            fase = 1
    elif fase == 1: # Y -> G
        colores[0] -= step
        if colores[0] <= 0:
            colores[0] = 0
            fase = 2
    elif fase == 2: # G -> C
        colores[2] += step
        if colores[2] >= 255:
            colores[2] = 255
            fase = 3
    elif fase == 3: # C -> B
        colores[1] -= step
        if colores[1] <= 0:
            colores[1] = 0
            fase = 4
    elif fase == 4: # B -> M
        colores[0] += step
        if colores[0] >= 255:
            colores[0] = 255
            fase = 5
    elif fase == 5: # M -> R
        colores[2] -= step
        if colores[2] <= 0:
            colores[2] = 0
            fase = 0
    pines["rgb"][0] = colores
    pines["rgb"].write()
    
def def_sleep():
    global colores
    colores = [0,0,0]
    pines["rgb"][0] = colores
    pines["rgb"].write()
    lightsleep()
funciones = {
    "b1": def_color_fijo,
    "b2": def_secuencia,
    "b3": def_sleep
    }    

def configIO():
    for nombre, cfg in btns.items():
        pines[nombre] = Pin(cfg["pin"], Pin.IN, cfg["pull"])
    pines["rgb"] = neopixel.NeoPixel(Pin(8),1)
configIO()

last_ms = {}
def leerBtn():
    for nombre, cfg in btns.items():
        if pines[nombre].value() == cfg["activo"]:
            return nombre
    return None

btn = None
while True:
    lectura = leerBtn()
    if lectura is not None:
        btn = lectura
        colores = [0,0,0]
    if btn in btns:
        funciones[btn]()
        time.sleep_ms(100)