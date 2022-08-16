# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.grid_rain`
================================================================================

Rain animations for CircuitPython helper library for LED animations.

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

import random
from adafruit_led_animation.animation import Animation

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"

from adafruit_led_animation.color import BLACK, colorwheel, calculate_intensity, GREEN


class Rain(Animation):
    """
    Droplets of rain.

    :param grid_object: The initialised PixelGrid object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param count: Number of sparkles to generate per animation cycle.
    :param length: Number of pixels per raindrop (Default 3)
    :param background: Background color (Default BLACK).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self, grid_object, speed, color, count=1, length=3, background=BLACK, name=None
    ):
        self._count = count
        self._length = length
        self._background = background
        self._raindrops = []
        super().__init__(grid_object, speed, color, name=name)

    def draw(self):

        # Move raindrops down
        keep = []
        for raindrop in self._raindrops:
            pixels = []
            if raindrop[1][0][0] >= 0:
                self.pixel_object[raindrop[0], raindrop[1][0][0]] = self._background
            for pixel in raindrop[1]:
                pixel[0] += 1
                if pixel[0] < self.pixel_object.height:
                    pixels.append(pixel)
            if pixels:
                keep.append([raindrop[0], pixels])
        self._raindrops = keep

        # Add a raindrop
        if len(self._raindrops) < self._count:
            x = random.randint(0, self.pixel_object.width - 1)
            self._raindrops.append([x, self._generate_droplet(x, self._length)])

        # Draw raindrops
        for x, pixels in self._raindrops:
            for y, color in pixels:
                if y >= 0:
                    self.pixel_object[x, y] = color

    def _generate_droplet(self, x, length):  # pylint: disable=unused-argument
        return [[n, self.color] for n in range(-length, 0)]


class RainbowRain(Rain):
    """
    Rainbow Rain animation.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self, grid_object, speed, count=1, length=3, background=BLACK, name=None
    ):
        super().__init__(grid_object, speed, BLACK, count, length, background, name)

    def _generate_droplet(self, x, length):
        color = colorwheel(random.randint(0, 255))
        return [
            [n, calculate_intensity(color, 1.0 - -((n + 1) / (length + 1)))]
            for n in range(-length, 0)
        ]


class MatrixRain(Rain):
    """
    The Matrix style animation.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        grid_object,
        speed,
        color=GREEN,
        count=1,
        length=6,
        background=(0, 32, 0),
        name=None,
    ):
        super().__init__(grid_object, speed, color, count, length, background, name)

    def _generate_droplet(self, x, length):
        return [
            [n, calculate_intensity(self.color, random.randint(10, 100) * 1.0)]
            for n in range(-length, 0)
        ]
