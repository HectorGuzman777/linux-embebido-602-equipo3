/*
 * Programa_4.c
 *
 * Created: 6/13/2024 8:14:44 PM
 * Author: mario
 */


#include <io.h>
#include <stdio.h>
#include <delay.h>

#define NOTE_B0  31
#define NOTE_C1  33
#define NOTE_CS1 35
#define NOTE_D1  37
#define NOTE_DS1 39
#define NOTE_E1  41
#define NOTE_F1  44
#define NOTE_FS1 46
#define NOTE_G1  49
#define NOTE_GS1 52
#define NOTE_A1  55
#define NOTE_AS1 58
#define NOTE_B1  62
#define NOTE_C2  65
#define NOTE_CS2 69
#define NOTE_D2  73
#define NOTE_DS2 78
#define NOTE_E2  82
#define NOTE_F2  87
#define NOTE_FS2 93
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978
#define REST      0

#define RED1 PORTB.4
#define GREEN1 PORTB.3
#define BLUE1 PORTB.2
#define RED2 PORTB.7
#define GREEN2 PORTB.6
#define BLUE2 PORTB.5
#define RED3 PORTC.2
#define GREEN3 PORTC.1
#define BLUE3 PORTC.0
#define RED5 PORTC.5
#define GREEN5 PORTC.4
#define BLUE5 PORTC.3
#define RED4 PORTD.2
#define GREEN4 PORTD.3
#define BLUE4 PORTD.4

char dato;
char led, color;

int estadoTono = 0; 

int melody1[] = {

 // Never Gonna Give You Up - Rick Astley
  // Score available at https://musescore.com/chlorondria_5/never-gonna-give-you-up_alto-sax
  // Arranged by Chlorondria

  NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,4, //1
  NOTE_E5,-4, NOTE_FS5,-4, NOTE_A5,16, NOTE_G5,16, NOTE_FS5,8,
  NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,2,
  NOTE_A4,16, NOTE_A4,16, NOTE_B4,16, NOTE_D5,8, NOTE_D5,16,
  NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,4, //repeat from 1
  NOTE_E5,-4, NOTE_FS5,-4, NOTE_A5,16, NOTE_G5,16, NOTE_FS5,8,
  NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,2,
  NOTE_A4,16, NOTE_A4,16, NOTE_B4,16, NOTE_D5,8, NOTE_D5,16,
  REST,4, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_D5,8, NOTE_E5,8, NOTE_CS5,-8,
  NOTE_B4,16, NOTE_A4,2, REST,4, 

  REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,4, NOTE_A4,8, //7
  NOTE_A5,8, REST,8, NOTE_A5,8, NOTE_E5,-4, REST,4, 
  NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_D5,8, NOTE_E5,8, REST,8,
  REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
  REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4,
  NOTE_E5,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4, REST,4,
 
 
};

// sizeof gives the number of bytes, each int value is composed of two bytes (16 bits)
// there are two values per note (pitch and duration), so for each note there are four bytes
int notes1 = sizeof(melody1) / sizeof(melody1[0]) / 2;

// this calculates the duration of a whole note in ms
int wholenote = 1714;   //(60000 * 4) / tempo; milisegundos

int divider = 0, noteDuration = 0;

void tono (float frec)
{
    float Cuentas;
    unsigned int CuentasEnt;
    TCCR1A = 0x40;  //Timer 1 en CTC
    TCCR1B = 0x09;  //Con pre-esacalador CK
    Cuentas = 500000.0/frec;
    //500000*8 para que haga 8 veces mas cuentas
    CuentasEnt=Cuentas;
    //formas de redondeo             //Ej 1 Cuentas=100.99                //Ej 2 Cuentas=100.49
//    if((Cuentas-CuentasEnt) >= 0.5)  //Ej 1 CuentasEnt=100                //Ej 2 CuentasEnt=100
//        CuentasEnt++;                //Ej 1 Cuentas-CuentasEnt=0.99       //Ej 2 Cuentas-CuentasEnt=49
                                     //Ej 1 CuentasEnt=101                //Ej 2 CuentasEnt=100
    CuentasEnt=Cuentas+0.5;   
    OCR1AH=(CuentasEnt-1)/256;
    OCR1AL=(CuentasEnt-1)%256;
 }
 
void noTono()
{
    TCCR1A=0x00;
    TCCR1B=0x00; //apaga el timer y por ende ya no genera una frecuencia de salida
    PORTB.1=0; //Lo mandamos a 0 si llega a quedar un 1 logico
    //pero esta secuestrado por CTC, ya que no me va a hacer caso si lo dejo asi por eso agrego lo de arriba
    
}


