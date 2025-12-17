from machine import Pin, I2C, Timer, lightsleep
from lcd.i2c_lcd import I2cLcd
from time import sleep,sleep_ms
import time

msj = "SALUDOS"
lcd_width = 16
derecha = False  
hibernar=False
barrido=True
contador=0
t1 = Timer(1)
estadot1=False

def activarTimer():
    global estadot1
    estadot1=True
    t1.init(mode=Timer.PERIODIC,period=1000,callback=rstConteo)
def desactivarTimer():
    global estadot1
    estadot1=False
    t1.deinit()
    
def rstConteo(t1):
    global contador,derecha,barrido
    miLcd.clear()
    barrido = True
    if contador==1:
        derecha=True
        print("1")
    elif contador==2:
        derecha=False
        print("2")
    elif contador>=3:
        barrido = False
        print("3")
    contador=0
    desactivarTimer()
    
last_ms = {}
def antirrebote(nombre, intervalo_ms=200):
    global last_ms
    now  = time.ticks_ms()
    last = last_ms.get(nombre, 0)
    if time.ticks_diff(now, last) < intervalo_ms:
        return False
    last_ms[nombre] = now
    return True
estadot1 = False

def def_mov_lcd(pin):
    global derecha, barrido, contador
    if antirrebote("b1"):
        if not estadot1:
            activarTimer()
        contador+=1
    
def def_sleep():
    global hibernar
    hibernar=True
    print("hola")
    
pines = {}
btns = {
    "b1": {"pin": 1, "pull": Pin.PULL_UP,"trigger": Pin.IRQ_FALLING,"handler":def_sleep},
    "b2": {"pin": 4, "pull": Pin.PULL_DOWN, "trigger": Pin.IRQ_FALLING,"handler":def_mov_lcd}
}

def configIO():
    for nombre, cfg in btns.items():
        pines[nombre] = Pin(cfg["pin"], Pin.IN, cfg["pull"])
        valor_trigger = cfg["trigger"]
        valor_def = cfg["handler"]
        pines[nombre].irq(handler=valor_def, trigger=valor_trigger)
configIO()

def config_i2c():
    i2c = I2C(scl=7,sda=6,freq=400000)
    devices = i2c.scan()
    if devices:
        print("Dispositivos encontrados:", len(devices))
        for d in devices:
            print("I2C device encontrado en dirección:", hex(d))
    else:
        print("No se encontraron dispositivos I2C")  
    pines["lcd"]=I2cLcd(i2c,0x27,2,16)
config_i2c()

msj_padded = " " * lcd_width + msj + " " * lcd_width

miLcd = pines["lcd"]
i = 0
while True:
    if hibernar:
        miLcd.clear()
        miLcd.move_to(0,0)
        miLcd.putstr("buenas noches")
        sleep_ms(50)
        lightsleep()
    else:
        
        if barrido:
            maximo = len(msj_padded) - lcd_width
            if derecha:
                i = (i+1)%maximo
            else:
                i = (i-1)%maximo
            display_text = msj_padded[i:i + lcd_width]
            miLcd.move_to(0, 0)
            miLcd.putstr(display_text)
            sleep_ms(200)
        else:
            miLcd.move_to(0,0)
            display_text = msj_padded[i:i + lcd_width]
            miLcd.putstr(display_text)
            sleep_ms(200)
