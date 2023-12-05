import plasma
from plasma import plasma_stick

LEDS = 30
FPS = 60
BRIGHTNESS = 15 # Between 0 and 31

led_strip = plasma.WS2812(LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)
led_strip.start(FPS)
led_strip.set_brightness(BRIGHTNESS)

led_strip.set_rgb(0, 255, 0, 255)
