import machine
import dht
import time

datos = machine.Pin(4) # Configuracion del pin de datos
sensor = dht.DHT11(datos) # Crea la instancia del sensor

print("Iniciando lectura de datos...")

while True:
    try:
        time.sleep(2) # Estabilizacion del DTH11
        sensor.measure() # Realiza la Medicion
        temperatura = sensor.temperature() # Celsius
        humedad = sensor.humidity()    # Porcentaje %
        
        print(f"Temperatura: {temperatura}°C | Humedad: {humedad}%")
        
    except OSError as e:
        print("Error al leer el sensor. Revisa las conexiones.")