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

try:
    from time import monotonic_ns
except ImportError:
    import time

    def monotonic_ns():
        """
        Implementation of monotonic_ns for platforms without time.monotonic_ns
        """
        return int(time.time() * 1000000000)

import random
from .color import BLACK, RAINBOW

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"


class Animation:
    """
    Base class for animations.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, pixel_object, speed, color, peers=None, paused=False):
        self.pixel_object = pixel_object
        self._speed_ns = 0
        self.speed = speed  # sets _speed_ns
        self._color = color
        self._next_update = monotonic_ns()
        self.pixel_object.auto_write = False
        self.color = color
        self.peers = peers if peers else []
        self._paused = paused
        self._time_left_at_pause = 0

    def animate(self):
        """
        Call animate() from your code's main loop.  It will draw the animation draw() at intervals
        configured by the speed property (set from init).

        :return: True if the animation draw cycle was triggered, otherwise False.
        """
        if self._paused:
            return False

        now = monotonic_ns()
        if now < self._next_update:
            return False

        self.draw()
        if self.peers:
            for peer in self.peers:
                peer.draw()
        self.show()
        for peer in self.peers:
            peer.show()

        self._next_update = now + self._speed_ns
        return True

    def draw(self):
        """
        Animation subclasses must implement draw() to render the animation sequence.
        """

    def show(self):
        """
        Displays the updated pixels.  Called during animates with changes.
        """
        self.pixel_object.show()

    def freeze(self):
        """
        Stops the animation until resumed.
        """
        self._paused = True
        self._time_left_at_pause = max(0, monotonic_ns() - self._next_update)

    def resume(self):
        """
        Resumes the animation.
        """
        self._next_update = monotonic_ns() + self._time_left_at_pause
        self._time_left_at_pause = 0
        self._paused = False

    def fill(self, color):
        """
        Fills the pixel object with a color.
        """
        self.pixel_object.fill(color)
        self.show()

    @property
    def color(self):
        """
        The current color.
        """
        return self._color

    @color.setter
    def color(self, color):
        if isinstance(color, int):
            color = (color >> 16 & 0xff, color >> 8 & 0xff, color & 0xff)
        self._color = color
        self._recompute_color(color)

    @property
    def speed(self):
        """
        The animation speed in fractional seconds.
        """
        return self._speed_ns / 1000000000

    @speed.setter
    def speed(self, seconds):
        self._speed_ns = int(seconds * 1000000000)

    def _recompute_color(self, color):
        pass

    def change_color(self, color):
        """
        By default changing color uses the color property.
        """
        self.color = color


class ColorCycle(Animation):
    """
    Animate a sequence of one or more colors, cycling at the specified speed.

    :param pixel_object: The initialised LED object.
    :param int speed: Animation speed in seconds, e.g. ``0.1``.
    :param colors: A list of colors to cycle through in ``(r, g, b)`` tuple, or ``0x000000`` hex
                   format. Defaults to a rainbow color cycle.
    """
    def __init__(self, pixel_object, speed, colors=RAINBOW):
        self.colors = colors
        super(ColorCycle, self).__init__(pixel_object, speed, colors[0])
        self._generator = self._color_generator()

    def draw(self):
        next(self._generator)
        self.pixel_object.fill(self.color)
        self.show()

    def _color_generator(self):
        index = 0
        while True:
            self._color = self.colors[index]
            yield
            index = (index + 1) % len(self.colors)

    def change_color(self, color):
        """
        ColorCycle doesn't support change_color.
        """


class Blink(ColorCycle):
    """
    Blink a color on and off.

    :param pixel_object: The initialised LED object.
    :param int speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    """
    def __init__(self, pixel_object, speed, color):
        super(Blink, self).__init__(pixel_object, speed, [color, BLACK])

    def _recompute_color(self, color):
        self.colors = [color, BLACK]

    def change_color(self, color):
        """
        Change the color.
        """
        self.colors[0] = color


class Solid(ColorCycle):
    """
    A solid color.

    :param pixel_object: The initialised LED object.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    """
    def __init__(self, pixel_object, color):
        super(Solid, self).__init__(pixel_object, speed=1, colors=[color])

    def _recompute_color(self, color):
        self.colors = [color]

    def change_color(self, color):
        """
        Change the color.
        """
        self.colors[0] = color


class Comet(Animation):
    """
    A comet animation.

    :param pixel_object: The initialised LED object.
    :param int speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param int tail_length: The length of the comet. Defaults to 10. Cannot exceed the number of
                            pixels present in the pixel object, e.g. if the strip is 30 pixels
                            long, the ``tail_length`` cannot exceed 30 pixels.
    :param bool reverse: Animates the comet in the reverse order. Defaults to ``False``.
    :param bool bounce: Comet will bounce back and forth. Defaults to ``True``.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, pixel_object, speed, color, tail_length=10, reverse=False, bounce=False):
        self._tail_length = tail_length + 1
        self._color_step = 0.9 / tail_length
        self._color_offset = 0.1
        self._comet_colors = None
        self._reverse_comet_colors = None
        self.reverse = reverse
        self.bounce = bounce
        super(Comet, self).__init__(pixel_object, speed, color)
        self._generator = self._comet_generator()

    def _recompute_color(self, color):
        self._comet_colors = [BLACK] + [
            [int(color[rgb] * ((n * self._color_step) + self._color_offset))
             for rgb in range(len(color))
            ] for n in range(self._tail_length - 1)
        ]
        self._reverse_comet_colors = list(reversed(self._comet_colors))

    def _get_range(self, num_pixels):
        if self.reverse:
            return range(num_pixels, -self._tail_length - 1, -1)
        return range(-self._tail_length, num_pixels + 1)

    def _comet_generator(self):
        num_pixels = len(self.pixel_object)
        while True:
            colors = self._reverse_comet_colors if self.reverse else self._comet_colors
            for start in self._get_range(num_pixels):

                if start + self._tail_length < num_pixels:
                    end = self._tail_length
                else:
                    end = num_pixels - start
                if start <= 0:
                    num_visible = self._tail_length + start
                    self.pixel_object[0:num_visible] = colors[self._tail_length - num_visible:]
                else:
                    self.pixel_object[start:start + end] = colors[0:end]
                self.show()
                yield
            if self.bounce:
                self.reverse = not self.reverse

    def draw(self):
        next(self._generator)


