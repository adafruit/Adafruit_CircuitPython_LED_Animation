"""
This example displays the basic animations in sequence, at a five second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example may not work on SAMD21 (M0) boards.
"""
import board
import neopixel

from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import (
    PINK,
    PURPLE,
    GREEN,
    RED,
    WHITE,
    BLUE
)

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D5
# Update to match the number of NeoPixels you have connected
pixel_num = 32
brightness = 0.3

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=brightness, auto_write=False)

# colors default to RAINBOW
custom_color_chase_rainbow = CustomColorChase(pixels, speed=0.1, size=2, spacing=3)
# Patriotic
custom_color_chase_rwb = CustomColorChase(pixels, speed=0.1, colors=[RED, WHITE, BLUE], size=2, spacing=3)
# St Pat Day
custom_color_chase_gw = CustomColorChase(pixels, speed=0.1, colors=[GREEN, WHITE], size=2, spacing=3)
# Christmas
custom_color_chase_rg = CustomColorChase(pixels, speed=0.1, colors=[RED, GREEN], size=2, spacing=3)
custom_color_chase_rg_r = CustomColorChase(pixels, speed=0.1, colors=[RED, GREEN], size=2, spacing=3, reverse=True)
# Valentines Day
custom_color_chase_rp = CustomColorChase(pixels, speed=0.1, colors=[RED , PINK], size=2, spacing=3)


animations = AnimationSequence(
    custom_color_chase_rainbow,
    custom_color_chase_rp,
    custom_color_chase_gw,
    custom_color_chase_rwb,
    custom_color_chase_rg,
    custom_color_chase_rg_r,
    advance_interval=6, auto_clear=True,
)

while True:
    animations.animate()
