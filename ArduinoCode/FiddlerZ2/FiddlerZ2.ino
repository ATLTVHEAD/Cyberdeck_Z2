// Atltvhead      atltvhead@gmail.com
// created 7/7/2022
// FiddlerZ2 code for an arduino nano rp2040 connect and an MCP23017
//  for reading in a chorded keyboard array


#include <Adafruit_MCP23X17.h>

#define BUTTON_PIN_1 1   // MCP23XXX pin used for interrupt
#define BUTTON_PIN_2 28   // MCP23XXX pin used for interrupt

#define INT_PIN_1 3      // microcontroller pin attached to INTA/B

volatile byte state = LOW;
byte oldState = LOW;

Adafruit_MCP23X17 mcp;

void setup() {
  Serial.begin(9600);
  //while (!Serial);
  Serial.println("MCP23xxx Interrupt Test!");

  // uncomment appropriate mcp.begin
  if (!mcp.begin_I2C()) {
  //if (!mcp.begin_SPI(CS_PIN)) {
    Serial.println("Error.");
    while (1);
  }

  // configure MCU pin that will read INTA/B state
  pinMode(INT_PIN_1, INPUT);
  attachInterrupt(digitalPinToInterrupt(INT_PIN_1), blink, CHANGE);

  // OPTIONAL - call this to override defaults
  // mirror INTA/B, active drive, signaled with a LOW
  mcp.setupInterrupts(true, true, LOW);

  // configure button pin for input with pull up
  mcp.pinMode(BUTTON_PIN_1, INPUT_PULLUP);
  mcp.pinMode(BUTTON_PIN_2, INPUT_PULLUP);
  
  // enable interrupt on button_pin
  mcp.setupInterruptPin(BUTTON_PIN_1, CHANGE);
  mcp.setupInterruptPin(BUTTON_PIN_2, CHANGE);

  Serial.println("Looping...");
}

void loop() {
  delay(500);
  if(state != oldState){
    Serial.println(mcp.getLastInterruptPin());
    Serial.println(state);
  }
 oldState = state;
}

void blink() {
  state = !state;
}