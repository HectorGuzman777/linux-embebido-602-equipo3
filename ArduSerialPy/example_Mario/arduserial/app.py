from tkinter import BOTH
from tkinter import Tk
from tkinter import Frame #va a heredar de la clase Frame
from tkinter.ttk import Combobox

from utils import find_available_serial_ports

from typing import Any, Literal

class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent:Tk = parent #parent sera el objeto al que se le va a pegar el frame
        self.serial_devices_combobox = self.__init_serial_devices_combobox()
        self.init_gui()


    def init_gui(self,) -> None:
        self.parent.title = 'ArduSerial'
        self.parent.geometry('800x800')
        self['bg'] = 'white'
        self.pack(expand=True, fill=BOTH)   #que se pegue, que se empaquete

        #row 0
        self.serial_devices_combobox.grid(row=0, column=0)
    
    def __init_serial_devices_combobox(self, )->Combobox:
        ports = find_available_serial_ports()
        return Combobox(self, values=ports, font=("Courier", 20))




root = Tk()   #objeto raiz que va a crear nuestra visual

if __name__ == '__main__':
    ex = App(root)

    root.mainloop()