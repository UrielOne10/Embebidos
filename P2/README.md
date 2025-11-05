## Implementacion del protocolo I2C del ESP32

## Descripción general
Se ingresara al modo ahorro de energia, al mismo tiempo saldra del mismo modo por medio de botones analogicos. Esto a su vez se tendra interactuando la patalla LCD para la vizualizacion del modo en el que se encuentra.
## Funcionalidad del sistema
| Variable | GPIO | Resistencia Interna | Función |
|:----|:----|:----|:----|
|btn1|1|PULL UP|Saldra del modo LIGHTSLEEP|
|btn1rising|1|PULL UP|Entrara al modo LIGHTSLEEP|
|btn2|4|PULL DOWN|Movimiento en la pantalla LCD|
|i2c|7 y 6|7k ohms|Mandar informaciòn a la pantalla LCD|

Cabe mencionar que, el mismo "btn1" mantendra un mensaje estatitco con el cual se sabra si salio del mismo modo LIGHTSLEEP. A su vez que, el "btn2" mandara los mensajes dependiendo del nùmero de pulsaciones que se esten ejecutando con el boton analogico. Con ello los pines 7 y 8 estan predeterminados para el modo i2c de la pantalla LCD con el ESP32, siendo su comunicaiòn SCL Y SDA.

## Hardware
- Esp32 C6
- Push button
- Pantala LCD
## Software
Metodos usados desde micropython
- [DeepSleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions)
- [Libreria NeoPixel](https://docs.micropython.org/en/latest/library/neopixel.html)
- [Libreria LCD](https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-lcd-i2c)
## Conexión
<img width="400" height="200" alt="image" src="https://github.com/UrielOne10/Embebidos/blob/c149b894bc3d42477683f97f84cab78171ba2865/P2/Pror.png" />

*Figura 1. Esquema general del sistema.*
