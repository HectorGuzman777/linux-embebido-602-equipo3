import socket
import threading

HEADER = 64  # bytes
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

led_states = {
    1: {'R': False, 'G': False, 'B': False, 'Y': False, 'C': False, 'M': False, 'W': False},
    2: {'R': False, 'G': False, 'B': False, 'Y': False, 'C': False, 'M': False, 'W': False},
    3: {'R': False, 'G': False, 'B': False, 'Y': False, 'C': False, 'M': False, 'W': False},
    4: {'R': False, 'G': False, 'B': False, 'Y': False, 'C': False, 'M': False, 'W': False},
    5: {'R': False, 'G': False, 'B': False, 'Y': False, 'C': False, 'M': False, 'W': False}
}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    print(f"[{addr}] {msg}")
                    # Procesar el comando recibido
                    process_command(msg)
                    response = "Command processed successfully"
                    conn.send(response.encode(FORMAT))
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected")

def process_command(msg):
    # Ejemplo de procesamiento de comandos
    # Comandos esperados: "LED <number> <color> ON/OFF" o "ACTIVATE BUZZER"
    try:
        parts = msg.split()
        if parts[0] == "LED" and len(parts) == 4:
            led_number = int(parts[1])
            color = parts[2]
            state = parts[3].upper() == "ON"
            if led_number in led_states and color in led_states[led_number]:
                led_states[led_number][color] = state
                print(f"LED {led_number} - {color} set to {state}")
            else:
                print("Invalid LED number or color")
        elif msg == "ACTIVATE BUZZER":
            print("Buzzer activated")
            # Aquí podrías agregar la lógica para activar el buzzer físico
        else:
            print("Invalid command")
    except Exception as e:
        print(f"[ERROR] Failed to process command: {e}")

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting.....")
start()
