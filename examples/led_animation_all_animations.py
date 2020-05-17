"""
This example repeatedly displays all available animations, at a five second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example does not work on SAMD21 (M0) boards.
"""
import board
import neopixel

import adafruit_led_animation.animation.blink
import adafruit_led_animation.animation.sparklepulse
from adafruit_led_animation import animation
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)

blink = adafruit_led_animation.animation.animation.blink.Blink(
    pixels, speed=0.5, color=JADE
)
comet = animation.Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = animation.Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = animation.Pulse(pixels, speed=0.1, period=3, color=AMBER)
sparkle = adafruit_led_animation.animation.animation.sparkle.Sparkle(
    pixels, speed=0.1, color=PURPLE, num_sparkles=10
)
solid = adafruit_led_animation.animation.animation.solid.Solid(pixels, color=JADE)
rainbow = adafruit_led_animation.animation.animation.rainbow.Rainbow(
    pixels, speed=0.1, period=2
)
sparkle_pulse = adafruit_led_animation.animation.animation.sparklepulse.SparklePulse(
    pixels, speed=0.1, period=3, color=JADE
)
rainbow_comet = adafruit_led_animation.animation.animation.rainbowcomet.RainbowComet(
    pixels, speed=0.1, tail_length=7, bounce=True
)
rainbow_chase = adafruit_led_animation.animation.animation.rainbowchase.RainbowChase(
    pixels, speed=0.1, size=3, spacing=2, wheel_step=8
)


animations = AnimationSequence(
    comet,
    blink,
    chase,
    pulse,
    sparkle,
    solid,
    rainbow,
    sparkle_pulse,
    rainbow_comet,
    rainbow_chase,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
