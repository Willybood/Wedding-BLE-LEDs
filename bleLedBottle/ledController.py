import plasma
from plasma import plasma_stick
from math import sin
from random import random, uniform
from time import ticks_ms
from snow import snow
from sparkles import sparkle
from tree import setupTree, tree

# Set how many LEDs you have
NUM_LEDS = 50
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

previousCheckedMs = 0

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Uses a sine wave to set the brightness
pulseOffset = 0
def pulse(hueValue):
    SPEED = 0.002
    MAX_LED_BRIGHTNESS = 1.0
    MIN_LED_BRIGHTNESS = 0.3
    
    global pulseOffset
    mappedValue = map(sin(pulseOffset), 1.0, -1.0, 1.0, 0.3)
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, hueValue, 1.0, mappedValue)
    pulseOffset += SPEED
    
def solidColour(red, green, blue):
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, red, green, blue)

# Fire effect! Random red/orange hue, full saturation, random brightness
def fireEffect():
    global previousCheckedMs
    lightChangeDelayMs = 100
    currentMs = ticks_ms()
    if(currentMs != previousCheckedMs and currentMs % lightChangeDelayMs == 0):
        previousCheckedMs = currentMs
        for i in range(NUM_LEDS):
            led_strip.set_hsv(i, uniform(0.0, 50 / 360), 1.0, random())
    
# Rainbow colour effect
rainbowOffset = 0.0
def rainbows():
    global previousCheckedMs
    global rainbowOffset
    SPEED = 20 # The SPEED that the LEDs cycle at (1 - 255)
    UPDATES = 60 # How many times the LEDs will be updated per second
    
    lightChangeDelayMs = int((1.0 / UPDATES) * 1000.0)
    currentMs = ticks_ms()
    if(currentMs != previousCheckedMs and currentMs % lightChangeDelayMs == 0):
        rainbowOffset += float(SPEED) / 2000.0
        previousCheckedMs = currentMs
        for i in range(NUM_LEDS):
            hue = float(i) / NUM_LEDS
            led_strip.set_hsv(i, hue + rainbowOffset, 1.0, 1.0)

def turnLedsOff():
    solidColour(0, 0, 0)

previousPatternGroup = 99
previousSubPattern = 99
def playLedPattern(patternGroup, subPattern):
    global previousPatternGroup
    global previousSubPattern
    if(0 == patternGroup):
        if(0 == subPattern):
            solidColour(255, 255, 0) # Yellow
        elif(1 == subPattern):
            solidColour(0, 0, 255) # Blue
        elif(2 == subPattern):
            solidColour(128, 0, 128) # Purple
        elif(3 == subPattern):
            solidColour(255, 0, 0) # Red
        else:
            turnLedsOff()
    elif(1 == patternGroup):
        if(0 == subPattern):
            pulse(0.1) # Yellow
        elif(1 == subPattern):
            pulse(0.5) # Blue
        elif(2 == subPattern):
            pulse(0.8) # Purple
        elif(3 == subPattern):
            pulse(1.0) # Red
        else:
            turnLedsOff()
    elif(2 == patternGroup):
        if(0 == subPattern):
            sparkle(led_strip, NUM_LEDS, [255, 255, 0], [50, 50, 0]) # Yellow
        elif(1 == subPattern):
            sparkle(led_strip, NUM_LEDS, [0, 0, 255], [0, 0, 50]) # Blue
        elif(2 == subPattern):
            sparkle(led_strip, NUM_LEDS, [128, 0, 128], [25, 0, 25]) # Purple
        elif(3 == subPattern):
            sparkle(led_strip, NUM_LEDS, [255, 0, 0], [50, 0, 0]) # Red
        else:
            turnLedsOff()
    elif(3 == patternGroup):
        if(0 == subPattern):
            sparkle(led_strip, NUM_LEDS, [0, 0, 255], [255, 0, 0]) # Blue and Red
        elif(1 == subPattern):
            rainbows()
        elif(2 == subPattern):
            snow(led_strip, NUM_LEDS)
        elif(3 == subPattern):
            if(previousPatternGroup != patternGroup or previousSubPattern != subPattern):
                setupTree(led_strip, NUM_LEDS)
            tree(led_strip, NUM_LEDS)
        else:
            turnLedsOff()
    else:
        turnLedsOff()
    
    previousPatternGroup = patternGroup
    previousSubPattern = subPattern

def setupLeds():
    # Set up the WS2812 / NeoPixel™ LEDs
    # Start updating the LED strip
    led_strip.start()

if __name__ == "__main__":
    setupLeds()
    while True:
        playLedPattern(3, 3)