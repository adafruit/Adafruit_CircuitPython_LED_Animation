"""
This example repeatedly displays all available animations, at a five second interval.

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.
"""
import board
import neopixel
from adafruit_led_animation import animation
from adafruit_led_animation.helper import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
pixel_num = 32

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)

blink = animation.Blink(pixels, speed=0.1, color=JADE)
comet = animation.Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = animation.Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
pulse = animation.Pulse(pixels, speed=0.1, period=3, color=AMBER)
sparkle = animation.Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
solid = animation.Solid(pixels, color=JADE)
rainbow = animation.Rainbow(pixels, speed=0.1, period=2)
sparkle_pulse = animation.SparklePulse(pixels, speed=0.1, period=3, color=JADE)
rainbow_comet = animation.RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
rainbow_chase = animation.RainbowChase(
    pixels, speed=0.1, size=3, spacing=2, wheel_step=8
)


animations = AnimationSequence(
    blink,
    comet,
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
