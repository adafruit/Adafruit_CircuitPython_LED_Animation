"""
This example repeatedly displays two animations, Comet and Chase, at a five second interval.

Designed for NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.
"""
import board
import neopixel
from adafruit_led_animation.animation import Comet, Chase
from adafruit_led_animation.helper import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)

comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)

animations = AnimationSequence(comet, chase, advance_interval=5)

while True:
    animations.animate()
