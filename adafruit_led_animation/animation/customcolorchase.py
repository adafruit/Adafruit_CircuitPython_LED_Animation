# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
# SPDX-FileCopyrightText: 2020 Connie Sieh for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.customcolorchase`
================================================================================

Custom color chase animation for CircuitPython helper library for LED animations.

* Author(s): Kattni Rembor, Connie Sieh

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""

from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.color import RAINBOW


class CustomColorChase(Chase):
    """
    Chase pixels in one direction, like a theater marquee with Custom Colors

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed rate in seconds, e.g. ``0.1``.
    :param colors: Animation colors in list of `(r, g, b)`` tuple, or ``0x000000`` hex format
    :param size: Number of pixels to turn on in a row.
    :param spacing: Number of pixels to turn off in a row.
    :param reverse: Reverse direction of movement.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        size=2,
        spacing=3,
        reverse=False,
        name=None,
        colors=RAINBOW,
    ):
        self._num_colors = len(colors)
        self._colors = colors
        self._color_idx = 0
        super().__init__(pixel_object, speed, 0, size, spacing, reverse, name)

    def bar_color(self, n, pixel_no=0):
        return self._colors[self._color_idx - (n % len(self._colors))]

    def on_cycle_complete(self):
        self._color_idx = (self._color_idx + self._direction) % len(self._colors)
        super().on_cycle_complete()
