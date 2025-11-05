## Implementacion de sensores analogicos en el ESP32
## Descripción general
Se obendran señales externas mediante los sensores analogicos, por medio de una clasificacion binaria. Esto estara relacionado a un umbral que estara activando o desactivando un actuador fisico.
## Funcionalidad del sistema
| Variable | GPIO | Resistencia Interna | Función |
|:----|:----|:----|:----|
| i2c | 7 y 8 | 7k ohms| |
| Foco | 3 | Sin especificaciones  | |
| Ventilador | 2 | Sin especificaciones | |
| BtnEstado | 1 | PULL-DOWN | |

## Hardware
- LCD con modulo I2C 
- Foco 127VAC 
- LM35 
- Ventilador 
- ESP32 C6
## Software
- [DeepSleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions)
- [Libreria NeoPixel](https://docs.micropython.org/en/latest/library/neopixel.html)
- [Libreria LCD](https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-lcd-i2c)
- [Pantalla OLED](https://www.esploradores.com/oled_ssd1306/)
## Conexión
<img width="400" height="200" alt="image" src="https://github.com/UrielOne10/Embebidos/blob/bba406a42e5623f357f35ab4b759f97e19c8eb98/P3/Circuito_3.png" />

*Figura 1. Esquema general del sistema.*
