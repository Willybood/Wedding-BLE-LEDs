import plasma
from plasma import plasma_stick
from random import random, choice
from time import ticks_ms

"""
A Christmas tree, with fairy lights!
This will probably work better if your LEDs are in a vaguely tree shaped bottle :)
"""

# Set how many LEDs you have
MAX_NUM_LEDS = 50

previousCheckedMs = 0

# we're using HSV colours in this example - find more at https://colorpicker.me/
# to convert a hue that's in degrees, divide it by 360
TREE_COLOUR = [0.34, 1.0, 0.6]
LIGHT_RATIO = 4  # every nth pixel is a light, the rest are tree.
LIGHT_COLOURS = ((0.0, 1.0, 1.0),   # red
                 (0.1, 1.0, 1.0),   # orange
                 (0.6, 1.0, 1.0),   # blue
                 (0.85, 0.4, 1.0))  # pink
LIGHT_CHANGE_CHANCE = 0.5  # change to 0.0 if you want static lights
LIGHT_CHANGE_DELAY_SEC = 0.5

# initial setup
def setupTree(led_strip, num_leds):
    for i in range(num_leds):
        if i % LIGHT_RATIO == 0:  # add an appropriate number of lights
            led_strip.set_hsv(i, *choice(LIGHT_COLOURS))  # choice randomly chooses from a list
        else:  # GREEN
            led_strip.set_hsv(i, *TREE_COLOUR)

def tree(led_strip, num_leds):
    global previousCheckedMs
    lightChangeDelayMs = int(LIGHT_CHANGE_DELAY_SEC * 1000)
    currentMs = ticks_ms()
    if(currentMs != previousCheckedMs and currentMs % lightChangeDelayMs == 0):
        previousCheckedMs = currentMs
        for i in range(num_leds):
            if (i % LIGHT_RATIO == 0) and (random() < LIGHT_CHANGE_CHANCE):
                led_strip.set_hsv(i, *choice(LIGHT_COLOURS))

if __name__ == "__main__":
    # set up the WS2812 / NeoPixel™ LEDs
    led_strip = plasma.WS2812(MAX_NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)
    # start updating the LED strip
    led_strip.start()
    setupTree(led_strip, MAX_NUM_LEDS)
    while True:
        tree(led_strip, MAX_NUM_LEDS)