# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.sparkle`
================================================================================

Sparkle animation for CircuitPython helper library for LED animations.

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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"


class Sparkle(Animation):
    """
    Sparkle animation of a single color.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param num_sparkles: Number of sparkles to generate per animation cycle.
    :param mask: array to limit sparkles within range of the mask
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self, pixel_object, speed, color, num_sparkles=1, name=None, mask=None
    ):
        if len(pixel_object) < 2:
            raise ValueError("Sparkle needs at least 2 pixels")
        if mask:
            self._mask = mask
        else:
            self._mask = []
        if len(self._mask) >= len(pixel_object):
            raise ValueError("Sparkle mask should be smaller than number pixel array")
        self._half_color = color
        self._dim_color = color
        self._sparkle_color = color
        self._num_sparkles = num_sparkles
        self._num_pixels = len(pixel_object)
        self._pixels = []
        super().__init__(pixel_object, speed, color, name=name)

    def _set_color(self, color):
        half_color = tuple(color[rgb] // 4 for rgb in range(len(color)))
        dim_color = tuple(color[rgb] // 10 for rgb in range(len(color)))
        for pixel in range(  # pylint: disable=consider-using-enumerate
            len(self.pixel_object)
        ):
            if self.pixel_object[pixel] == self._half_color:
                self.pixel_object[pixel] = half_color
            elif self.pixel_object[pixel] == self._dim_color:
                self.pixel_object[pixel] = dim_color
        self._half_color = half_color
        self._dim_color = dim_color
        self._sparkle_color = color

    def _random_in_mask(self):
        if len(self._mask) == 0:
            return random.randint(0, (len(self.pixel_object) - 1))
        return self._mask[random.randint(0, (len(self._mask) - 1))]

    def draw(self):
        self._pixels = [self._random_in_mask() for _ in range(self._num_sparkles)]
        for pixel in self._pixels:
            self.pixel_object[pixel] = self._sparkle_color

    def after_draw(self):
        self.show()
        for pixel in self._pixels:
            self.pixel_object[pixel % self._num_pixels] = self._half_color
            if (pixel + 1) % self._num_pixels in self._mask:
                self.pixel_object[(pixel + 1) % self._num_pixels] = self._dim_color
