"""
This simpletest example repeatedly displays two animations, Comet and Chase, at a five second
interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example does not work on SAMD21 (M0) boards.
"""
import board
import neopixel
import adafruit_led_animation.animation.comet as comet_animation
import adafruit_led_animation.animation.chase as chase_animation
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)

comet = comet_animation.Comet(
    pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True
)
chase = chase_animation.Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)

animations = AnimationSequence(comet, chase, advance_interval=5)

while True:
    animations.animate()
