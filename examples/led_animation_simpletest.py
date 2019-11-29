import board
import neopixel
from adafruit_led_animation.animation import Blink
import adafruit_led_animation.color as color

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)
blink = Blink(pixels, 0.5, color.PURPLE)

while True:
    blink.animate()
