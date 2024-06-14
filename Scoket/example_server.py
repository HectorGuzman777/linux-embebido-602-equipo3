
import socket

ADDRESS = 'localhost' #e.g. '192.168.10.3'
PORT = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((ADDRESS, PORT)) #le paso una tupla
sock.listen()

connection, client_address = sock.accept() #en el momento que alguien se conecte

print(f"Received connection from address: {client_address}")

try:
    while True:
        data = connection.recv(1024)

        print(f"Received {data.decode()}")
except KeyboardInterrupt:
    print("Shutting down server...")
except Exception as e:
    print(f"Something happened {e}")
finally:
    connection.close()
    sock.close()