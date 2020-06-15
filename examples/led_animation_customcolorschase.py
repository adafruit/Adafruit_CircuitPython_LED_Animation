"""
This example displays the basic animations in sequence, at a five second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example may not work on SAMD21 (M0) boards.
"""
import board
import neopixel

from adafruit_led_animation.animation.customcolorschase import CustomColorsChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PINK, PURPLE, GREEN, RED, WHITE, BLUE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D5
# Update to match the number of NeoPixels you have connected
pixel_num = 32
brightness = 0.3

pixels = neopixel.NeoPixel(
    pixel_pin, pixel_num, brightness=brightness, auto_write=False
)

# colors default to RAINBOW
custom_colors_chase_rainbow = CustomColorsChase(pixels, speed=0.1, size=2, spacing=3)
# Patriotic
custom_colors_chase_rwb = CustomColorsChase(
    pixels, speed=0.1, colors=[RED, WHITE, BLUE], size=2, spacing=3
)
# St Pat Day
custom_colors_chase_gw = CustomColorsChase(
    pixels, speed=0.1, colors=[GREEN, WHITE], size=2, spacing=3
)
# Christmas
custom_colors_chase_rg = CustomColorsChase(
    pixels, speed=0.1, colors=[RED, GREEN], size=2, spacing=3
)
custom_colors_chase_rg_r = CustomColorsChase(
    pixels, speed=0.1, colors=[RED, GREEN], size=1, spacing=2, reverse=True
)
# Valentines Day
custom_colors_chase_rp = CustomColorsChase(
    pixels, speed=0.1, colors=[RED, PINK], size=2, spacing=3
)


animations = AnimationSequence(
    custom_colors_chase_rainbow,
    custom_colors_chase_rp,
    custom_colors_chase_gw,
    custom_colors_chase_rwb,
    custom_colors_chase_rg,
    custom_colors_chase_rg_r,
    advance_interval=6,
    auto_clear=True,
)

while True:
    animations.animate()
