import machine
import dht
import time

datos = machine.Pin(4)
sensor = dht.DHT22(datos) 

print("Iniciando lectura de datos...")

while True:
    try:
        time.sleep(2) # Estabilizacion del DTH22
        sensor.measure() # Realiza la Medicion
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        
        print(f"Temperatura: {temperatura:.1f}°C | Humedad: {humedad:.1f}%")
        
    except OSError as e:
        print("Error al leer el sensor. Revisa las conexiones.")