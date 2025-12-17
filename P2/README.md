## Implementacion del protocolo I2C del ESP32

## Descripción general
Se ingresara al modo ahorro de energia, al mismo tiempo saldra del mismo modo por medio de botones analogicos. Esto a su vez se tendra interactuando la patalla LCD para la vizualizacion del modo en el que se encuentra.
## Funcionalidad del sistema
| Variable | GPIO | Resistencia Interna | Función |
|:----|:----|:----|:----|
|btn1|1|PULL UP|Entrara al modo LIGHTSLEEP|
|btn2|4|PULL DOWN|Configuracion de la pantalla LCD (multigestos)|
|i2c|7 y 6|4.7k ohms|Mandar informaciòn a la pantalla LCD|

## Dispositivos I2C
Los pines 7 y 6 en la placa ESP32C6 son SCL y SDA respectivamente, por lo tano primero se define al maestro para que empiece a escanear dispositivos, ya definidos, marcamos al esclavo para que funciones correctamente en base a la libreria de LCD
```python
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
```

## Funcionalidad del sistema de gestos
tendrá 3 configuraciones basadas en la cantidad de pulsaciones en un tiempo determinado
| Pulsos | Función |
|:----|:----|
| 1 | El mensaje realiza un corrimiento de izquierda a derecha |  
| 2 | El mensaje realiza un corrimiento de derecha a izquierda |  
| 3 | El mensaje se queda quieto 
 A traves de un timer con un periodo de 1 seg 
 ```python
 t1.init(mode=Timer.PERIODIC,period=1000,callback=rstConteo)
 ```
Se va contando la cantidad de pulsos hechos. El callback resetea dicho conteo.

## Funcionalidad del sistema antirrebotes
Para evitar entradas rebote por parte de la acción mecánica del boton, se adapto una funcion de antirrebote

```python
def antirrebote(nombre, intervalo_ms=500):
    global last_ms
    now  = time.ticks_ms()
    last = last_ms.get(nombre, 0)
    if time.ticks_diff(now, last) < intervalo_ms:
        return False
    last_ms[nombre] = now
    return True
```
Esta a traves de un diccionario donde se le da un nombre a cada variable de la que queremos detectar antirrebotes nos entrega un True o False, en funcion del tiempo intervalo_ms propuesto


## Hardware
- Esp32 C6
- Push button
- Pantalla LCD
## Software
Metodos usados desde micropython
- [DeepSleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions)
- [Libreria NeoPixel](https://docs.micropython.org/en/latest/library/neopixel.html)
- [Libreria LCD](https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-lcd-i2c)
- [Interrupciones Ext](https://docs.micropython.org/en/latest/library/machine.Pin.html)
- [Antirrebote](https://docs.micropython.org/en/latest/library/time.html#module-time)
## Conexión
<img width="400" height="200" alt="image" src="https://github.com/UrielOne10/Embebidos/blob/c149b894bc3d42477683f97f84cab78171ba2865/P2/Pror.png" />

*Figura 1. Esquema general del sistema.*
