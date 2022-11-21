# By ATLTVHEAD 
#   atltvhead@gmail.com
#   Created: 7/22/2022
#   updated:
#   Purpose: a Class for the fiddler, containing buttons, and sensors in the keyboard 
# 

import secrets
import time
import json
import board
import busio
import digitalio
from adafruit_debouncer import Button
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi



class Fiddler:
    _kPins = 0
    _mPins = list()
    mode = 0


    def __init__(self, scl_pin, sda_pin, kPins, mPins):
        self._kPins = kPins
        self._mPins = mPins
        self.i2c = busio.I2C(scl_pin, sda_pin)
        self.mcp = MCP23017(self.i2c, 0x20)  # MCP23017
        self.sensor = LSM6DSOX(self.i2c)
        self.keyboard = Keyboardz(self.mcp, self._kPins)
        self.mouse = Mousez(self._mPins)
        self.setWiFiPins()
        self.connectAndTestWiFi()

    def updateFiddler(self):
        if(self.keyboard.updateKeyboard()):
            print(self.keyboard._kChord)
            self.s.connect(self.socketaddr, conntype=self.esp.UDP_MODE)
            paket = bytearray(json.dumps({'chord': self.keyboard._kChord}))
            self.s.send(paket)
            self.s.close()
            
            self.keyboard.cleanupChord()
        self.mouse.updateMouse()
    
    def setMode(self):
        if(self.mouse._mButtons[0].long_press):
            self.mode = self.mode + 1
            if(self.mode>4):
                self.mode = 0

    def main(self):
        self.setMode()
        if(self.mode == 0):
            self.testTotalButtons()
        else:
            print("Mode = {}".format(self.mode))

    def testTotalButtons(self):
        self.keyboard.testKeyboard(self.sensor)
        self.mouse.testMouse()
        
    def setWiFiPins(self):
        #  ESP32 pins
        self.esp32_cs = digitalio.DigitalInOut(board.CS1)
        self.esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)
        self.esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)
        #  uses the secondary SPI connected through the ESP32
        self.spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
        self.esp = adafruit_esp32spi.ESP_SPIcontrol(self.spi, self.esp32_cs, self.esp32_ready, self.esp32_reset)
    
    def connectAndTestWiFi(self):
        # connect to wifi AP
        self.esp.connect(secrets.secrets_stuff)

        # test for connectivity to server
        print("Server ping:", self.esp.ping(secrets.HOST), "ms")

        # create the socket
        socket.set_interface(self.esp)
        self.socketaddr = socket.getaddrinfo(secrets.HOST, secrets.PORT)[0][4]
        self.s = socket.socket(type=socket.SOCK_DGRAM)

        self.s.settimeout(secrets.TIMEOUT)

        print("Sending")
        self.s.connect(self.socketaddr, conntype=self.esp.UDP_MODE)
        packet = bytearray(json.dumps({'chord': 253, 'test': [3,4,True]}))
        self.s.send(packet)
        self.s.close()


class Keyboardz:
    _kPins = 0
    _pins = list()
    _kButtons = list()
    _kChord = list()
    _kPressed = list()
    keyboard_ready = False

    def __init__(self, MPC, kPins):
        self._kPins = kPins
        self._mcp = MPC
        self.setKPins()
        self.setKeyboardButtons()

    def setKPins(self):
        print("setting Keyboard pins")
        for i in range(self._kPins):
            self._pins.append(self._mcp.get_pin(i))
            self._kChord.append(False)
            self._kPressed.append(False)
        for pin in self._pins:
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP 

    def setKeyboardButtons(self):
        print("setting Keyboard Buttons")
        for pin in self._pins:
            self._kButtons.append(Button(pin))

    def updateKeyboard(self):
        for ind, _button in enumerate(self._kButtons):
            _button.update()
            #This is where Double presses would need to be counted for updating, instead of bools compare ints? 
            if(_button.fell):
                self._kPressed[ind] = True
                self._kChord[ind] = False
            if(_button.rose):
                self._kChord[ind] = True
            
        #This method would need to change to allow for double presses, instead of bools compare ints? 
        self.isChordReady()
        return self.keyboard_ready

    #This method would need to change to allow for double presses, instead of bools compare ints? 
    def isChordReady(self):
        for ind in range(self._kPins):
            if(self._kPressed[ind] != self._kChord[ind]):
                self.keyboard_ready = False
                break
            elif(self._kPressed[ind] != False):
                self.keyboard_ready = True
                
    #This method would need to change to allow for double presses, instead of bools compare ints? 
    def cleanupChord(self):
        self.keyboard_ready = False
        for ind in range(self._kPins):
            self._kPressed[ind] = False
            self._kChord[ind] = False

    def testKeyboard(self, _sensor):
        for ind, switch in enumerate(self._kButtons):
            if switch.rose:
                print('Just released keyboard pin '+ str(ind))
            if switch.long_press:
                print('Long Press keyboard pin '+ str(ind))
                print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (_sensor.acceleration))
                print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (_sensor.gyro))
            if switch.short_count != 0:
                print("Short Press Count  keyboardPin" + str(ind) + " =", switch.short_count)
            if switch.long_press and switch.short_count == 1:
                print("That's a long double press keyboard!")
        
        



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
    
    def testMouse(self):
        for ind, switch in enumerate(self._mButtons):
            if switch.rose:
                print('Just released mouse pin '+ str(ind))
            if switch.long_press:
                print('Long Press mouse pin '+ str(ind))
            if switch.short_count != 0:
                print("Short Press Count mouse Pin" + str(ind) + " =", switch.short_count)
            if switch.long_press and switch.short_count == 1:
                print("That's a long double press mouse!")