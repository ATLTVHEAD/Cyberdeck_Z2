/*
    Author: Atltvhead atltvhead.gmail.com
    Purpose: Debounce regular buttons and MPC23017
        buttons given Adafruits MPC23x17 lib.
        Uses Exponential Moving Average to determine
        pressed states.
*/

#define ButtonBouncer_h

#if defined(ARDUINO) && ARDUINO >=100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include <inttypes.h>

class EmaButton{
  public:
    const uint8_t pin;
    uint32_t numberKeyPresses;
    bool rawState;
    bool currentState;
    bool previousState;
    int ema;
    int oldEma;
    bool isMcp;

    void calcEma(){
      ema = (0.25 * rawState * 128) + (oldEma * 0.75);
    }

    void setOldEma(){
      oldEma = ema;
    }

    void setbuttonState(){
      if(ema <=51){
        currentState = true;
      }
      else if (ema >= 77){
        currentState = false;
      }
    }
};