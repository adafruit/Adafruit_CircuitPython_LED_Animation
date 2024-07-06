# SPDX-FileCopyrightText: 2019 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.pulse_generator`
================================================================================

Helper method for pulse generation

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

from . import MS_PER_SECOND, monotonic_ms
from .color import calculate_intensity


def pulse_generator(period: float, animation_object, dotstar_pwm=False):
    """
    Generates a sequence of colors for a pulse, based on the time period specified.
    :param period: Pulse duration in seconds.
    :param animation_object: An animation object to interact with.
    :param dotstar_pwm: Whether to use the dostar per pixel PWM value for brightness control.
    """
    period = int((period + (animation_object.breath * 2)) * MS_PER_SECOND)
    half_breath = int(animation_object.breath * MS_PER_SECOND // 2)
    half_period = period // 2

    last_update = monotonic_ms()
    cycle_position = 0
    last_pos = 0
    while True:
        now = monotonic_ms()
        time_since_last_draw = now - last_update
        last_update = now
        pos = cycle_position = (cycle_position + time_since_last_draw) % period
        if pos < last_pos:
            animation_object.cycle_complete = True
        last_pos = pos
        if pos > half_period:
            pos = period - pos
        if pos < half_breath:
            intensity = animation_object.min_intensity
        elif pos > (half_period - half_breath):
            intensity = animation_object.max_intensity
        else:
            intensity = animation_object.min_intensity + (
                ((pos - half_breath) / (half_period - (half_breath * 2)))
                * (animation_object.max_intensity - animation_object.min_intensity)
            )
        if dotstar_pwm:
            fill_color = (
                animation_object.color[0],
                animation_object.color[1],
                animation_object.color[2],
                intensity,
            )
            yield fill_color
            continue
        yield calculate_intensity(animation_object.color, intensity)
