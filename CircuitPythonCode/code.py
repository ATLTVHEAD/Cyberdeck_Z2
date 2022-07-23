# By ATLTVHEAD 
#   atltvhead@gmail.com
#   Created: 7/22/2022
#   updated:
#   Purpose: Main code for switching operational modes 

import Fiddler
import time
import board



# Initialize the I2C bus:
sda_pin = board.SDA
scl_pin = board.SCL

glove = Fiddler.Fiddler(scl_pin,sda_pin)


# Now loop through glove functions
while True:
    glove.updateButtons()
    glove.testButtons()
