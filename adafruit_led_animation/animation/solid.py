# The MIT License (MIT)
#
# Copyright (c) 2019-2020 Roy Hooper
# Copyright (c) 2020 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_led_animation.animation.solid`
================================================================================

TODO

* Author(s): Roy Hooper, Kattni Rembor

"""

from adafruit_led_animation.animation.colorcycle import ColorCycle


class Solid(ColorCycle):
    """
    A solid color.

    :param pixel_object: The initialised LED object.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    """

    def __init__(self, pixel_object, color, name=None):
        super().__init__(pixel_object, speed=1, colors=[color], name=name)

    def _recompute_color(self, color):
        self.colors = [color]