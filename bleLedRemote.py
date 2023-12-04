from random import randint
from rgbkeypad import RGBKeypad
import bluetooth

keypad = RGBKeypad()
keypad.brightness = 0.5 # From 0 to 1

while True:
    for x in range(4):
        for y in range(4):
            key = keypad[x,y]
            if key.is_pressed():
                key.color = (
                    randint(0,255),
                    randint(0,255),
                    randint(0,255)
                    )
                print("key", x, y, "pressed")
