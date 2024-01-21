from i2cSlave import i2c_slave
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# Inicializar la pantalla OLED
WIDTH = 128
HEIGHT = 64
i2c_oled = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c_oled)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
s_i2c = i2c_slave(0, sda=0, scl=1, slaveAddress=0x41)

ciclo = 2
tiempo = time.time()
lista = []

# Función para graficar
def formato_grafica(alertas):
    global tiempo, lista, X_prev, Y_prev  # Declarar variables globales

    # Limpiar la pantalla OLED
    oled.fill(0)

    # Obtener la fecha y hora actuales
    current_time = time.localtime()
    template_fecha = "{:02d}/{:02d}/{:04d}".format(current_time[2], current_time[1], current_time[0])
    template_hora = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])

    # Mostrar la fecha y hora en la pantalla OLED
    oled.text(template_fecha, 0, 0)
    oled.text(template_hora, 0, 9)
    oled.hline(0, 16, 128, 1)  # Línea divisoria

    # Verificar si es tiempo de actualizar la lista y la gráfica
    if tiempo + ciclo < time.time():
        lista.insert(0, alertas)  # Agregar alerta a la lista
        tiempo = time.time()  # Actualizar el tiempo
    for k in range(len(lista)):
        X = 132 - (k + 1) * 8
        Y = int(60 - lista[k] * 5) if tiempo + ciclo < time.time() else int(60 - lista[k])
        oled.pixel(X, Y, 1)  # Dibujar píxel en la pantalla OLED
        if k > 0:
            oled.line(X_prev, Y_prev, X, Y, 1)  # Dibujar línea entre píxeles
        X_prev, Y_prev = X, Y

    oled.show()  # Mostrar cambios en la pantalla OLED

def leer ():
    aux = ""
    while True:
        data = chr(int(hex(s_i2c.get()),16))
        if data == "*":
            return aux
        aux += data
            

# Bucle principal
while True:
    alert = leer()
    #print(alert)
    if alert == "+":
        break
    formato_grafica(int(alert))  # Llamar a formato_grafica() con 'alert' como argumento