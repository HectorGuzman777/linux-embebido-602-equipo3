import os
import shutil
import serial
import time
import logging
import requests
from fastapi import FastAPI
from starlette.responses import HTMLResponse

# Configurar el registro (logging)
logging.basicConfig(level=logging.INFO)

# Conexión al lector RFID a través del puerto serial
try:
    rfid_reader = serial.Serial('/dev/ttyUSB1', 9600, timeout=5)
    logging.info("Conexión al lector RFID establecida.")
except Exception as e:
    logging.error(f"No se pudo establecer conexión al lector RFID: {e}")

# Diccionario para almacenar los nombres de las tarjetas RFID
rfid_cards = {
    '500094696BC6': 'Sujeto1',
    '4F0056AF0ABC': 'Sujeto2'
}

# Lista para almacenar los registros de acceso
access_records = []

# Función para limpiar y procesar códigos RFID
def clean_rfid_code(code):
    return ''.join(filter(str.isalnum, code.strip()))

app = FastAPI()

def activate_buzzer():
    try:
        # Abrir el puerto serial para enviar el comando al ATmega
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(b'T\n')  # Enviar el comando para activar el buzzer
            logging.info("Comando enviado al buzzer para activación.")
    except Exception as e:
        logging.error(f"No se pudo activar el buzzer: {e}")


def read_rfid_code():
    try:
        # Leer el código RFID
        logging.info("Leyendo código RFID...")
        rfid_code = rfid_reader.readline().decode('utf-8')
        rfid_code_cleaned = clean_rfid_code(rfid_code)
        
        if not rfid_code_cleaned:
            return None
        
        logging.info(f"Código RFID leído: '{rfid_code}' (limpiado: '{rfid_code_cleaned}')")

        # Buscar el nombre de la tarjeta en el diccionario
        card_name = rfid_cards.get(rfid_code_cleaned)
        if card_name is None:
            card_name = f"Intento de ingreso por {rfid_code_cleaned}"
        logging.info(f"Nombre de la tarjeta: {card_name}")

        # Obtener la hora actual
        current_time = time.strftime("%H:%M:%S")

        # Guardar el registro de acceso
        access_records.append((card_name, current_time))

        return card_name, current_time
    except Exception as e:
        logging.error(f"Error durante la lectura del RFID: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def main():
    rfid_data = read_rfid_code()
    
    if rfid_data:
        card_name, current_time = rfid_data
        last_access_html = f"<h1>Último acceso: {card_name} a las {current_time}</h1>"
    else:
        last_access_html = "<h1>No se ha leído ningún código RFID recientemente.</h1>"

    # Crear el contenido HTML con auto-refresh y mostrar todos los registros
    content = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Acceso RFID</title>
        <meta http-equiv="refresh" content="5"> <!-- Refresca cada 5 segundos -->
    </head>
    <body>
        {last_access_html}
        <h2>Registros de Acceso</h2>
        <ul>
        {"".join([f"<li>{name} accedió a las {time}</li>" for name, time in access_records])}
        </ul>
    </body>
</html>
    """
    return HTMLResponse(content=content)

@app.get("/activate_buzzer")
async def activate_buzzer_route():
    try:
        print("Attempting to activate buzzer...")  # Información de depuración
        activate_buzzer()  # Llamar a la función para activar el buzzer
        print("Buzzer activated successfully")
        return {"message": "Buzzer activated"}
    except Exception as e:
        print(f"Error activating buzzer: {e}")
        return {"error": f"Failed to activate buzzer: {e}"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8082)
