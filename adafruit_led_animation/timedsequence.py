# SPDX-FileCopyrightText: 2020 Gamblor21
#
# SPDX-License-Identifier: MIT
"""
`adafruit_led_animation.timedsequence`
================================================================================

Animation timed sequence helper for CircuitPython helper library for LED animations.


* Author(s): Mark Komus

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

from adafruit_led_animation.sequence import AnimationSequence
from . import MS_PER_SECOND


class TimedAnimationSequence(AnimationSequence):
    """
    A sequence of Animations to run in succession, each animation running for an
    individual amount of time.
    :param members: The animation objects or groups followed by how long the animation
                    should run in seconds.
    :param bool auto_clear: Clear the pixels between animations. If ``True``, the current animation
                            will be cleared from the pixels before the next one starts.
                            Defaults to ``False``.
    :param bool random_order: Activate the animations in a random order. Defaults to ``False``.
    :param bool auto_reset: Automatically call reset() on animations when changing animations.
    .. code-block:: python
        import board
        import neopixel
        from adafruit_led_animation.timedsequence import TimedAnimationSequence
        import adafruit_led_animation.animation.comet as comet_animation
        import adafruit_led_animation.animation.sparkle as sparkle_animation
        import adafruit_led_animation.animation.blink as blink_animation
        import adafruit_led_animation.color as color
        strip_pixels = neopixel.NeoPixel(board.A1, 30, brightness=1, auto_write=False)
        blink = blink_animation.Blink(strip_pixels, 0.2, color.RED)
        comet = comet_animation.Comet(strip_pixels, 0.1, color.BLUE)
        sparkle = sparkle_animation.Sparkle(strip_pixels, 0.05, color.GREEN)
        animations = TimedAnimationSequence(blink, 5, comet, 3, sparkle, 7)
        while True:
            animations.animate()
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self, *members, auto_clear=True, random_order=False, auto_reset=False, name=None
    ):
        self._animation_members = []
        self._animation_timings = []
        for x, item in enumerate(members):
            if not x % 2:
                self._animation_members.append(item)
            else:
                self._animation_timings.append(item)

        super().__init__(
            *self._animation_members,
            auto_clear=auto_clear,
            random_order=random_order,
            auto_reset=auto_reset,
            advance_on_cycle_complete=False,
            name=name,
        )
        self._advance_interval = self._animation_timings[self._current] * MS_PER_SECOND

    def activate(self, index):
        super().activate(index)
        self._advance_interval = self._animation_timings[self._current] * MS_PER_SECOND
