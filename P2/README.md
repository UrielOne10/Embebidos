# Implementacion del protocolo I2C del ESP32

# Descripción general
Se ingresara al modo ahorro de energia, al mismo tiempo saldra del mismo modo por medio de botones analogicos. Esto a su vez se tendra interactuando la patalla LCD para la vizualizacion del modo en el que se encuentra.
# Funcionalidad del sistema
| Variable | GPIO | Resistencia Interna | Función |
|:----|:----|:----|:----|
|btn1|1|PULL UP|Hacer un barrido hacia el lado derecho|
|btn1rising|1|PULL UP||
|btn2|4|PULL DOWN|Mostrar un mensaje "Hola", desactivar el modo "sleep"|


# Hardware
- Esp32 C6
- Push button
- Pantala LCD
# Software
Metodos usados desde micropython
- [DeepSleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions)
# Conexión
