# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.sparklepulse`
================================================================================

Sparkle-pulse animation for CircuitPython helper library for LED animations.

* Author(s): dmolavi

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.helper import pulse_generator


class SparklePulse(Sparkle):
    """
    Combination of the Sparkle and Pulse animations.

    :param pixel_object: The initialised LED object.
    :param int speed: Animation refresh rate in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param period: Period to pulse the LEDs over.  Default 5.
    :param max_intensity: The maximum intensity to pulse, between 0 and 1.0.  Default 1.
    :param min_intensity: The minimum intensity to pulse, between 0 and 1.0.  Default 0.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        color,
        period=5,
        max_intensity=1,
        min_intensity=0,
        name=None,
    ):
        self._max_intensity = max_intensity
        self._min_intensity = min_intensity
        self._period = period
        dotstar = len(pixel_object) == 4 and isinstance(pixel_object[0][-1], float)
        super().__init__(
            pixel_object, speed=speed, color=color, num_sparkles=1, name=name
        )
        self._generator = pulse_generator(self._period, self, dotstar_pwm=dotstar)

    def _set_color(self, color):
        self._color = color

    def draw(self):
        self._sparkle_color = next(self._generator)
        super().draw()

    def after_draw(self):
        self.show()
