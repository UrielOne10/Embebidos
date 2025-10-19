# Control de LED RGB con botones 

## Descripción general
Se implementa el control de un LED RGB tipo NeoPixel mediante 3 botones físicos. El sistema permite alternar entre modos de iluminación al igual que activar el modo de ahorro de energía.
## Funcionalidad del sistema 

| Boton | GPIO | Resistencia Interna | Función |
|:----|:---------|:-------------|:--------------------------|
| b1 | 10 | Pull-down | Enciende el LED en color fijo parpadeante |
b2|11|Pull-down|Inicia una secuencia de arcoiris|
b3|1|Pull-up|Apaga el LED y entra a modo DeepSleep|

Cabe mencionar que para realizar la funcion de los botones se utilizo unicamente el monitoreo constante de el valor del pin.
