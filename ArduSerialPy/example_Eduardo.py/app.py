from tkinter import BOTH
from tkinter import Tk
from tkinter import Frame
from tkinter.ttk import Combobox

from utils import find_available_serial_ports

class App(Frame):

    def __init__(self, parent, *args, **kwargs): 
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent:Tk = parent
        # Aqui vamos a crear todos los componentes graficos
        self.serial_devices_combobox = self._init_serial_devices_combobox()
        self.init_gui()

    def init_gui(self,)-> None:
        
        self.parent.title = 'ArduSerial'
        self.parent.geometry('800x800') 
        self['bg'] = 'white'
        self.pack(expand=True, fill=BOTH)
        #aqui vamos a colocar los elementos graficos
        #row 0
        self.serial_devices_combobox.grid(row=0, column=0)
    
    def _init_serial_devices_combobox(self, )->Combobox:
        ports = find_available_serial_ports()
        return Combobox(self, values=ports, font=("Courier", 20))


root = Tk()

if __name__ == '__main__':
    ex = App(root)
    
    root.mainloop()