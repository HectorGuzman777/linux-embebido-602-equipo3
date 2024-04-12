#include <avr/io.h>
#include <util/delay_basic.h>

int main (void)
{
    DDRB |= _BV(PORTB0);      // set pin 0 of port B as an output pin

    for (;;) {
        PORTB |= _BV(PORTB0);  // set pin 0 of port B high
        _delay_loop_2(62500);  // loop for 62500 iterations * 4 cycles / 1MHz clock ~= 250ms
        PORTB &= ~_BV(PORTB0); // set pin 0 of port B low
        _delay_loop_2(62500);  // loop for 62500 iterations * 4 cycles / 1MHz clock ~= 250ms
    }
}
