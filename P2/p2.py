from machine import Pin, I2C, Timer, lightsleep
from lcd.i2c_lcd import I2cLcd
from time import sleep,sleep_ms

# # INSTANCIA DE COMUNICACION I2C
i2c = I2C(scl=7,sda=6,freq=400000)

# Escanea dispositivos
devices = i2c.scan()

if devices:
    print("Dispositivos encontrados:", len(devices))
    for d in devices:
        print("I2C device encontrado en dirección:", hex(d))
else:
    print("No se encontraron dispositivos I2C")
    
miLcd=I2cLcd(i2c,0x27,2,16)
miLcd.move_to(0, 0)


msj = "SALUDOS"
lcd_width = 16
derecha = False  
hibernar=False
barrido=True
contador=0
t1 = Timer(1)
estadot1=False
def activarTimer():
    t1.init(mode=Timer.PERIODIC,period=525,callback=rstConteo)
    global estadot1
    estadot1=True
def desactivarTimer():
    t1.deinit()
    global estadot1
    estadot1=False
    
# # DECLARACION DEF INTERRUPCIONES
def interrupciones1(btn1):
    sleep_ms(100)
    global derecha, barrido, contador
    if not estadot1:
        activarTimer()
    contador+=1
    
def delayRising(btn1rising):
    sleep(40)
    
def rstConteo(t1):
    global contador,derecha,barrido
    if contador==1:
        derecha=True
        print("1")
    elif contador==2:
        derecha=False
        print("2")
    elif contador>=4:
        barrido = not barrido
        print("3")
    contador=0
    desactivarTimer()
    
def interrupciones2(btn2):
    global hibernar
    hibernar=True
    print("hola")

# # # # # VARIABLES HW
btn1 = Pin(1,Pin.IN,Pin.PULL_UP)
btn1rising = Pin(1,Pin.IN,Pin.PULL_UP)
btn1rising.irq(delayRising,Pin.IRQ_RISING)
btn1.irq(interrupciones1,Pin.IRQ_FALLING)
btn2 = Pin(4,Pin.IN,Pin.PULL_DOWN)
btn2.irq(interrupciones2,Pin.IRQ_RISING)


msj_padded = " " * lcd_width + msj + " " * lcd_width

while True:
    if hibernar:
        miLcd.clear()
        miLcd.move_to(0,0)
        miLcd.putstr("buenas noches")
        sleep_ms(50)
        lightsleep()
    else:
        if barrido:
            if derecha:
                # Barrido derecha a izquierda
                for i in range(len(msj_padded) - lcd_width + 1):
                    display_text = msj_padded[i:i + lcd_width]
                    miLcd.move_to(0, 0)
                    miLcd.putstr(display_text)
                    sleep_ms(100)
            else:
                # Barrido izquierda a derecha
                for i in range(len(msj_padded) - lcd_width, -1, -1):
                    display_text = msj_padded[i:i + lcd_width]
                    miLcd.move_to(0, 0)
                    miLcd.putstr(display_text)
                    sleep_ms(100)
        else:
            miLcd.move_to(0,0)
            miLcd.putstr(msj)
