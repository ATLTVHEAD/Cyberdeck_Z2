# By ATLTVHEAD 
#   atltvhead@gmail.com
#   Created: 7/22/2022
#   updated:
#   Purpose: a Class for the fiddler, containing buttons, and sensors in the keyboard 
# 

import time
import board
import busio
import digitalio
from adafruit_debouncer import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

class Fiddler:
    _pins = list()
    _fButtons = list()

    def __init__(self, scl_pin, sda_pin):
        self.i2c = busio.I2C(scl_pin, sda_pin)
        self.mcp = MCP23017(self.i2c, 0x20)  # MCP23017
        self.sensor = LSM6DSOX(self.i2c)
        self.setBPins()
        self.setButtons()

    def setBPins(self):
        print("setting pins")
        for i in range(16):
            self._pins.append(self.mcp.get_pin(i)) 
        self._pins.append(digitalio.DigitalInOut(board.D8))
        self._pins.append(digitalio.DigitalInOut(board.D9))
        self._pins.append(digitalio.DigitalInOut(board.D10))
        self._pins.append(digitalio.DigitalInOut(board.D11))
        self._pins.append(digitalio.DigitalInOut(board.D12))
        for pin in self._pins:
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP

        
    def setButtons(self):
        print("setting Buttons")
        for pin in self._pins:
            self._fButtons.append(Button(pin))
    
    def updateButtons(self):
        for _button in self._fButtons:
            _button.update()

    def testButtons(self):
        for ind, switch in enumerate(self._fButtons):
            if switch.rose:
                print('Just released pin '+ str(ind))
            if switch.long_press:
                print('Long Press pin '+ str(ind))
                print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (self.sensor.acceleration))
                print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (self.sensor.gyro))
            if switch.short_count != 0:
                print("Short Press Count Pin" + str(ind) + " =", switch.short_count)
            if switch.long_press and switch.short_count == 1:
                print("That's a long double press !")

    # Figure out Chording Next
