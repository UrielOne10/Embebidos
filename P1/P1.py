from machine import Pin, Timer               # Importa módulos para manejar pines y temporizadores
import neopixel                              # Importa la librería para controlar NeoPixels
import time                                  # Importa funciones de tiempo

"LED RGB en GPIO8"
p8 = neopixel.NeoPixel(Pin(8), 1)            # Inicializa un NeoPixel en el pin GPIO8 con 1 LED

"Botones en GPIO4, GPIO5 y GPIO6"
p4 = Pin(4, Pin.IN, Pin.PULL_UP)             # Configura el botón en GPIO4 como entrada con pull-up (modo polling)
p5 = Pin(5, Pin.IN, Pin.PULL_UP)             # Configura el botón en GPIO5 como entrada con pull-up (modo interrupción)
p6 = Pin(6, Pin.IN, Pin.PULL_DOWN)           # Configura el botón en GPIO6 como entrada con pull-down (modo interrupción)

"Estado de variables"
parpadeando = False                          # Bandera para saber si el LED verde está parpadeando
led_encendido = False                        # Bandera para saber si el LED está encendido
arcoiris_activado = False                    # Bandera para saber si el modo arcoíris está activo
indice_color = 0                             # Índice actual del color en la lista de arcoíris
boton_activo = None                          # Variable que indica qué botón tiene el control actualmente
estado_p4_anterior = 1                       # Estado anterior del pin p4 para detectar flanco (polling)

"Colores del arcoíris"
colores_arcoiris = [
    (148, 0, 211),                           # Violeta
    (75, 0, 130),                            # Índigo
    (0, 0, 255),                             # Azul
    (0, 255, 0),                             # Verde
    (255, 255, 0),                           # Amarillo
    (255, 127, 0),                           # Naranja
    (255, 0, 0)                              # Rojo
]

"Timer para parpadeo blanco"
def boton_5_timer(timer):                    # Función llamada por el temporizador de parpadeo
    global led_encendido                     # Usa variable global para saber el estado del LED
    if led_encendido:                        # Si el LED está encendido...
        p8[0] = (0, 0, 0)                    # ... lo apaga
        led_encendido = False               # Actualiza el estado
    else:
        p8[0] = (255, 255, 255)                 # Si estaba apagado, lo enciende en verde
        led_encendido = True                # Actualiza el estado
    p8.write()                              # Envía el color al NeoPixel

"Botón p5: Parpadeo verde"
def boton_5(pin):                            # Maneja interrupciones del botón p5
    global parpadeando, boton_activo
    if pin.value() == 0:                     # Si el botón fue presionado (LOW)
        if boton_activo is None:             # Si ningún otro botón está activo
            boton_activo = 'p5'              # Se asigna el control a p5
            timer_5.init(period=500, mode=Timer.PERIODIC, callback=boton_5_timer)  # Inicia parpadeo
            parpadeando = True               # Marca que está parpadeando
    else:
        if boton_activo == 'p5':             # Si el botón liberado era el que tenía el control
            timer_5.deinit()                 # Detiene el temporizador
            parpadeando = False              # Ya no está parpadeando
            boton_activo = None              # Libera el control
            p8[0] = (0, 0, 0)                # Apaga el LED
            p8.write()                       # Actualiza el NeoPixel

"Botón p6: arcoíris"
def boton_6_timer(timer):                    # Función llamada por el temporizador del modo arcoíris
    global indice_color                      # Accede al índice actual del color
    p8[0] = colores_arcoiris[indice_color]   # Muestra el color correspondiente al índice
    p8.write()                               # Actualiza el LED
    indice_color = (indice_color + 1) % len(colores_arcoiris)  # Avanza al siguiente color cíclicamente

def boton_6(pin):                            # Maneja interrupciones del botón p6
    global arcoiris_activado, indice_color, boton_activo
    if pin.value() == 1:                     # Si el botón está presionado (HIGH por pull-down)
        if boton_activo is None:             # Si ningún otro botón tiene el control
            boton_activo = 'p6'              # Toma el control
            indice_color = 0                 # Reinicia la secuencia de colores
            timer_6.init(period=300, mode=Timer.PERIODIC, callback=boton_6_timer)  # Inicia el temporizador
            arcoiris_activado = True         # Marca que el modo arcoíris está activo
    else:
        if boton_activo == 'p6':             # Si el botón liberado era el que tenía el control
            timer_6.deinit()                 # Detiene el temporizador
            arcoiris_activado = False        # Desactiva modo arcoíris
            boton_activo = None              # Libera el control
            p8[0] = (0, 0, 0)                # Apaga el LED
            p8.write()                       # Actualiza el NeoPixel

"Interrupciones solo en p5 y p6"
p5.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=boton_5)  # Configura interrupción para botón p5
p6.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=boton_6)  # Configura interrupción para botón p6

"Timers"
timer_5 = Timer(0)                            # Temporizador 0 para botón p5
timer_6 = Timer(1)                            # Temporizador 1 para botón p6

"Loop principal: polling para el botón p4"
while True:
    estado_p4_actual = p4.value()             # Lee el estado actual del botón p4

    if estado_p4_anterior == 1 and estado_p4_actual == 0:  # Flanco de bajada (botón presionado)
        if boton_activo is None:              # Si ningún botón tiene el control
            boton_activo = 'p4'               # Asigna control a p4
            p8[0] = (100, 0, 0)               # Enciende el LED en rojo
            p8.write()                        # Actualiza el NeoPixel

    elif estado_p4_anterior == 0 and estado_p4_actual == 1:  # Flanco de subida (botón liberado)
        if boton_activo == 'p4':              # Solo si p4 tenía el control
            boton_activo = None               # Libera el control
            p8[0] = (0, 0, 0)                 # Apaga el LED
            p8.write()                        # Actualiza el NeoPixel

    estado_p4_anterior = estado_p4_actual     # Guarda el estado actual para la siguiente comparación
    time.sleep(0.01)                          # Pequeño retardo para evitar rebotes (10 ms)
