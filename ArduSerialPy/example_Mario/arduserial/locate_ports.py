#Encontrar los puertos seriales disponibles
import serial.tools.list_ports

def find_ports()->list[str]:
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

print(find_ports())