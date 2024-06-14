from tkinter import BOTH
from tkinter import Button
<<<<<<< HEAD
from tkinter import Frame #va a heredar de la clase Frame
from tkinter import Label
from tkinter import messagebox
from tkinter import Tk
=======
from tkinter import Frame
from tkinter import Label
from tkinter import messagebox
from tkinter import Tk

>>>>>>> dev
from tkinter.ttk import Combobox

from utils import find_available_serial_ports
from serial_sensor import BAUDRATES
from serial_sensor import SerialSensor

<<<<<<< HEAD
from typing import Any, Literal

class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent:Tk = parent #parent sera el objeto al que se le va a pegar el frame
        self.serial_device: SerialSensor| None = None
        #Aqui vamos a crear todos los componentes graficos
        self.serial_devices_combobox: Combobox = self.__init_serial_devices_combobox()
        self.refresh_serial_devices_button: Button = self._create_refresh_serial_devices_button()
        self.baudrate_combobox: Combobox = self._create_baudrate_combobox()
        self.connect_button: Button = self._create_connect_button()
=======
class App(Frame):

    def _init_(self, parent, *args, **kwargs):       
        Frame._init_(self, parent, *args, **kwargs)
        self.parent:Tk = parent
        # Esta variable puede ser del tipo sensor o nada
        self.serial_device: SerialSensor | None = None
        # Aqui vamos a crear todos los componentes graficos
        self.serial_devices_combobox: Combobox = self._init_serial_devices_combobox()
        self.refresh_serial_devices_button: Button = self._create_refresh_serial_devices_button()
        self.baudrate_combobox: Combobox = self._create_baudrate_combobox()
        self.connet_button: Button = self._create_connect_button()
>>>>>>> dev
        self.temperature_label: Label = self._create_temperature_label()
        self.read_temperature_button: Button = self._create_temperature_button()
        self.init_gui()

<<<<<<< HEAD

    def init_gui(self,) -> None:
        self.parent.title = 'ArduSerial'
        self.parent.geometry('800x800')
        self['bg'] = 'white'
        self.pack(expand=True, fill=BOTH)   #que se pegue, que se empaquete
        #Aqui vamos a colocar los elementos graficos
        #row 0
        self.serial_devices_combobox.grid(row=0, column=0)
        self.refresh_serial_devices.grid(row=0, column=1)
        self.baudrate_combobox.grid(row=0, column=2)
        self.connect_button.grid(row=0,column=3)
        #row 1
        self.temperature_label.grid(row=1,column=0)
        self.read_temperature_button.grid(row=1,column=1)

        #other setting
        self.baudrate_combobox.current(0)

    def refresh_serial_devices(self)->None:
        ports = find_available_serial_ports()
        self.serial_devices_combobox['values'] = ports

    def connect_serial_device(self)->None:
        try:
            baudrate = int(self.baudrate_combobox.get())
            port = self.serial_devices_combobox.get()
            if port == '':
                messagebox.showerror('Port not selected', f'Select a valid port {port=}')
            return
            self.serial_device = SerialSensor(
                port=port,
                baudrate=baudrate
            )
        except ValueError:  #cuando hay un value error
            messagebox.showerror('Wrong baudrate', f'Baudrate not valid')
            return
        
    def read_temperature(self)->None:
        if self.serial_device is not None:
            temperature = self.serial_device.send('TC2')
            self.temperature_label['text'] = f"{temperature[1:-4]} C" 
            return
        messagebox.showerror(title='Serial connection Error', message='Serial device not inicialized')

    def __init_serial_devices_combobox(self, )->Combobox:
        ports = find_available_serial_ports()
        return Combobox(self, values=ports, font=("Courier", 20))
    
    def _create_refresh_serial_devices_button(self, )-> Button:
        return Button(
            master=self,
            text="Refresh seerial devices",
            command = self.refresh_serial_devices
        )

    def _create_baudrate_combobox(self) -> Combobox:
        baudrates_values = ['BAURATE'] +BAUDRATES
=======
    def init_gui(self,)-> None:

        self.parent.title('ArduSerial')
        self.parent.geometry('800x800') 
        self['bg'] = 'white'
        self.pack(expand=True, fill=BOTH)
        #aqui vamos a colocar los elementos graficos
        #row 0
        self.serial_devices_combobox.grid(row=0, column=0)
        self.refresh_serial_devices_button.grid(row = 0, column = 1)
        self.baudrate_combobox.grid(row = 0, column = 2)
        self.connet_button.grid(row = 0, column = 3)
        #row 1
        self.temperature_label.grid(row = 1, column = 0)
        self.read_temperature_button.grid(row = 1, column = 1)
        #other settings
        self.baudrate_combobox.current(0) # No esta seleccionado
    
    # El guión bajo es solo para funciones internas, y el doble guión para funciones tipo "protected"
    def read_temperature(self) -> None:
        if self.serial_device is not None:
            temperature = self.serial_device.send('TC2')
            self.temperature_label['text'] = f"{temperature[1:-4]} C"
            return
        messagebox.showerror(title='Serial connection error', message='Serial device not initializate')
    
    def _init_serial_devices_combobox(self, ) -> Combobox:
        ports = find_available_serial_ports()
        return Combobox(self, values=ports, font=("Courier", 20))
    
    def refresh_serial_devices(self) -> None:
        ports = find_available_serial_ports()
        self.serial_devices_combobox['values'] = ports
    
    def _create_refresh_serial_devices_button(self,) -> Button:
        return Button(
            master = self,
            text = "Refresh serial devices",
            command = self.refresh_serial_devices
        )
        
    def _create_baudrate_combobox(self) -> Combobox:
        baudrates_values = ['BAUDRATE'] + BAUDRATES
>>>>>>> dev
        return Combobox(
            master = self,
            values = baudrates_values
        )
<<<<<<< HEAD

    def _create_connect_button(self)->Button:
        return Button(
            master = self,
            text = 'Connect',
            command=self.connect_serial_device
        )
    
    def _create_temperature_label(self)-> Label:
        return Label(
            master=self,
            text='XX.XX C',
            foreground='red'
        )
    
    def _create_temperature_button(self)-> Button:
        return Button(
        master=self,
        text='read temperature',
        command=self.read_temperature
    )
=======
    
    def connect_serial_device(self) -> None:
        try:        
            baudrate = int(self.baudrate_combobox.get())
            port = self.serial_devices_combobox.get()
            if port != '':
                 messagebox.showerror('Port not selected',f'Select a valid port {port =}')
            self.serial_device = SerialSensor(
                port = port,
                baudrate = baudrate
            ) 
                
        except ValueError:
            messagebox.showerror('Wrong baudrate','Baudrate not valid')
            return
        

    def _create_connect_button(self,) -> Button:
        return Button(
            master = self,
            text = 'Connect',
            command = self.connect_serial_device
        )
    
    def _create_temperature_label(self) -> Label:
        return Label(
            master = self,
            text = 'XX.X °C',
            foreground = 'red'
        )
        
    def _create_temperature_button(self) -> None:
        return Button(
            master = self,
            text = 'Read temperature',
            command = self.read_temperature
        )
>>>>>>> dev

root = Tk()   #objeto raiz que va a crear nuestra visual

if __name__ == '__main__':
    ex = App(root)

<<<<<<< HEAD
    root.mainloop()

    
=======
    root.mainloop()
>>>>>>> dev
