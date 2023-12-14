from random import randint
from rgbkeypad import RGBKeypad
import bluetooth
import struct
from bleRemoteTransmitter import BLERemoteTransmitter
from time import sleep
from math import sin

# Constants
bleName = "wedRem"
bleIntervalMs = 250
timeBetweenGpioChecksSec = 0.2
unselectedButtonOption = 99
defaultButtons = [0, 0]

# Module variables
ble = bluetooth.BLE()
bleTransmitter = BLERemoteTransmitter(ble, bleName, bleIntervalMs)
keypad = RGBKeypad()
keypad.brightness = 1.0

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

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Uses a sine wave to set the brightness and colours to match the bottle pattern they correspond to
vSlowPulseOffset = 0
slowPulseOffset = 0
mediumPulseOffset = 0
fastPulseOffset = 0
def processKeyColours():
    V_SLOW_PULSE_SPEED = 0.025
    SLOW_PULSE_SPEED = 0.05
    MEDIUM_PULSE_SPEED = 0.1
    FAST_PULSE_SPEED = 0.2
    global vSlowPulseOffset
    global slowPulseOffset
    global mediumPulseOffset
    global fastPulseOffset
    vSlowPulseOffset += V_SLOW_PULSE_SPEED
    slowPulseOffset += SLOW_PULSE_SPEED
    mediumPulseOffset += MEDIUM_PULSE_SPEED
    fastPulseOffset += FAST_PULSE_SPEED
    slowMappedValue = map(sin(slowPulseOffset), 1.0, -1.0, 1.0, 0.0)
    mediumMappedValue = map(sin(mediumPulseOffset), 1.0, -1.0, 1.0, 0.0)
    fastMappedValue = map(sin(fastPulseOffset), 1.0, -1.0, 1.0, 0.0)
    keypad[0, 1].brightness = slowMappedValue
    keypad[1, 1].brightness = slowMappedValue
    keypad[2, 1].brightness = slowMappedValue
    keypad[3, 1].brightness = slowMappedValue
    keypad[0, 2].brightness = mediumMappedValue
    keypad[1, 2].brightness = mediumMappedValue
    keypad[2, 2].brightness = mediumMappedValue
    keypad[3, 2].brightness = mediumMappedValue
    keypad[0, 3].color = (int(fastMappedValue * 255), 0, int((1.0 - fastMappedValue) * 255))
    keypad[1, 3].color = (int(slowMappedValue * 255), int(mediumMappedValue * 255), int(fastMappedValue * 255))
    snowMappedValue = map(vSlowPulseOffset % 1.0, 1.0, 0.0, 0.0, 1.0)
    if(snowMappedValue > 1.0):
        keypad[2, 3].brightness = 1.0
    else:
        keypad[2, 3].brightness = snowMappedValue
    treeLightMappedValue = vSlowPulseOffset % 1.0
    TREE_LIGHT_COLOURS = ((255, 0, 0), # red
                         (255,165,0),  # orange
                         (0, 0, 255),  # blue
                         (255,20,147), # pink
                         (0, 255, 0))  # green
    treeColor = TREE_LIGHT_COLOURS[0]
    for index, treeLightColour in enumerate(TREE_LIGHT_COLOURS):
        treeLightLength = len(TREE_LIGHT_COLOURS)
        if(treeLightMappedValue < (index / treeLightLength)):
            treeColor = TREE_LIGHT_COLOURS[index]
            break;
    keypad[3, 3].color = (treeColor[0], treeColor[1], treeColor[2])

def processKeyGPIO():
    previousKey = [defaultButtons[0], defaultButtons[1]]
    currentlySelectedKey = [defaultButtons[0], defaultButtons[1]]
    buttonCurrentlyPushed = False
    while True:
        processKeyColours()
        for x in range(4):
            for y in range(4):
                key = keypad[x,y]
                if key.is_pressed() and x == currentlySelectedKey[0] and y == currentlySelectedKey[1] and buttonCurrentlyPushed == False: # If the button is pushed again
                    bleTransmitter.advertise(unselectedButtonOption, unselectedButtonOption)
                    buttonCurrentlyPushed = True
                    currentlySelectedKey = [unselectedButtonOption, unselectedButtonOption]
                elif key.is_pressed() and buttonCurrentlyPushed == False: # If a new button is pushed
                    previousKey = [x,y]
                    bleTransmitter.advertise(x, y)
                    currentlySelectedKey = [x, y]
                    buttonCurrentlyPushed = True
                elif key.is_pressed() == False and (x == previousKey[0] and y == previousKey[1]) and buttonCurrentlyPushed: # If the button is released
                    buttonCurrentlyPushed = False
                    
if __name__ == "__main__":
    bleTransmitter.advertise(defaultButtons[0], defaultButtons[1])
    setupKeyColours()
    processKeyGPIO()
