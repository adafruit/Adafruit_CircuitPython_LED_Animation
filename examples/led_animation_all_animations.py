"""
This example repeatedly displays all available animations, at a five second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example does not work on SAMD21 (M0) boards.
"""
import board
import neopixel

import adafruit_led_animation.animation.blink as blink_animation
import adafruit_led_animation.animation.sparklepulse as sparklepulse_animation
import adafruit_led_animation.animation.comet as comet_animation
import adafruit_led_animation.animation.chase as chase_animation
import adafruit_led_animation.animation.pulse as pulse_animation
import adafruit_led_animation.animation.sparkle as sparkle_animation
import adafruit_led_animation.animation.rainbowchase as rainbowchase_animation
import adafruit_led_animation.animation.rainbowsparkle as rainbowsparkle_animation
import adafruit_led_animation.animation.rainbowcomet as rainbowcomet_animation
import adafruit_led_animation.animation.solid as solid_animation
import adafruit_led_animation.animation.colorcycle as colorcycle_animation
import adafruit_led_animation.animation.rainbow as rainbow_animation
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)

blink = blink_animation.Blink(pixels, speed=0.5, color=JADE)
colorcycle = colorcycle_animation.ColorCycle(
    pixels, speed=0.4, colors=[MAGENTA, ORANGE]
)
comet = comet_animation.Comet(
    pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True
)
chase = chase_animation.Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = pulse_animation.Pulse(pixels, speed=0.1, period=3, color=AMBER)
sparkle = sparkle_animation.Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = solid_animation.Solid(pixels, color=JADE)
rainbow = rainbow_animation.Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = sparklepulse_animation.SparklePulse(
    pixels, speed=0.1, period=3, color=JADE
)
rainbow_comet = rainbowcomet_animation.RainbowComet(
    pixels, speed=0.1, tail_length=7, bounce=True
)
rainbow_chase = rainbowchase_animation.RainbowChase(
    pixels, speed=0.1, size=3, spacing=2, wheel_step=8
)
rainbow_sparkle = rainbowsparkle_animation.RainbowSparkle(
    pixels, speed=0.1, num_sparkles=15
)


animations = AnimationSequence(
    comet,
    blink,
    rainbow_sparkle,
    chase,
    pulse,
    sparkle,
    rainbow,
    solid,
    rainbow_comet,
    sparkle_pulse,
    rainbow_chase,
    advance_interval=5,
    auto_clear=True,
)

while True:
    animations.animate()
