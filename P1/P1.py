from machine import Pin, deepsleep                             #librerias que se necesitan para realizar la práctica
from neopixel import NeoPixel                                  #neopixel:control de LED RGB, Time:Control de delays
import time                                                    #Pin:Control de los pines del esp, Deepsleep:Control de
                                                               #modo descanso profundo
i=0                                                            #variable ocupada para el barrido
p=Pin(8,Pin.OUT)                                               #declaración del pin para control del RGB
n=NeoPixel(p,1)                                                #declaración para el usar el RGB
b1=Pin(3,Pin.IN,Pin.PULL_DOWN)                                #declaración del primer boton fisico usando resistencia pull-down
b2=Pin(4,Pin.IN,Pin.PULL_DOWN)                                #declaración del segundo boton fisico usando resistencia pull-down
b3=Pin(1,Pin.IN,Pin.PULL_UP)                                   #declaración del tercer boton fisico usando resistencia pull-up

arcoiris=[                                                     #arreglo para el barrido de colores
    (255, 0, 0),                                               # Rojo
    (255, 165, 0),                                             # Naranja
    (255, 255, 0),                                             # Amarillo
    (0, 255, 0),                                               # Verde
    (0, 0, 255),                                               # Azul
    (128, 0, 128),                                             # Morado
    (0, 0, 255),                                               # Azul
    (0, 255, 0),                                               # Verde
    (255, 255, 0),                                             # Amarillo
    (255, 165, 0),                                             # Naranja
    (255, 0, 0)                                                # Rojo
    ]

while True:                                                    #Inicio del programa principal
    if b1.value()==1:     #Entrada 1                           #Inicio del uso del boton 1
        while b2.value()==0 and b3.value()==1:                 #Condición para mantener el blink en un bucle infinito
            n[0] = (143, 0, 255)                               #Color escogido: Violeta
            n.write()                                          #Comando para imprimir el color en el RGB
            time.sleep(0.3)                                    #Tiempo dado para que se vea el color (dado en segundos)
            n[0] = (0, 0, 0)                                   #Color para "apagar" el RGB
            n.write()                                          #Comando para imprimir el "color" en el RGB
            time.sleep(0.3)                                    #Tiempo dado para que se vea el "color" (dado en segundos)
    if b2.value() == 1:   #Entrada 2                           #Inicio del uso del boton 2
        time.sleep(0.3)                                        #Da tiempo para un "antirrebote"
        while True:                                            #Condicipon del boton 2
            n[0] = arcoiris[i % len(arcoiris)]                 #Usa un color del arreglo "arcoirirs" y asi mismo se usa para el bucle infinito
            n.write()                                          #Comando para imprimir el color en el RGB
            i += 1                                             #Cambia el color segun el arreglo "arcoiris"
            time.sleep(0.2)                                    # Velocidad de cambio de color
            if b3.value()==0 or b1.value()==1:                 #Condición para terminar el bucle infinito y poner a dormir el esp o regresar al boton 1
                break                                          #Sale del bucle
    if b3.value()==0:     #Entarda 3                            #Inicio del uso del boton 3
        n[0] = (0, 0, 0)                                       #Apaga el RGB
        n.write()                                              #Apaga el RGB
        print("EL ESP32 se puso a mimir zzz")     #Nos imprime en la computadora para saber que el ESP esta en modo deepsleep
        time.sleep(0.2)                                        #Tiempo para entrar en modo deepsleep
        deepsleep()                                            #El esp ya entra en modo sleep