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

struct EmaButton {
  const uint8_t pin;
  uint32_t numberKeyPresses;
  bool currentState;
  bool previousState;
  int ema;
  int oldEma;
  bool isMcp;
};

class EmaButton2{
  public:
    const uint8_t pin;
    uint32_t numberKeyPresses;
    bool currentState;
    bool previousState;
    int ema;
    int oldEma;
    bool isMcp;
};