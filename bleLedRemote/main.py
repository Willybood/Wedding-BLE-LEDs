from random import randint
from rgbkeypad import RGBKeypad
import bluetooth
import struct
from bleRemoteTransmitter import BLERemoteTransmitter
from time import sleep

# Constants
bleName = "wedRem"
unselectedBrightness = 0.05 # From 0 to 1
bleIntervalMs = 250
timeBetweenGpioChecksSec = 0.2

# Module variables
ble = bluetooth.BLE()
bleTransmitter = BLERemoteTransmitter(ble, bleName, bleIntervalMs)
keypad = RGBKeypad()
keypad.brightness = unselectedBrightness
keypad.color = (0, 255, 255)

def runLeds():
    previousKey = [0,0] # Set default to the 'off' key
    while True:
        sleep(timeBetweenGpioChecksSec)
        for x in range(4):
            for y in range(4):
                key = keypad[x,y]
                if key.is_pressed() and (x != previousKey[0] or y != previousKey[1]):
                    keypad[previousKey[0], previousKey[1]].brightness = unselectedBrightness
                    previousKey = [x,y]
                    key.brightness = 1
                    bleTransmitter.advertise(x, y)
                    print("key", x, y, "pressed")
    
if __name__ == "__main__":
    runLeds()