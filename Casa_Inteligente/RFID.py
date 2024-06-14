
import serial

ser = serial.Serial('/dev/ttyUSB1', 9600)  # Ajusta la velocidad en baudios si es necesario

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
