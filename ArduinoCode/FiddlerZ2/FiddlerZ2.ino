// Atltvhead      atltvhead@gmail.com
// created 7/7/2022
// FiddlerZ2 code for an arduino nano rp2040 connect and an MCP23017
//  for reading in a chorded keyboard array
//
//PURPOSE: send out button 
//  
//Features:
//    -single and multi button press (B1+B2)



////////////////////////////////////////////////////////////////

#include <Adafruit_MCP23X17.h>
#include "ButtonBouncer.h"
#include "Keymap.h"

#define BUTTON_PIN_1 1   // MCP23XXX pin used for interrupt
#define BUTTON_PIN_2 28   // MCP23XXX pin used for interrupt

#define INT_PIN_1 3      // microcontroller pin attached to INTA/B

Adafruit_MCP23X17 mcp;


Glove glove;

EmaButton buttons[TOTAL_BUTTONS] = {
  {0,0,false,false,false,false,128,128,true},
  {1,0,false,false,false,false,128,128,true},
  {2,0,false,false,false,false,128,128,true},
  {3,0,false,false,false,false,128,128,true},
  {4,0,false,false,false,false,128,128,true},
  {5,0,false,false,false,false,128,128,true},
  {6,0,false,false,false,false,128,128,true},
  {7,0,false,false,false,false,128,128,true},
  {8,0,false,false,false,false,128,128,true},
  {9,0,false,false,false,false,128,128,true},
  {10,0,false,false,false,false,128,128,true},
  {11,0,false,false,false,false,128,128,true},
  {12,0,false,false,false,false,128,128,true},
  {13,0,false,false,false,false,128,128,true},
  {14,0,false,false,false,false,128,128,true},
  {15,0,false,false,false,false,128,128,true},
  {12,0,false,false,false,false,128,128,false},
  {11,0,false,false,false,false,128,128,false},
  {10,0,false,false,false,false,128,128,false},
  {9,0,false,false,false,false,128,128,false},
  {8,0,false,false,false,false,128,128,false},
};

int mode = 0;


void setup() {
  Serial.begin(9600);
  Serial.println("MCP23xxx Interrupt Test!");

  if (!mcp.begin_I2C()) {
    Serial.println("Error.");
    while (1);
  }

  for(int i=0;i<TOTAL_BUTTONS;i++){
    if(buttons[i].isMcp){mcp.pinMode(buttons[i].pin, INPUT_PULLUP);}
    else{pinMode(buttons[i].pin, INPUT_PULLUP);}
  }

  glove.glove_ready = false;

  for(int i =0; i<TOTAL_BUTTONS; i++){
    glove.bpressed[i] = false;
    glove.breleased[i] = false;
  }

  Serial.println("Looping...");
}

void loop() {
  buttonUpdater();
  gloveUpdater();
  if(glove.glove_ready==true){
    modeSetter();
    switch(mode){
      case 1:
        yield();
        break;
      default:
        chordingCompare();
        break;
    }
    gloveReseter();
  }
}
//-------------------------------------------------------------------------------

void buttonUpdater(){
  for(int i=0; i< TOTAL_BUTTONS; i++){
    if(buttons[i].isMcp){
      buttons[i].rawState = mcp.digitalRead(buttons[i].pin);
    }
    else{
      buttons[i].rawState = digitalRead(buttons[i].pin);
    }
    buttons[i].calcEma();
    buttons[i].setbuttonState();
    buttons[i].setOldEma();
  }
}

void gloveReseter(){
  for(int i=0; i<TOTAL_BUTTONS; i++){
    //Serial.print(", ");
    glove.bpressed[i] = false;
    glove.breleased[i] = false;
  }
  //Serial.println("]");
  glove.glove_ready=false;

}

void gloveUpdater(){
  for(int i=0; i< TOTAL_BUTTONS; i++){
    if(buttons[i].changedState){
      if(buttons[i].rose()){
        glove.breleased[i]= true;
      }
      else if(buttons[i].fell()){
        glove.bpressed[i] = true;
        glove.breleased[i]= false;
      }
    }
  }
  for (int i = 0; i < TOTAL_BUTTONS; i++)  {
    if(glove.bpressed[i] != glove.breleased[i]){
      glove.glove_ready=false;
      break;
    }
    else if(glove.bpressed[i] != false){glove.glove_ready=true;}
  }
}

void chordingCompare(){
  Serial.println("Glove is ready");
  //Serial.print("[");
  int gloveInt = buttonsToInt(glove.bpressed);
  if(gloveInt - buttonsToInt(_a) == 0){
    Serial.println("a");
  }
  else if(gloveInt - buttonsToInt(_b) == 0){
    Serial.println("b");
  }
}

int buttonsToInt(bool bols[]){
  int recivedID = 0;
  for(int i=0; i<NUM_MCP_BUTTONS; i++){
    recivedID |= bols[i] << i;
  }
  return recivedID;
}

void modeSetter(){
  yield();
}