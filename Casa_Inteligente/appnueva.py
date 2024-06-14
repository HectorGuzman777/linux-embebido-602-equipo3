
from tkinter import BOTH, Button, Frame, Label, Toplevel, Tk, messagebox
import tkinter as tk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import serial
import subprocess
import socket
import threading
import serial.tools.list_ports

BAUDRATES = [9600, 19200, 38400, 57600, 115200]

numero_de_led = 0

# ######################################################################## #
class SerialSensor:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)

    def send(self, command):
        self.ser.write(command.encode())
        return self.ser.readline().decode()

# ######################################################################## #
class App:
    def __init__(self, parent):
        self.parent = parent
        self.serial_device = None
        self.init_gui()

    def init_gui(self):
        self.parent.title('CASA INTELIGENTE')
        self.parent.geometry('1000x1000')  # Tamaño de la ventana 1000x1000

        # Crear un Frame para contener la imagen de fondo y otros widgets
        self.frame = tk.Frame(self.parent, bg='black')
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
        self.resized_image = self.image.resize((frame_width, frame_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.resized_image)

        # Actualizar la imagen en el Label
        self.bg_label.config(image=self.photo)

    def create_widgets(self):
        # Crear widgets para la conexión serial
        self.serial_devices_combobox = self._init_serial_devices_combobox()
        self.refresh_serial_devices_button = self._create_refresh_serial_devices_button()
        self.baudrate_combobox = self._create_baudrate_combobox()
        self.connect_button = self._create_connect_button()
        self.comboboxs = self.comboboxs()   # Llamar al método combobox_leds
        self.on_off_buttons = self.on_off_buttons()
        self.buzzer_button = self._create_buzzer_button()
        self.labels_xd()

        self.serial_devices_combobox.place(x=50, y=20)
        self.refresh_serial_devices_button.place(x=275, y=20)
        self.baudrate_combobox.place(x=450, y=20)
        self.connect_button.place(x=650, y=20)
        self.buzzer_button.place(x=800, y=20)
        # las coordenadas de on_off_buttions estan declarados de la misma funcion
        # lo mismo con labelxd

        

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
        except ValueError:
            messagebox.showerror('Wrong baudrate', 'Baudrate not valid')
            return

    def _create_connect_button(self):
        return Button(self.frame, text='Connect', command=self.connect_serial_device)
    
    """
    def create_led_control_buttons(self):
        colors = ['R', 'G', 'B', 'Y', 'C', 'M', 'W']
        for led_number in range(1, 6):
            for idx, color in enumerate(colors):
                button = Button(self.frame, text=f"LED {led_number} - {color}",
                                command=lambda num=led_number, col=color: self.send_command(num, col))
                button.place(x=50 + (idx * 100), y=100 + (led_number * 50))
    """

    def send_command(self, led_number, color):
        if self.serial_device is None:
            messagebox.showerror('Serial connection error', 'Serial device not initialized')
            return
        command = f"{led_number}{color}\n"
        self.serial_device.send(command)
        print(f"Enviando comando: {command.strip()}")

    def comboboxs(self):
        
        # COMBOBOX LEDS
        leds_list = ['Led #1', 'Led #2', 'Led #3', 'Led #4', 'Led #5']
        self.led_var = tk.StringVar()
        self.led_box = Combobox(self.frame, textvariable=self.led_var, values=leds_list)
        self.led_box.place(x=50, y=70)
        self.led_box.bind('<<ComboboxSelected>>', self.on_led_selected)

        # COMBOBOX COLORES
        color_list = ['Rojo', 'Azul', 'Amarillo', 'Morado', 'Verde', 'Blanco', 'Cian']
        self.color_var = tk.StringVar()
        self.color_box = Combobox(self.frame, textvariable=self.color_var, values=color_list)
        self.color_box.place(x=450, y=70)
        self.color_box.bind('<<ComboboxSelected>>', self.on_color_selected)



    def on_led_selected(self, event):
        selected_led = self.led_var.get()
        self.confirm_led_selection(selected_led)

    def confirm_led_selection(self, led):
        top = Toplevel(self.parent)
        top.title("Confirmación")
        top.geometry("300x100")

        Label(top, text=f"Has seleccionado {led}. ¿Es correcto?").pack(pady=10)
        Button(top, text="OK", command=top.destroy).pack(pady=5)

    def on_color_selected(self, event):
        selected_color = self.color_var.get()
        selected_led = self.led_var.get()

        led_button_map = {
            'Led #1': self.button1,
            'Led #2': self.button2,
            'Led #3': self.button3,
            'Led #4': self.button4,
            'Led #5': self.button5,
        }

        color_map = {
            'Rojo': 'red',
            'Azul': 'blue',
            'Amarillo': 'yellow',
            'Verde': 'green',
            'Morado': 'purple',
            'Cian': 'cyan',
            'Blanco': 'white',
        }

        if selected_led in led_button_map:
            led_button_map[selected_led].config(text = "ON", fg=color_map[selected_color])
    

    def on_off_buttons(self):
        leds_list = ['Led #1', 'Led #2', 'Led #3', 'Led #4', 'Led #5']
        color_list = ['Rojo', 'Azul', 'Amarillo', 'Morado', 'Verde', 'Blanco', 'Cian']
        self.button1 = tk.Button(self.frame, text="Led #1", 
                                             font=("Times New Roman", 20, "bold"), 
                                             bg="white", fg="black", 
                                             width=10, height=2, 
                                             relief="raised", 
                                             borderwidth=3, 
                                             command=lambda: self.send_command(leds_list, color_list))
        self.button1.place(x=480, y=170)


        self.button2 = tk.Button(self.frame, text="Led #2", 
                                             font=("Times New Roman", 20, "bold"), 
                                             bg="white", fg="black", 
                                             width=10, height=2, 
                                             relief="raised", 
                                             borderwidth=3, 
                                             command=lambda: self.toggle_led(2))
        self.button2.place(x=250, y=300)
    

        self.button3 = tk.Button(self.frame, text="Led #3", 
                                             font=("Times New Roman", 20, "bold"), 
                                             bg="white", fg="black", 
                                             width=10, height=2, relief="raised", 
                                             borderwidth=3, 
                                             command=lambda: self.toggle_led(3))
        self.button3.place(x=720, y=300)


        self.button4 = tk.Button(self.frame, text="Led #4", 
                                             font=("Times New Roman", 20, "bold"), 
                                             bg="white", fg="black", 
                                             width=10, height=2, relief="raised", 
                                             borderwidth=3, 
                                             command=lambda: self.toggle_led(4))
        self.button4.place(x=220, y=550)


        self.button5 = tk.Button(self.frame, text="Led #5", 
                                             font=("Times New Roman", 20, "bold"), 
                                             bg="white", fg="black", 
                                             width=10, height=2, relief="raised", 
                                             borderwidth=3, 
                                             command=lambda: self.toggle_led(5))
        self.button5.place(x=750, y=550)


    def toggle_led(self, led_number):
        self.led_states[led_number] = not self.led_states[led_number]
        button = getattr(self, f'button{led_number}')
        if self.led_states[led_number]:
            selected_color = self.color_var.get().lower()
            color_map = {
                'rojo'  : 'red',
                'azul'  : 'blue',
                'amarillo'  : 'yellow',
                'verde' : 'green',
                'cian'  : 'cyan',
                'morado': 'purple',
                'blanco': 'white',
            }
            button.config(bg=color_map.get(selected_color, 'white'), fg='black')
    

    def labels_xd(self):
        num_leds_label = Label (
            master = self.frame,
            text = 'Numero de leds',
            background='white',
            foreground = 'black',
            font=("Times New Roman", 13), 
        )
        num_leds_label.place(x=240, y=70)

        color_leds_label = Label (
            master = self.frame,
            text = 'Colores a elegir',
            background='white',
            foreground = 'black',
            font=("Times New Roman", 13), 
        )   
        color_leds_label.place(x=650, y=70)
        
    def send_buzzer_command(self):
        if self.serial_device is None:
            messagebox.showerror('Serial connection error', 'Serial device not initialized')
            return
        command = 'T\n'  # Comando para activar el buzzer
        self.serial_device.send(command)
        print(f"Enviando comando al buzzer: {command.strip()}")


    def _create_buzzer_button(self):
        return Button(self.frame, text='Activate Buzzer', command=self.send_buzzer_command)
    

    @staticmethod
    def find_available_serial_ports():
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
# ######################################################################## #

if __name__ == '__main__':

        # Inicializar el servidor primero
    server = HouseServer(host='0.0.0.0', port=3333)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    root = Tk()
    app = App(root)
    root.mainloop()
