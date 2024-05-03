#Standar python libraries
import time
#3rd party libraries
import serial
#local libraries or modules
#import .example
from locate_ports import find_ports

ser = serial.Serial(port='/dev/ttyACM0',baudrate=115200)

time.sleep(2)

ser.write(b'hola')  #lo mando en bytes

time.sleep(1)

for i in range(1,4):
    to_send = f'prueba {i}'
    ser.write(to_send.encode('utf-8')) #utf-8 es un estandar para decir que tal byte es tal caracter, tipo ascii
    time.sleep(.5)
    received = ser.readline()
    print("Received: ", received)




# Llama a la función find_ports para obtener la lista de puertos seriales disponibles
available_ports = find_ports()

# Imprime los puertos seriales disponibles
print("Puertos seriales disponibles:")
for port in available_ports:
    print(port)


ser.close() #siempre que trabajemos con serial ponerlo