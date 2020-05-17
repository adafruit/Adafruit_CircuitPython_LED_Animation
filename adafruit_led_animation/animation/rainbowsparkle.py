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
`adafruit_led_animation.animation.rainbowcomet`
================================================================================

TODO

* Author(s): Roy Hooper, Kattni Rembor

"""

import random

from adafruit_led_animation.animation.rainbow import Rainbow


class RainbowSparkle(Rainbow):

    def __init__(self, pixel_object, speed, period=5, num_sparkles=None, step=1, name=None,
                 bg_brightness=0.2):
        self._num_sparkles = num_sparkles
        if num_sparkles is None:
            self._num_sparkles = max(1, int(len(pixel_object) / 20))
        self._sparkle_duration = 2
        self._bg_brightness = bg_brightness
        self._bright_colors = None
        super().__init__(pixel_object=pixel_object, speed=speed, period=period, step=step, name=name,
                         precompute_rainbow=True)

    def generate_rainbow(self, step=1):
        super().generate_rainbow()
        self._bright_colors = self.colors[:]
        for i, color in enumerate(self.colors):
            if isinstance(self.colors[i], int):
                self.colors[i] = (
                    int(self._bg_brightness * ((color & 0xff0000) >> 16)),
                    int(self._bg_brightness * ((color & 0xff00) >> 8)),
                    int(self._bg_brightness * (color & 0xff))
                )
            else:
                self.colors[i] = (
                    int(self._bg_brightness * color[0]),
                    int(self._bg_brightness * color[1]),
                    int(self._bg_brightness * color[2])
                )

    def show(self):
        pixels = [
            random.randint(0, len(self.pixel_object)-1)
            for n in range(self._num_sparkles)
        ]
        for pixel in pixels:
            bc = (self._wheel_index + pixel) % len(self._bright_colors)
            self.pixel_object[pixel] = self._bright_colors[bc]
        super().show()
