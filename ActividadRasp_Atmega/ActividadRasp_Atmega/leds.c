#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>

  // Definir la frecuencia del reloj como 1 MHz>

int main(void)
{
    DDRB |= (1 << PB0) | (1 << PB1) | (1 << PB2); // Configurar pines PB0, PB1 y PB2 como salidas
    while (1)
    {
        PORTB |= (1 << PB0); // Encender LED en PB0
        _delay_ms(1500);      // Esperar 250 ms
        PORTB &= ~(1 << PB0); // Apagar LED en PB0
        PORTB |= (1 << PB1);  // Encender LED en PB1
        _delay_ms(1500);       // Esperar 250 ms
        PORTB &= ~(1 << PB1); // Apagar LED en PB1
        PORTB |= (1 << PB2);  // Encender LED en PB2
        _delay_ms(1500);       // Esperar 250 ms
        PORTB &= ~(1 << PB2); // Apagar LED en PB2
    }
    return 0;
}
