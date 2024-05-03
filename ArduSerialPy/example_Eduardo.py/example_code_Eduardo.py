
# en orden alfabetico
# standard python libraries
import time 
import serial
#local libraries or maodules
#mandamos a llamar la funcion del archivo desde de find ports 
#para poder subirla
from locate_ports import find_ports

ser = serial.Serial(port='/dev/tty', baudrate=115200)

time.sleep(2)

ser.write(b'Hola')

time.sleep(2)

ser.write(b'Hola')

time.sleep(2)

#ser.write(b'Prueba')
for i in range (1,4):
    to_send = f'prueba {i}'
    ser.write(to_send.encode('utf-8'))
    time.sleep(.5)
    received = ser.readline()
    print("Received", received)
ser.close()
