# SPDX-FileCopyrightText: 2022 Tim Cocks
#
# SPDX-License-Identifier: MIT
"""
This example animates a red, yellow, and green chase animation.

For QT Py Haxpress and a NeoPixel strip. Update pixel_pin and pixel_num to match your wiring if
using a different board or form of NeoPixels.

This example will run on SAMD21 (M0) Express boards (such as Circuit Playground Express or QT Py
Haxpress), but not on SAMD21 non-Express boards (such as QT Py or Trinket).
"""
import board
import neopixel
from adafruit_led_animation.animation.multicolor_chase import MulticolorChase


# Update to match the pin connected to your NeoPixels
pixel_pin = board.D9
# Update to match the number of NeoPixels you have connected
pixel_num = 96
brightness = 0.03

pixels = neopixel.NeoPixel(
    pixel_pin,
    pixel_num,
    brightness=brightness,
    auto_write=True,
    pixel_order=neopixel.RGB,
)

gradient_colors = [
    0xFF0000,
    0xFD2000,
    0xF93E00,
    0xF45B00,
    0xEC7500,
    0xE28D00,
    0xD5A200,
    0xC6B500,
    0xB5C600,
    0xA2D500,
    0x8DE200,
    0x75EC00,
    0x5BF400,
    0x3EF900,
    0x20FD00,
    0x00FF00,
]

chase = MulticolorChase(
    pixels,
    speed=0.05,
    size=3,
    spacing=8,
    colors=(0xFF0000, 0xFFFF00, 0x00FF00),
    # colors=gradient_colors, # try this one for smoother color transition
)

while True:
    chase.animate()
