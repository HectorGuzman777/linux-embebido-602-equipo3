import socket
import time

ADDRESS = 'localhost' #e.g. '192.168.10.3'
PORT = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ADDRESS,PORT))

try:
    while True:
        to_send = input("Do you want to send something?->")
        sock.send(to_send.encode())
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting....")
except Exception as e:
    print(f"Something happened {e}")
finally:
    sock.close()