# SPDX-FileCopyrightText: 2020 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.pulse`
================================================================================

Pulse animation for CircuitPython helper library for LED animations.

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

from adafruit_led_animation.animation import Animation


class Pulse(Animation):
    """
    Pulse all pixels a single color.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation refresh rate in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param period: Period to pulse the LEDs over.  Default 5.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, pixel_object, speed, color, period=5, name=None):
        super().__init__(pixel_object, speed, color, name=name)
        self._period = period
        self._generator = None
        self.reset()

    on_cycle_complete_supported = True

    def draw(self):
        color = next(self._generator)
        self.pixel_object.fill(color)

    def reset(self):
        """
        Resets the animation.
        """
        dotstar = len(self.pixel_object[0]) == 4 and isinstance(
            self.pixel_object[0][-1], float
        )
        from adafruit_led_animation.helper import (  # pylint: disable=import-outside-toplevel
            pulse_generator,
        )

        self._generator = pulse_generator(self._period, self, dotstar_pwm=dotstar)
