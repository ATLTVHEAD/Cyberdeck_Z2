# By ATLTVHEAD 
#   atltvhead@gmail.com
#   Created: 7/22/2022
#   updated:
#   Purpose: Main code for switching operational modes 

import Fiddler
import time
import board
import digitalio



# Initialize the I2C bus:
sda_pin = board.SDA
scl_pin = board.SCL

glove = Fiddler.Fiddler(scl_pin,sda_pin)


pin0 = glove.mcp.get_pin(0)


# Setup pin0 as an output that's at a high logic level.
pin0.direction = digitalio.Direction.INPUT
pin0.pull = digitalio.Pull.UP
switch = Fiddler.Button(pin0)

# Now loop blinking the pin 0 output and reading the state of pin 1 input.
while True:
    switch.update()
    if switch.rose:
        print('Just released')
    if switch.long_press:
        print("Long Press")
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (glove.sensor.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (glove.sensor.gyro))
    if switch.short_count != 0:
        print("Short Press Count =", switch.short_count)
    if switch.long_press and switch.short_count == 1:
        print("That's a long double press !")
    #print("Pin 1 is at a high level: {0}".format(pin0.value))
