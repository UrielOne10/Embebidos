# Control de LED RGB con botones 

## Descripción general
Se implementa el control de un LED RGB tipo NeoPixel mediante 3 botones físicos. El sistema permite alternar entre modos de iluminación al igual que activar el modo de ahorro de energía.
## Funcionalidad del sistema 

| Variable | GPIO | Resistencia Interna | Función |
|:----|:---------|:-------------|:--------------------------|
| b1 | 4 | Pull-down | Enciende el LED en color fijo parpadeante |
b2|3|Pull-down|Inicia una secuencia de arcoiris|
b3|1|Pull-up|Apaga el LED y entra a modo DeepSleep|
n|8|Sin definir|LED RGB incorporado|
## Librerias utilizadas

| Librerias | Función |
|:----|:---------|
| Machine | Pin:Control de los pines del esp, Deepsleep:Control de modo descanso profundo|
| Neopixel | control de LED RGB |
| Time | Control de delays |

```python
from machine import Pin, deepsleep
from neopixel import NeoPixel 
import time
```

Cabe mencionar que para realizar la funcion de los botones se utilizo unicamente el monitoreo constante de el valor del pin. Mientras que el pin 8 es el pin asociado a nuestro RGB, siendo esta asociación del GPIO obligatoria.

## Hardware
- Esp32 C6
- Push button
  
## Software
Metodos usados desde micrpython
- [DeepSleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions)
- [Libreria NeoPixel](https://docs.micropython.org/en/latest/library/neopixel.html)

## Conexión


<img width="400" height="200" alt="image" src="https://github.com/user-attachments/assets/f20e1e9e-9af4-4818-b037-fcffea74df03" />

*Figura 1. Esquema general del sistema.*
