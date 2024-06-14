"""
José Eduardo Viveros Escamilla
Mario Godinez Chavero
Hector Gumaro Guzman Reyes
"""



from tkinter import BOTH
from tkinter import Button
from tkinter import Frame
from tkinter import Label
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, parent):
        self.parent = parent
        self.init_gui()

    def init_gui(self):
        self.parent.title('CASA INTELIGENTE')
        self.parent.geometry('1000x1000')  # Tamaño de la ventana    1000x800

        # Crear un Frame para contener la imagen de fondo y otros widgets
        self.frame = tk.Frame(self.parent, bg = 'red')
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
        frame_width  = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()

        # Redimensionar la imagen para que se ajuste al Label
        self.resized_image = self.image.resize((frame_width, frame_height), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.resized_image)

        # Actualizar la imagen en el Label
        self.bg_label.config(image=self.photo)

    def create_widgets(self):
        
        # Ejemplo de widget en el frame
        button = tk.Button(self.frame, text="")
        button.place(x=50, y=50)  # Ajusta la posición según sea necesario
       
        button = tk.Button(self.frame, text="Presionar")
        button.place(x=100, y=200)  # Ajusta la posición según sea necesario
        


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()