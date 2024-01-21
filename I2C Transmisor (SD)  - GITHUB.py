from machine import Pin, SPI, I2C
from sdcard import SDCard
from uos import VfsFat, mount
import time
import utime

# Inicializar el bus I2C
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
direccion = 0x41


#SPI
cs = Pin(5)
spi = SPI(1,
          baudrate=1000000,
          polarity=0,
          phase=0,
          sck = Pin(2),
          mosi = Pin(3),
          miso = Pin(4))
#SD
sd = SDCard(spi, cs)
vol = VfsFat(sd)
mount(vol, "/sd")

datos = []
cont = 0


#Recopilar datos
for ruta in listdir("/sd"):
    if cont >= 14:
        break
    if ruta[:7] == "Alertas":
        archivo = open("/sd/"+ruta, "r")
        aux = archivo.read()
        archivo.close()

        cruces = 0

        for linea in aux.split("\n"):
            if linea == "":
                continue
            cruces += int(linea[:2])
        
        datos.insert(0,cruces)
        cont += 1


def leer():
    try:
        with open('Alertas.txt', 'r') as file:
            lineas = file.readlines()
            datos = [linea.split(':')[-1].strip() for linea in lineas]  # Utiliza list comprehension para obtener los números
            return datos
    except FileNotFoundError:
        print("El archivo 'Alertas.txt' no se encontró.")
        return []  # Devuelve una lista vacía en caso de error
    except Exception as e:
        print("Ocurrió un error al intentar leer el archivo:", str(e))
        return []  # Devuelve una lista vacía en caso de error


alertas = leer()
for alerta in alertas:
    message_bytes = bytearray(str(alerta + "*"), "utf-8")
    i2c.writeto(direccion, message_bytes)
    utime.sleep_ms(1)