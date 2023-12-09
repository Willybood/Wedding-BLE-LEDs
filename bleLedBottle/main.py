from ubluetooth import BLE
import plasma
from plasma import plasma_stick
from math import sin
from bleRemoteScanner import startScanningForRemotes
from bleBottleTransmitter import BLERemoteTransmitter

"""
Simple pulsing effect generated using a sine wave.
"""

# Set how many LEDs you have
NUM_LEDS = 50

# we're using HSV colours in this example - find more at https://colorpicker.me/
# to convert a hue that's in degrees, divide it by 360
COLOUR = 0.5

MAX_LED_BRIGHTNESS = 1.0
MIN_LED_BRIGHTNESS = 0.3

SPEED = 0.002

BLE_NAME = "wedBot"
BLE_INTERVAL_MS = 250

# set up the WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

# start updating the LED strip
led_strip.start()

offset = 0

bt = BLE()
bleTransmitter = BLERemoteTransmitter(bt, BLE_NAME, BLE_INTERVAL_MS)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == "__main__":
    startScanningForRemotes(bt, bleTransmitter)
    while True:
        # use a sine wave to set the brightness
        mappedValue = map(sin(offset), 1.0, -1.0, 1.0, 0.3)
        for i in range(NUM_LEDS):
            led_strip.set_hsv(i, COLOUR, 1.0, mappedValue)
        offset += SPEED