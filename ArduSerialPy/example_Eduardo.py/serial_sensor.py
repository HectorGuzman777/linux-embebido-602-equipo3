<<<<<<< HEAD
#Librerias standar
import time

#libreris de terceros
import serial

#archivos locales

BAUDRATES = [ #Velocidad en la que se envian o reciben los caracteres
    2400,
    4800, 
=======

#Librerias standard
import time

#Librerias de 3ros
import serial

#Archivos locales

BAUDRATES = [   #Velocidad a la que se envian o reciben los caracteres
    2400,
    4800,
>>>>>>> dev
    9600, 
    19200, 
    38400, 
    57600, 
    115200
]

class SerialSensor:
<<<<<<< HEAD

    def __init__(self,
                  port: str,
                  baudrate: int = 115200,
                  timeout: float = 2.,  #por defecto dos segundos
                  connection_time: float = 3.,
                  reception_time: float = .5
        ) -> None:
        self._serial = serial.Serial(
            port = port,
            baudrate = baudrate,
            timeout = timeout  #tiempo que esperas esa respuesta
        )
        self.connection_time = connection_time
        self.reception_time = reception_time
        time.sleep(connection_time)
        received = self.send('OK')


    def send(self, to_send:str)->str:   #vamos a regresar una strign
        self.serial.write(to_send.encode('utf-8'))
        time.sleep(self.reception_time)
        received = self.serial.readline()  #para facilitar lleer lineas
        return received.decode(encoding='utf-8')
    
    def received(self,) -> str:
        received = self._serial.readline()
        return received.decode(encoding='utf-8')
    
    def close(self )-> None:
        self._serial.close()
    

    def __str__(self) -> str:
        return "SerialSensor({self.serial=}, {self.connection_time=}, {self.reception_time=})"

    def __repr__(self) -> str:
        return "SerialSensor({self.serial=}, {self.connection_time=}, {self.reception_time=})"

=======
    
    def __init__(self,
                 port:str,
                 baudrate: int = 115200,
                 timeout: float = 2.,
                 connection_time: float = 3.,
                 reception_time: float = .5
            ) -> None:
            self._serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
            self.connection_time = connection_time
            self.reception_time = reception_time
            time.sleep(connection_time)
            recieved = self.send('OK')
            
    def send(self, to_send:str) -> str:
        self._serial.write(to_send.encode('utf-8')) #Codificar
        time.sleep(self.reception_time) #Tiempo de espera para que se puedan sincronzar ambos dispositivos
        recieved = self._serial.readline()
        return recieved.decode(encoding='utf-8') #Decodificar
    
    def recieve(self,) -> str:
        recieved = self._serial.readline()
        return recieved
    
    def close(self) -> None:
        self._serial.close()
            
    def __str__(self) -> str:
        return f"Serial Sensor({self._serial=}, {self.connection_time=},{self.reception_time=})"
    
    def __repr__(self) -> str:
        return f"Serial Sensor({self._serial=}, {self.connection_time=},{self.reception_time=})"
    
>>>>>>> dev
    def __del__(self) -> None:
        self.close()