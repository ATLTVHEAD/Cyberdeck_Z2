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
    _kPins = 0
    _mPins = list()

    def __init__(self, scl_pin, sda_pin, kPins, mPins):
        self._kPins = kPins
        self._mPins = mPins
        self.i2c = busio.I2C(scl_pin, sda_pin)
        self.mcp = MCP23017(self.i2c, 0x20)  # MCP23017
        self.sensor = LSM6DSOX(self.i2c)
        self.keyboard = Keyboardz(self.mcp, self._kPins)
        self.mouse = Mousez(self._mPins)

    def updateFiddler(self):
        self.keyboard.updateKeyboard()
        self.mouse.updateMouse()

    def testTotalButtons(self):
        for ind, switch in enumerate(self.keyboard._kButtons):
            if switch.rose:
                print('Just released keyboard pin '+ str(ind))
            if switch.long_press:
                print('Long Press keyboard pin '+ str(ind))
                print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (self.sensor.acceleration))
                print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (self.sensor.gyro))
            if switch.short_count != 0:
                print("Short Press Count  keyboardPin" + str(ind) + " =", switch.short_count)
            if switch.long_press and switch.short_count == 1:
                print("That's a long double press keyboard!")
        for ind, switch in enumerate(self.mouse._mButtons):
            if switch.rose:
                print('Just released mouse pin '+ str(ind))
            if switch.long_press:
                print('Long Press mouse pin '+ str(ind))
                print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (self.sensor.acceleration))
                print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (self.sensor.gyro))
            if switch.short_count != 0:
                print("Short Press Count mouse Pin" + str(ind) + " =", switch.short_count)
            if switch.long_press and switch.short_count == 1:
                print("That's a long double press mouse!")

    # Figure out Chording Next


class Keyboardz:
    _kPins = 0
    _pins = list()
    _kButtons = list()

    def __init__(self, MPC, kPins):
        self._kPins = kPins
        self._mcp = MPC
        self.setKPins()
        self.setKeyboardButtons()

    def setKPins(self):
        print("setting Keyboard pins")
        for i in range(self._kPins):
            self._pins.append(self._mcp.get_pin(i))
        for pin in self._pins:
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP 

    def setKeyboardButtons(self):
        print("setting Keyboard Buttons")
        for pin in self._pins:
            self._kButtons.append(Button(pin))

    def updateKeyboard(self):
        for _button in self._kButtons:
            _button.update()



class Mousez:
    _mPins= list()
    _pins = list()
    _mButtons = list()

    def __init__(self,mPins):
        self._mPins = mPins
        self.setMPins()
        self.setMouseButtons()


    def setMPins(self):
        print("setting Mouse pins")
        for digitalButton in self._mPins:
            self._pins.append(digitalio.DigitalInOut(digitalButton))
        for pin in self._pins:
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP
    
    def setMouseButtons(self):
        print("setting Mouse Buttons")
        for pin in self._pins:
            self._mButtons.append(Button(pin))

    def updateMouse(self):
        for _button in self._mButtons:
            _button.update()