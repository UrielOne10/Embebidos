## Implementacion del protocolo I2C del ESP32

## Descripción general
Se ingresara al modo ahorro de energia, al mismo tiempo saldra del mismo modo por medio de botones analogicos. Esto a su vez se tendra interactuando la patalla LCD para la vizualizacion del modo en el que se encuentra.
## Funcionalidad del sistema
| Variable | GPIO | Resistencia Interna | Función |
|:----|:----|:----|:----|
|btn1|1|PULL UP|Entrara al modo LIGHTSLEEP|
|btn2|4|PULL DOWN|Movimiento en la pantalla LCD|
|i2c|7 y 6|4.7k ohms|Mandar informaciòn a la pantalla LCD|
## Funcionalidad del sistema de gestos
tendrá 3 configuraciones basadas en la cantidad de pulsaciones en un tiempo determinado
| Pulsos | Función |
|:----|:----|
| 1 | El mensaje realiza un corrimiento de izquierda a derecha |  
| 2 | El mensaje realiza un corrimiento de derecha a izquierda |  
| 3 | El mensaje se queda quieto |  
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
Cabe mencionar que, el mismo "btn1" mantendra un mensaje estatitco con el cual se sabra si salio del mismo modo LIGHTSLEEP. Con ello los pines 7 y 8 estan predeterminados para el modo i2c de la pantalla LCD con el ESP32, siendo su comunicaiòn SCL Y SDA.

## Hardware
- Esp32 C6
- Push button
- Pantalla LCD
## Software
Metodos usados desde micropython
- [DeepSleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions)
- [Libreria NeoPixel](https://docs.micropython.org/en/latest/library/neopixel.html)
- [Libreria LCD](https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-lcd-i2c)
- [Interrupciones Ext]
- [Antirrebote]
## Conexión
<img width="400" height="200" alt="image" src="https://github.com/UrielOne10/Embebidos/blob/c149b894bc3d42477683f97f84cab78171ba2865/P2/Pror.png" />

*Figura 1. Esquema general del sistema.*