class Sparkle(Animation):
    """
    Sparkle animation of a single color.

    :param pixel_object: The initialised LED object.
    :param int speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    """
    def __init__(self, pixel_object, speed, color):
        self._half_color = None
        self._dim_color = None
        super(Sparkle, self).__init__(pixel_object, speed, color)

    def _recompute_color(self, color):
        half_color = tuple(color[rgb] // 4 for rgb in range(len(color)))
        dim_color = tuple(color[rgb] // 10 for rgb in range(len(color)))
        for pixel in range(len(self.pixel_object)):
            if self.pixel_object[pixel] == self._half_color:
                self.pixel_object[pixel] = half_color
            elif self.pixel_object[pixel] == self._dim_color:
                self.pixel_object[pixel] = dim_color
        self._half_color = half_color
        self._dim_color = dim_color

    def draw(self):
        pixel = random.randint(0, (len(self.pixel_object) - 2))
        self.pixel_object[pixel] = self._color
        self.show()
        self.pixel_object[pixel] = self._half_color
        self.pixel_object[pixel + 1] = self._dim_color
        self.show()


class Pulse(Animation):
    """
    Pulse all pixels a single color.

    :param pixel_object: The initialised LED object.
    :param int speed: Animation refresh rate in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param period: Period to pulse the LEDs over.  Default 5.
    :param max_intensity: The maximum intensity to pulse, between 0 and 1.0.  Default 1.
    :param min_intensity: The minimum intensity to pulse, between 0 and 1.0.  Default 0.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, pixel_object, speed, color, period=5, max_intensity=1, min_intensity=0):
        self._intensity = min_intensity
        self.max_intensity = max_intensity
        self.min_intensity = min_intensity
        self._direction = 1.0
        self._intensity_step = 2 / (period / speed)
        self._bpp = len(pixel_object[0])
        super(Pulse, self).__init__(pixel_object, speed, color)

    def draw(self):
        self._intensity += self._intensity_step * self._direction
        if self._direction < 0 and self._intensity <= self.min_intensity:
            self._direction = -self._direction
            self._intensity = self.min_intensity
        elif self._direction > 0 and self._intensity >= self.max_intensity:
            self._direction = -self._direction
            self._intensity = self.max_intensity
        color = [int(self._color[n] * self._intensity) for n in range(self._bpp)]
        self.fill(color)
        self.show()


class AnimationSequence:
    """
    A sequence of Animations to run in sequence, looping forever.
    Advances manually or at the specified interval.

    :param members: The animation objects or groups.
    :param int advance_interval: Time in seconds between animations if cycling
                                 automatically. Defaults to ``None``.

    .. code-block:: python

        from adafruit_led_animation.animation import AnimationSequence, Blink, Comet, Sparkle
        import adafruit_led_animation.color as color
        import board
        import neopixel

        strip_pixels = neopixel.NeoPixel(board.A1, 30, brightness=1, auto_write=False)

        blink = Blink(strip_pixels, 0.2, color.RED)
        comet = Comet(strip_pixels, 0.1, color.BLUE)
        sparkle = Sparkle(strip_pixels, 0.05, color.GREEN)

        animations = AnimationSequence(blink, comet, sparkle, advance_interval=1)

        while True:
            animations.animate()
    """
    def __init__(self, *members, advance_interval=None, auto_clear=False):
        self._members = members
        self._advance_interval = advance_interval * 1000000000 if advance_interval else None
        self._last_advance = monotonic_ns()
        self._current = 0
        self._auto_clear = auto_clear
        self.clear_color = BLACK
        self._paused = False
        self._paused_at = 0

    def _auto_advance(self):
        if not self._advance_interval:
            return
        now = monotonic_ns()
        if now - self._last_advance > self._advance_interval:
            self._last_advance = now
            self.next()

    def next(self):
        """
        Jump to the next animation.
        """
        if self._auto_clear:
            self.fill(self.clear_color)
        self._current = (self._current + 1) % len(self._members)

    def animate(self):
        """
        Call animate() from your code's main loop.  It will draw the current animation
        or go to the next animation based on the advance_interval if set.

        :return: True if the animation draw cycle was triggered, otherwise False.
        """
        if not self._paused:
            self._auto_advance()
        return self.current_animation.animate()

    @property
    def current_animation(self):
        """
        Returns the current animation in the sequence.
        """
        return self._members[self._current]

    def change_color(self, color):
        """
        Change the color of all members that support setting the color with ``change_color``.
        Ignored by animations that do not support it.
        """
        for item in self._members:
            item.change_color(color)

    def fill(self, color):
        """
        Fills the current animation with a color.
        """
        self.current_animation.fill(color)

    def freeze(self):
        """
        Freeze the current animation in the sequence.
        Also stops auto_advance.
        """
        if self._paused:
            return
        self._paused = True
        self._paused_at = monotonic_ns()
        self.current_animation.freeze()

    def resume(self):
        """
        Resume the current animation in the sequence, and resumes auto advance if enabled.
        """
        if not self._paused:
            return
        self._paused = False
        now = monotonic_ns()
        self._last_advance += now - self._paused_at
        self._paused_at = 0
        self.current_animation.resume()


class AnimationGroup:
    """
    A group of animations that are active together. An example would be grouping a strip of
    pixels connected to a board and the onboard LED.

    :param members: The animation objects or groups.
    :param bool sync: Synchronises the timing of all members of the group to the settings of the
                      first member of the group. Defaults to ``False``.

    """
    def __init__(self, *members, sync=False):
        self._members = members
        self._sync = sync
        if sync:
            main = members[0]
            main.peers = members[1:]

    def animate(self):
        """
        Call animate() from your code's main loop.  It will draw all of the animations
        in the group.

        :return: True if any animation draw cycle was triggered, otherwise False.
        """
        if self._sync:
            return self._members[0].animate()

        return any([item.animate() for item in self._members])

    def _for_all(self, method, *args, **kwargs):
        for item in self._members:
            getattr(item, method)(*args, **kwargs)

    def change_color(self, color):
        """
        Change the color of all members that support setting the color with change_color.
        Ignored by animations that do not support it.
        """
        self._for_all('change_color', color)

    def fill(self, color):
        """
        Fills all pixel objects in the group with a color.
        """
        self._for_all('fill', color)

    def freeze(self):
        """
        Freeze all animations in the group.
        """
        self._for_all('freeze')

    def resume(self):
        """
        Resume all animations in the group.
        """
        self._for_all('resume')
