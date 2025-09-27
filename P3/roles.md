Max
  ADC -> Etapas: 
            Configuracion del ADC
            Lectura
            Proceso : Conversión de valores hexadecimales ( o binarios) a un valor decimal maximo de 3 digitos(centena,decena,unidad)

Antonio
  LCD(I2C) ->  Etapas:
                  Recepcion de datos (por parte del ADC y actuadores)
                  Proceso de conversion a caracteres
                  despliegue de msj de apagado
                  Despliegue de msj de encendido, datos y actuadores

Mike 
  IntExt -> Etapas:
              Definicion de vectores de interrupciones
              Configuraciones
              Logica de banderas (on/off)

Olguin
  LogicaPrincipal -> Etapas:
                      recepcion de bool on/off
                      Logica on/off
                      modo sleep
                      encendido y apagado de actuadores


                  
