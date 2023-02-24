# SPDX-FileCopyrightText: 2022 Tim Cocks
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.multicolor_comet`
================================================================================

Multi-color Comet animation for CircuitPython helper library for LED animations.

* Author(s): Kattni Rembor, Tim Cocks

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import BLACK


class MulticolorComet(Comet):
    """
    A multi-color comet animation.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param colors: Animation colors in a list or tuple of entries in
                            ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param int tail_length: The length of the comet. Defaults to 25% of the length of the
                            ``pixel_object``. Automatically compensates for a minimum of 2 and a
                            maximum of the length of the ``pixel_object``.
    :param bool reverse: Animates the comet in the reverse order. Defaults to ``False``.
    :param bool bounce: Comet will bounce back and forth. Defaults to ``True``.
    :param Optional[string] name: A human-readable name for the Animation.
                                  Used by the to string function.
    :param bool ring: Ring mode.  Defaults to ``False``.
    :param bool off_pixels: Turn pixels off after the animation passes them. Defaults to ``True``.
                            Setting to False will result in all pixels not currently in the comet
                            to remain on and set to a color after the comet passes.
    """

    # pylint: disable=too-many-arguments,too-many-instance-attributes
    def __init__(
        self,
        pixel_object,
        speed,
        colors,
        *,
        tail_length=0,
        reverse=False,
        bounce=False,
        name=None,
        ring=False,
        off_pixels=True,
    ):
        if tail_length == 0:
            tail_length = len(pixel_object) // 4
        if bounce and ring:
            raise ValueError("Cannot combine bounce and ring mode")
        self.bounce = bounce
        self._reverse = reverse
        self._initial_reverse = reverse
        self._tail_length = tail_length

        self._comet_colors = None

        self._num_pixels = len(pixel_object)
        self._direction = -1 if reverse else 1
        self._left_side = -self._tail_length
        self._right_side = self._num_pixels
        self._tail_start = 0
        self._ring = ring
        self._colors = colors
        if colors is None or len(colors) < 2:
            raise ValueError("Must pass at least two colors.")

        self._off_pixels = off_pixels
        if ring:
            self._left_side = 0
        self.reset()
        super().__init__(
            pixel_object,
            speed,
            0x0,
            name=name,
            tail_length=tail_length,
            bounce=bounce,
            ring=ring,
            reverse=reverse,
        )

    on_cycle_complete_supported = True

    def _set_color(self, color):
        if self._off_pixels:
            self._comet_colors = [BLACK]
        else:
            self._comet_colors = []

        for n in range(self._tail_length):
            _float_index = ((len(self._colors)) / self._tail_length) * n
            _color_index = int(_float_index)
            self._comet_colors.append(self._colors[_color_index])
