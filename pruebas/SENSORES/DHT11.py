from machine import Pin
import dht
import time

sensor = dht.DHT11(Pin(4))

time.sleep(1)  

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print("Temperatura:", temp, "°C")
        print("Humedad:", hum, "%")
        print("-----")

    except OSError:
        print("Error de lectura DHT11")

    time.sleep(1)
