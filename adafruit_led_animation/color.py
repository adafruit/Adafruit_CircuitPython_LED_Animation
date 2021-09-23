# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.color`
================================================================================

Color variables assigned to RGB values made available for import.

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""
# Makes colorwheel() available.
from rainbowio import colorwheel  # pylint: disable=unused-import

RED = (255, 0, 0)
"""Red."""
YELLOW = (255, 150, 0)
"""Yellow."""
ORANGE = (255, 40, 0)
"""Orange."""
GREEN = (0, 255, 0)
"""Green."""
TEAL = (0, 255, 120)
"""Teal."""
CYAN = (0, 255, 255)
"""Cyan."""
BLUE = (0, 0, 255)
"""Blue."""
PURPLE = (180, 0, 255)
"""Purple."""
MAGENTA = (255, 0, 20)
"""Magenta."""
WHITE = (255, 255, 255)
"""White."""
BLACK = (0, 0, 0)
"""Black or off."""

GOLD = (255, 222, 30)
"""Gold."""
PINK = (242, 90, 255)
"""Pink."""
AQUA = (50, 255, 255)
"""Aqua."""
JADE = (0, 255, 40)
"""Jade."""
AMBER = (255, 100, 0)
"""Amber."""
OLD_LACE = (253, 245, 230)  # Warm white.
"""Old lace or warm white."""

RGBW_WHITE_RGB = (255, 255, 255, 0)
"""RGBW_WHITE_RGB is for RGBW strips to illuminate only the RGB diodes."""
RGBW_WHITE_W = (0, 0, 0, 255)
"""RGBW_WHITE_W is for RGBW strips to illuminate only White diode."""
RGBW_WHITE_RGBW = (255, 255, 255, 255)
"""RGBW_WHITE_RGBW is for RGBW strips to illuminate the RGB and White diodes."""

RAINBOW = (RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
"""RAINBOW is a list of colors to use for cycling through.
Includes, in order: red, orange, yellow, green, blue, and purple."""


def calculate_intensity(color, intensity=1.0):
    """
    Takes a RGB[W] color tuple and adjusts the intensity.
    :param float intensity:
    :param color: color value (tuple, list or int)
    :return: color
    """
    # Note: This code intentionally avoids list comprehensions and intermediate variables
    # for an approximately 2x performance gain.
    if isinstance(color, int):
        return (
            (int((color & 0xFF0000) * intensity) & 0xFF0000)
            | (int((color & 0xFF00) * intensity) & 0xFF00)
            | (int((color & 0xFF) * intensity) & 0xFF)
        )

    if len(color) == 3:
        return (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity),
        )
    if len(color) == 4 and isinstance(color[3], float):
        return (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity),
            color[3],
        )
    return (
        int(color[0] * intensity),
        int(color[1] * intensity),
        int(color[2] * intensity),
        int(color[3] * intensity),
    )
