# Definir el compilador
CC = avr-gcc
# Definir las banderas del compilador
CFLAGS = -Os -mmcu=atmega328p -I/usr/lib/avr/include
# Definir el nombre del archivo de salida
TARGET = leds
# Definir el microcontrolador
MCU = m328p
# Definir el programador
PROGRAMMER = usbasp


# Regla por defecto
all: $(TARGET).hex


# Regla para compilar el código
$(TARGET).o: leds.c
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET).elf: $(TARGET).o
	$(CC) $(CFLAGS) -o $@ $<

$(TARGET).hex: $(TARGET).elf
	avr-objcopy -j .text -j .data -O ihex $< $@

#Regla para programar el microcontroladdor
program: $(TARGET).hex
	sudo avrdude -c $(PROGRAMMER) -p $(MCU) -U flash:w:$<


# Regla para limpiar los archivos generados
clean:
	rm -f $(TARGET).o $(TARGET).elf $(TARGET).hex