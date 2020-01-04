"""
Example animation sequence.
"""
from adafruit_led_animation.animation import Comet, AnimationSequence, Chase
from adafruit_led_animation.color import PURPLE, WHITE
import neopixel
import board

pixels = neopixel.NeoPixel(board.D6, 32, brightness=0.2, auto_write=False)
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
animations = AnimationSequence(comet, chase, advance_interval=15)

while True:
    animations.animate()
