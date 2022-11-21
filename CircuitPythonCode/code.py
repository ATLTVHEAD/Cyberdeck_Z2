# By ATLTVHEAD 
#   atltvhead@gmail.com
#   Created: 7/22/2022
#   updated:
#   Purpose: Main code for switching operational modes 

import Fiddler
import secrets
import time
import board
import busio
import json

# Initialize the I2C bus:
sda_pin = board.SDA
scl_pin = board.SCL
mouse_pins = [board.D8, board.D9, board.D10, board.D11, board.D12]
keyboard_pin_number = 16

glove = Fiddler.Fiddler(scl_pin, sda_pin, keyboard_pin_number, mouse_pins)

# Now loop through glove functions
while True:
    glove.updateFiddler()
    #glove.main()
