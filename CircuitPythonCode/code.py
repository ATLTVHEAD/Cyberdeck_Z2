# By ATLTVHEAD 
#   atltvhead@gmail.com
#   Created: 7/22/2022
#   updated:
#   Purpose: Main code for switching operational modes 

import Fiddler
import time
import board
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from digitalio import DigitalInOut
import busio
import struct
import json

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

#  ESP32 pins
esp32_cs = DigitalInOut(board.CS1)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

#  uses the secondary SPI connected through the ESP32
spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

TIMEOUT = 5
# edit host and port to match server
HOST = "pool.ntp.org"
PORT = 123
NTP_TO_UNIX_EPOCH = 2208988800  # 1970-01-01 00:00:00

# connect to wifi AP
esp.connect(secrets)

# test for connectivity to server
print("Server ping:", esp.ping(HOST), "ms")

# create the socket
socket.set_interface(esp)
socketaddr = socket.getaddrinfo(HOST, PORT)[0][4]
s = socket.socket(type=socket.SOCK_DGRAM)

s.settimeout(TIMEOUT)

print("Sending")
s.connect(socketaddr, conntype=esp.UDP_MODE)
packet = bytearray(48)
packet[0] = 0b00100011  # Not leap second, NTP version 4, Client mode
s.send(packet)

print("Receiving")
packet = s.recv(48)
seconds = struct.unpack_from("!I", packet, offset=len(packet) - 8)[0]
print("Time:", time.localtime(seconds - NTP_TO_UNIX_EPOCH))



# Initialize the I2C bus:
sda_pin = board.SDA
scl_pin = board.SCL
mouse_pins = [board.D8, board.D9, board.D10, board.D11, board.D12]
keyboard_pin_number = 16

glove = Fiddler.Fiddler(scl_pin, sda_pin, keyboard_pin_number, mouse_pins)

# Now loop through glove functions
while True:
    glove.updateFiddler()
    glove.main()
