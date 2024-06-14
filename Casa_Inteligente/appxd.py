from tkinter import Button, messagebox
import tkinter as tk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
import requests
import socket

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

BAUDRATES = [9600, 19200, 38400, 57600, 115200]

class SerialSensor:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)

    def send(self, command):
        self.ser.write(command.encode())
        return self.ser.readline().decode()

class App:
    def __init__(self, parent):
        self.parent = parent
        self.serial_device = None
        self.init_gui()

    def init_gui(self):
        self.parent.title('CASA INTELIGENTE')
        self.parent.geometry('1000x1000')  # Tamaño de la ventana 1000x800

        # Crear un Frame para contener la imagen de fondo y otros widgets
        self.frame = tk.Frame(self.parent, bg='red')
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Crear un Label para la imagen de fondo
        self.bg_label = tk.Label(self.frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Cargar la imagen y redimensionarla para que se ajuste al Label
        self.load_image()

        # Ajustar la imagen cuando la ventana cambia de tamaño
        self.parent.bind('<Configure>', self.resize_image)

        # Colocar otros widgets en el Frame
        self.create_widgets()

    def load_image(self):
        self.image = Image.open('CASAINTELIGENTE.png')
        self.photo = ImageTk.PhotoImage(self.image)
        self.bg_label.config(image=self.photo)

    def resize_image(self, event):
        # Obtener el tamaño actual del frame
        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()

        # Redimensionar la imagen para que se ajuste al Label
        self.resized_image = self.image.resize((frame_width, frame_height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.resized_image)

        # Actualizar la imagen en el Label
        self.bg_label.config(image=self.photo)

    def create_widgets(self):
        # Crear widgets para la conexión serial
        self.serial_devices_combobox = self._init_serial_devices_combobox()
        self.refresh_serial_devices_button = self._create_refresh_serial_devices_button()
        self.baudrate_combobox = self._create_baudrate_combobox()
        self.connect_button = self._create_connect_button()
        self.buzzer_button = self._create_buzzer_button()
        
        self.serial_devices_combobox.place(x=50, y=20)
        self.refresh_serial_devices_button.place(x=270, y=20)
        self.baudrate_combobox.place(x=450, y=20)
        self.connect_button.place(x=650, y=20)
        self.buzzer_button.place(x=800, y=20)
        
        self.create_led_control_buttons()

    def _init_serial_devices_combobox(self):
        ports = self.find_available_serial_ports()
        return Combobox(self.frame, values=ports, font=("Courier", 12))

    def refresh_serial_devices(self):
        ports = self.find_available_serial_ports()
        self.serial_devices_combobox['values'] = ports

    def _create_refresh_serial_devices_button(self):
        return Button(self.frame, text="Refresh serial devices", command=self.refresh_serial_devices)

    def _create_baudrate_combobox(self):
        baudrates_values = [str(rate) for rate in BAUDRATES]
        return Combobox(self.frame, values=baudrates_values)

    def connect_serial_device(self):
        try:
            baudrate = int(self.baudrate_combobox.get())
            port = self.serial_devices_combobox.get()
            if port == '':
                messagebox.showerror('Port not selected', 'Select a valid port')
                return
            self.serial_device = SerialSensor(port=port, baudrate=baudrate)
            messagebox.showinfo('Connection Successful', 'Serial device connected successfully')
        except ValueError:
            messagebox.showerror('Wrong baudrate', 'Baudrate not valid')
            return

    def _create_connect_button(self):
        return Button(self.frame, text='Connect', command=self.connect_serial_device)

    def _create_buzzer_button(self):
        return Button(self.frame, text='Activate Buzzer', command=self.send_buzzer_command)

    def create_led_control_buttons(self):
        colors = ['R', 'G', 'B', 'Y', 'C', 'M', 'W']
        for led_number in range(1, 6):
            for idx, color in enumerate(colors):
                button = Button(self.frame, text=f"LED {led_number} - {color}",
                                command=lambda num=led_number, col=color: self.send_command(num, col))
                button.place(x=50 + (idx * 100), y=100 + (led_number * 50))

    def send_command(self, led_number, color):
        if self.serial_device is None:
            messagebox.showerror('Serial connection error', 'Serial device not initialized')
            return
        command = f"{led_number}{color}\n"
        self.serial_device.send(command)
        self.send_socket_command(command)
        print(f"Enviando comando: {command.strip()}")

    def send_socket_command(self, command):
        message = command.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def send_buzzer_command(self):
        if self.serial_device is None:
            messagebox.showerror('Serial connection error', 'Serial device not initialized')
            return

        # Verificar si se ha detectado una tarjeta válida
        rfid_data = self.read_rfid_code()
        if rfid_data:
            print(f"Valid RFID card detected: {rfid_data}")
            # Llamar al servidor para activar el buzzer solo si se detecta una tarjeta válida
            try:
                response = requests.get('http://localhost:8082/activate_buzzer')
                if response.status_code == 200:
                    messagebox.showinfo('Buzzer Activated', 'Buzzer activated successfully')
                    print("Buzzer activated successfully")
                    self.send_socket_command("Activate Buzzer")
                else:
                    messagebox.showerror('Server Error', 'Failed to activate the buzzer')
                    print(f"Failed to activate buzzer. Server returned status code: {response.status_code}")
            except Exception as e:
                messagebox.showerror('Server Connection Error', f'Error connecting to server: {e}')
                print(f"Error connecting to server: {e}")
        else:
            messagebox.showerror('RFID Error', 'No valid RFID card detected')
            print("No valid RFID card detected")

    def find_available_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def read_rfid_code(self):
        # Simulación de lectura de un código RFID
        return "123456789"


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
