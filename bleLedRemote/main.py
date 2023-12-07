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

# Module variables
ble = bluetooth.BLE()
bleTransmitter = BLERemoteTransmitter(ble, bleName, bleIntervalMs)
keypad = RGBKeypad()
keypad.brightness = unselectedBrightness
keypad.color = (0, 255, 255)

def runLeds():
    previousKey = [unselectedButtonOption,unselectedButtonOption]
    currentlySelectedKey = [unselectedButtonOption,unselectedButtonOption]
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
                    print("key", x, y, "depressed")
                elif key.is_pressed() and buttonCurrentlyPushed == False: # If a new button is pushed
                    if(previousKey[0] < 4 and previousKey[1] < 4): # If the values are in range
                        keypad[previousKey[0], previousKey[1]].brightness = unselectedBrightness
                    previousKey = [x,y]
                    key.brightness = 1
                    bleTransmitter.advertise(x, y)
                    currentlySelectedKey = [x, y]
                    buttonCurrentlyPushed = True
                    print("key", x, y, "pressed")
                elif key.is_pressed() == False and (x == previousKey[0] and y == previousKey[1]) and buttonCurrentlyPushed: # If the button is released
                    buttonCurrentlyPushed = False
                    print("key", x, y, "released")
                    
if __name__ == "__main__":
    bleTransmitter.advertise(unselectedButtonOption, unselectedButtonOption)
    runLeds()