void playMelody(int melody[], int notes)
{
    int thisNote;
    for (thisNote = 0; thisNote < notes * 2; thisNote = thisNote + 2) {

        // calculates the duration of each note
        divider = melody[thisNote + 1];
        if (divider > 0) {
          // regular note, just proceed
          noteDuration = (wholenote) / divider;
        } else if (divider < 0) {
          // dotted notes are represented with negative durations!! 
          divider=(-1)*divider;
          noteDuration = (wholenote) / (divider);
          noteDuration = 1.5*noteDuration; // increases the duration in half for dotted notes
        }
                
        tono(melody[thisNote]);
        delay_ms(noteDuration*0.9);
        noTono();
        delay_ms(noteDuration * 0.1); 
    }
 }  


void setColor(int led, char color) {
    switch (led) {
        case 1:
            RED1 = (color == 'R' || color == 'Y' || color == 'M' || color == 'W');
            GREEN1 = (color == 'G' || color == 'Y' || color == 'C' || color == 'W');
            BLUE1 = (color == 'B' || color == 'C' || color == 'M' || color == 'W');
            break;
        case 2:
            RED2 = (color == 'R' || color == 'Y' || color == 'M' || color == 'W');
            GREEN2 = (color == 'G' || color == 'Y' || color == 'C' || color == 'W');
            BLUE2 = (color == 'B' || color == 'C' || color == 'M' || color == 'W');
            break;
        case 3:
            RED3 = (color == 'R' || color == 'Y' || color == 'M' || color == 'W');
            GREEN3 = (color == 'G' || color == 'Y' || color == 'C' || color == 'W');
            BLUE3 = (color == 'B' || color == 'C' || color == 'M' || color == 'W');
            break;
        case 4:
            RED4 = (color == 'R' || color == 'Y' || color == 'M' || color == 'W');
            GREEN4 = (color == 'G' || color == 'Y' || color == 'C' || color == 'W');
            BLUE4 = (color == 'B' || color == 'C' || color == 'M' || color == 'W');
            break;
        case 5:
            RED5 = (color == 'R' || color == 'Y' || color == 'M' || color == 'W');
            GREEN5 = (color == 'G' || color == 'Y' || color == 'C' || color == 'W');
            BLUE5 = (color == 'B' || color == 'C' || color == 'M' || color == 'W');
            break;
    }
}

void main(void)
{
    // USART initialization
    // Communication Parameters: 8 Data, 1 Stop, No Parity
    // USART Receiver: On
    // USART Transmitter: On
    // USART0 Mode: Asynchronous
    // USART Baud Rate: 9600 (Double Speed Mode)
    UCSR0A=(0<<RXC0) | (0<<TXC0) | (0<<UDRE0) | (0<<FE0) | (0<<DOR0) | (0<<UPE0) | (1<<U2X0) | (0<<MPCM0);
    UCSR0B=(0<<RXCIE0) | (0<<TXCIE0) | (0<<UDRIE0) | (1<<RXEN0) | (1<<TXEN0) | (0<<UCSZ02) | (0<<RXB80) | (0<<TXB80);
    UCSR0C=(0<<UMSEL01) | (0<<UMSEL00) | (0<<UPM01) | (0<<UPM00) | (0<<USBS0) | (1<<UCSZ01) | (1<<UCSZ00) | (0<<UCPOL0);
    UBRR0H=0x00;
    UBRR0L=0x0C; 

 

    DDRB = 0xFE;
    DDRC = 0x3F; 
    DDRD = 0x5C;   
    
    PORTB.1=0;   
    

while (1) {
        // Verificar si hay un caracter listo para leer
        if ((UCSR0A & 0x80) != 0) {
            dato = getchar(); // Leer caracter del puerto serie

            if (estadoTono == 0) {
                if (dato == 'T') {
                    playMelody(melody1, notes1);
                } else {
                    // Leer el siguiente carácter solo si es un número válido para LED
                    if (dato >= '1' && dato <= '5') {
                        led = dato - '0'; // Convertir char a int
                        color = getchar(); // Leer el siguiente caracter para el color
                        // Verificar que el color sea un carácter válido (R, G, B, Y, C, M, W)
                        if (color == 'R' || color == 'G' || color == 'B' || color == 'Y' || 
                            color == 'C' || color == 'M' || color == 'W') {
                            printf("LED: %d, Color: %c\r", led, color);
                            setColor(led, color); // Establecer el color según los datos recibidos
                        } else {
                            // Manejo de error para caracteres inválidos
                            printf("Error: Caracter de color inválido: %c\r", color);
                        }
                    } else {
                        // Manejo de error para caracteres de LED inválidos
                        printf("Error: Caracter de LED inválido: %c\r", dato);
                    }
                }
            }
        }
    }

}
