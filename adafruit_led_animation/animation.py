# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
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
`adafruit_led_animation.animation`
================================================================================

CircuitPython helper library for LED animations.


* Author(s): Roy Hooper, Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

import time
from .color import BLACK
import random

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"


class Animation:
    # TODO: rename pixel_object to something more beginner friendly
    def __init__(self, pixel_object, speed):
        self.pixel_object = pixel_object
        self.speed = speed
        self._next_update = time.monotonic()
        self.pixel_object.auto_write = False

    def _timing_control(self):
        now = time.monotonic()
        if now >= self._next_update:
            self._next_update = now + self.speed
            return True
        return False


class Blink(Animation):
    def __init__(self, pixel_object, speed, color_on, color_off=BLACK):
        self.color_on = color_on
        self.color_off = color_off
        self._state = False
        super(Blink, self).__init__(pixel_object, speed)

    def animate(self):
        if not self._timing_control():
            return
        self._state = not self._state
        self.pixel_object.fill(self.color_on if self._state else self.color_off)
        self.pixel_object.show()


class Comet(Animation):
    def __init__(self, pixel_object, speed, color, tail_length=10):
        self._tail_length = tail_length
        self._color_step = 0.8 / tail_length
        self._color_offset = 0.2
        self.color = color
        super(Comet, self).__init__(pixel_object, speed)
        self._generator = self._comet_generator()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._compute_color()

    def _compute_color(self):
        self._comet_colors = [
            [int(self._color[rgb] * ((n * self._color_step) + self._color_offset))
                for rgb in range(len(self._color))
            ] for n in range(self._tail_length)
        ]

    def _comet_generator(self):
        num_pixels = len(self.pixel_object)
        while True:
            for start in range(-self._tail_length, num_pixels + 1):
                if start > 0:
                    self.pixel_object[start-1] = 0
                end = self._tail_length if start + self._tail_length < num_pixels else num_pixels - start
                if start < 0:
                    num_visible = self._tail_length + start
                    self.pixel_object[0:num_visible] = self._comet_colors[self._tail_length - num_visible:]
                else:
                    self.pixel_object[start:start + end] = self._comet_colors[0:end]
                self.pixel_object.show()
                yield

    def animate(self):
        if not self._timing_control():
            return
        next(self._generator)


class Sparkle(Animation):
    def __init__(self, pixel_object, speed, color):
        self._half_color = None
        self._dim_color = None
        super(Sparkle, self).__init__(pixel_object, speed)
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        half_color = tuple(value[rgb] // 2 for rgb in range(len(value)))
        dim_color = tuple(value[rgb] // 10 for rgb in range(len(value)))
        for pixel in range(len(self.pixel_object)):
            if self.pixel_object[pixel] == self._half_color:
                self.pixel_object[pixel] = half_color
            else:
                self.pixel_object[pixel] = dim_color
        self._half_color = half_color
        self._dim_color = dim_color
        self._color = value

    def animate(self):
        if not self._timing_control():
            return
        pixel = random.randint(0, (len(self.pixel_object) - 2))
        self.pixel_object[pixel] = self._color
        self.pixel_object.show()
        self.pixel_object[pixel] = self._half_color
        self.pixel_object[pixel + 1] = self._dim_color
        self.pixel_object.show()
