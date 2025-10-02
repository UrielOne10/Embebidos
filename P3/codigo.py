from machine import sleep, SoftI2C, Pin, ADC
from utime import ticks_diff, ticks_ms
from max30102._init_ import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import time
import math


# Configuración del ADC en GPIO0 (ADC1_CH0)
adc = ADC(Pin(0))  
# Configurar la atenuación a 0dB → rango ~0 a 1.1V
adc.atten(ADC.ATTN_0DB)
# Configurar resolución de 12 bits (0–4095)
adc.width(ADC.WIDTH_12BIT)

vector=[]
tamano=10

VREF = 1.1  # referencia en voltios
ADC_MAX = 4095

#lectura del ADC y su conversion a temperatura y voltaje
def leer_temperatura():
    lectura = adc.read()              # Guardamos el valor de la lectura en una variable
    voltaje = (lectura*VREF)/ADC_MAX  # Conversion a voltaje (usando el 1.1 de referencia)
    temperatura = ((voltaje*1000)/10)    # Conversion a temperatura
    return temperatura, voltaje,lectura


    def agregarElemento(self, dato):
        self.lista.append(dato)

    def norma2(self):
        if len(self.lista) >= self.ventana:
            prom = (math.sqrt(sum(x**2 for x in self.lista))) / len(self.lista)
            spo2 = 0.12698*prom +79.82  
            self.lista.clear()
            return spo2
        else:
            return None


# ----------------- Programa Principal -----------------
def main():
    i2c = SoftI2C(sda=Pin(6), scl=Pin(7), freq=400000)
    sensor = MAX30102(i2c=i2c)

    if sensor.i2c_address not in i2c.scan():
        print("Sensor not found.")
        return
    elif not sensor.check_part_id():
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    sensor.setup_sensor()
    sensor.set_sample_rate(3200)
    sensor.set_fifo_average(32)
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
    
    #actual_acquisition_rate = int(3200 /4)
    monitor = HeartRateMonitor()
    """
    hr_monitor = HeartRateMonitor(sample_rate=actual_acquisition_rate,
                                  window_size=int(actual_acquisition_rate * 3))
                                  """

    ventana_red = []
    ventana_ir = []
    ventana_mR = []
    ventana_mIR= []
    x=0
    VENTANA_SIZE = 10  # muestras para SpO2
    energia = 0
    valle = 1
    umbral = 100
    
    Energia1=0
    Energia2=0
    zeta=0
    Lista_energia=[]
    cuadrados=[]
    suma_cuadrados=0
    SPO2=0
    promedio=None
    print("Iniciando adquisición: RED, IR, BPM, SpO2")

    while True:
        #Imprision de la temperatura
         temp, v, l = leer_temperatura()
        vector.append(temp*3)
        if len(vector) == tamano:
            promedio=math.sqrt(sum(x**2 for  x in vector))/tamano
            print(" Temp = {:.2f} °C".format( promedio)) #imprimimos promedio de temperatura
            vector=[] #limpia vector
        time.sleep(0.1) 

        sensor.check()
        if sensor.available():
            red = sensor.pop_red_from_storage()
            ir = sensor.pop_ir_from_storage()

            # Agregar datos a la ventana de SpO2
            ventana_red.append(red)
            ventana_ir.append(ir)
            
            monitor.agregarElemento(red)
            Spo2=monitor.norma2()
            
            if len(ventana_red) > VENTANA_SIZE:
                ventana_red.pop(0)
                ventana_ir.pop(0)
            
            
            
            if(Spo2 is not None):
                print("RED: {:04d}, Promedio: {:0.2f}".format(red,Spo2))

            else:
                None
                print("RED: {:04d}, Promedio: ------".format(red))
            

if __name__ == "__main__":
    main()

