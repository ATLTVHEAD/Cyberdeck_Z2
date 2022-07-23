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
    def __init__(self, scl_pin, sda_pin):
        self.i2c = busio.I2C(scl_pin, sda_pin)
        self.mcp = MCP23017(self.i2c, 0x20)  # MCP23017
        self.sensor = LSM6DSOX(self.i2c)

    def createButtons():
        pass


class Fbutton:
    def __init__(self):
        pass