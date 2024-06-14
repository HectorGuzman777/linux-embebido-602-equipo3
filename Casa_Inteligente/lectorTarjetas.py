import serial
import time

# Conexión al lector RFID a través del puerto serial
rfid_reader = serial.Serial('/dev/ttyUSB0', 9600)

# Diccionario para almacenar los nombres de las tarjetas RFID
rfid_cards = {
    '500094696BC6': 'Sujeto1',
    '4F0056AF0ABC': 'Sujeto2'
}

while True:
    # Leer el código RFID
    rfid_code = rfid_reader.readline().strip()

    # Buscar el nombre de la tarjeta en el diccionario
    card_name = rfid_cards.get(rfid_code, 'Tarjeta no valida')

    # Obtener la hora actual
    current_time = time.strftime("%H:%M:%S")

    # Imprimir el nombre de la tarjeta y la hora
    print(f'{card_name} accedió a las {current_time}')
