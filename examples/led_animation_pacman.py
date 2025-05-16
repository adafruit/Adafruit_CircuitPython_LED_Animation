# SPDX-FileCopyrightText: 2025 Jose D. Montoya
# SPDX-License-Identifier: MIT

"""
This example animates a Pacman on a NeoPixel strip.
"""

import board
import neopixel

from adafruit_led_animation.animation.pacman import Pacman
from adafruit_led_animation.color import WHITE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D6
# Update to match the number of NeoPixels you have connected
num_pixels = 50

# Create the NeoPixel object
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels,
    brightness=0.5,
    auto_write=False,
    pixel_order=ORDER,
)

# Create the Pacman animation object
pacman = Pacman(pixels, speed=0.1, color=WHITE)

# Main loop
while True:
    pacman.animate()
