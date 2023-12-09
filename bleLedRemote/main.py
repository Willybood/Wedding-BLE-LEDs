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
unselectedButtonOption = 99
defaultButtons = [0, 0]

# Module variables
ble = bluetooth.BLE()
bleTransmitter = BLERemoteTransmitter(ble, bleName, bleIntervalMs)
keypad = RGBKeypad()
keypad.brightness = unselectedBrightness

def setupKeyColours():
    keypad[0, 0].color = (255, 255, 0)
    keypad[1, 0].color = (0, 0, 255)
    keypad[2, 0].color = (128, 0, 128)
    keypad[3, 0].color = (255, 0, 0)
    keypad[0, 1].color = (255, 255, 0)
    keypad[1, 1].color = (0, 255, 255)
    keypad[2, 1].color = (128, 0, 128)
    keypad[3, 1].color = (255, 0, 0)
    keypad[0, 2].color = (255, 255, 0)
    keypad[1, 2].color = (0, 0, 255)
    keypad[2, 2].color = (128, 0, 128)
    keypad[3, 2].color = (255, 0, 0)
    keypad[0, 3].color = (0, 0, 255)
    keypad[1, 3].color = (255, 0, 0)
    keypad[2, 3].color = (240, 255, 255)
    keypad[3, 3].color = (0, 255, 0)

def processKeys():
    previousKey = [defaultButtons[0], defaultButtons[1]]
    currentlySelectedKey = [defaultButtons[0], defaultButtons[1]]
    keypad[defaultButtons[0], defaultButtons[1]].brightness = 1
    buttonCurrentlyPushed = False
    while True:
        sleep(timeBetweenGpioChecksSec)
        for x in range(4):
            for y in range(4):
                key = keypad[x,y]
                if key.is_pressed() and x == currentlySelectedKey[0] and y == currentlySelectedKey[1] and buttonCurrentlyPushed == False: # If the button is pushed again
                    if(previousKey[0] < 4 and previousKey[1] < 4): # If the values are in range
                        keypad[previousKey[0], previousKey[1]].brightness = unselectedBrightness
                    bleTransmitter.advertise(unselectedButtonOption, unselectedButtonOption)
                    buttonCurrentlyPushed = True
                    currentlySelectedKey = [unselectedButtonOption, unselectedButtonOption]
                elif key.is_pressed() and buttonCurrentlyPushed == False: # If a new button is pushed
                    if(previousKey[0] < 4 and previousKey[1] < 4): # If the values are in range
                        keypad[previousKey[0], previousKey[1]].brightness = unselectedBrightness
                    previousKey = [x,y]
                    key.brightness = 1
                    bleTransmitter.advertise(x, y)
                    currentlySelectedKey = [x, y]
                    buttonCurrentlyPushed = True
                elif key.is_pressed() == False and (x == previousKey[0] and y == previousKey[1]) and buttonCurrentlyPushed: # If the button is released
                    buttonCurrentlyPushed = False
                    
if __name__ == "__main__":
    bleTransmitter.advertise(defaultButtons[0], defaultButtons[1])
    setupKeyColours()
    processKeys()
