# The MIT License (MIT)
#
# Copyright (c) 2019 Roy Hooper
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
`adafruit_led_animation.helper`
================================================================================

Helper classes for making complex animations using LED Animation library.


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

import math
import random
from . import NANOS_PER_SECOND, monotonic_ns
from .color import BLACK


class PixelMap:
    """
    PixelMap lets you treat ranges of pixels as single pixels for animation purposes.

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param iterable pixel_ranges: Pixel ranges (or individual pixels).
    :param bool individual_pixels: Whether pixel_ranges are individual pixels.

    .. code-block:: python

        import board
        import neopixel
        from adafruit_led_animation.helper import PixelMap
        pixels = neopixel.NeoPixel(board.D12, 307, auto_write=False)

        tree = PixelMap(pixels, [
            (0, 21), (21, 48), (48, 71), (71, 93),(93, 115), (115, 135), (135, 153),
            (153, 170), (170, 188), (188, 203), (203, 217), (217, 228), (228, 240),
            (240, 247), (247, 253), (253, 256), (256, 260), (260, 307)]
        )
        tree[0] = (255, 255, 0)
        tree.show()

    """

    def __init__(self, strip, pixel_ranges, individual_pixels=False):
        self._pixels = strip
        self._ranges = pixel_ranges
        self.n = len(self._ranges)
        self._individual_pixels = individual_pixels

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def _set_pixels(self, index, val):
        if self._individual_pixels:
            for pixel in self._ranges[index]:
                self._pixels[pixel] = val
        else:
            range_start, range_stop = self._ranges[index]
            self._pixels[range_start:range_stop] = [val] * (range_stop - range_start)

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self._ranges))
            length = stop - start
            if step != 0:
                length = math.ceil(length / step)
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_pixels(in_i, val[val_i])
        else:
            self._set_pixels(index, val)

        if self._pixels.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            out = []
            for in_i in range(*index.indices(len(self._ranges))):
                out.append(self._pixels[self._ranges[in_i][0]])
            return out
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        return self._pixels[self._ranges[index][0]]

    def __len__(self):
        return len(self._ranges)

    @property
    def brightness(self):
        """
        brightness from the underlying strip.
        """
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, brightness):
        # pylint: disable=attribute-defined-outside-init
        self._pixels.brightness = min(max(brightness, 0.0), 1.0)

    def fill(self, color):
        """
        Fill the used pixel ranges with color.
        :param color: Color to fill all pixels referenced by this PixelMap definition with.
        """
        if self._individual_pixels:
            for pixels in self._ranges:
                for pixel in pixels:
                    self._pixels[pixel] = color
        else:
            for start, stop in self._ranges:
                self._pixels[start:stop] = [color] * (stop - start)

    def show(self):
        """
        Shows the pixels on the underlying strip.
        """
        self._pixels.show()

    @property
    def auto_write(self):
        """
        auto_write from the underlying strip.
        """
        return self._pixels.auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._pixels.auto_write = value


class PixelSubset:
    """
    PixelSubset lets you work with a subset of a pixel object.

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param int start: Starting pixel number.
    :param int end: Ending pixel number.

    .. code-block:: python

        import board
        import neopixel
        from adafruit_led_animation.helper import PixelSubset
        pixels = neopixel.NeoPixel(board.D12, 307, auto_write=False)

        star_start = 260
        star_arm = PixelSubset(pixels, star_start + 7, star_start + 15)
        star_arm.fill((255, 0, 255))
        pixels.show()
    """

    def __init__(self, strip, start, end):
        self._pixels = strip
        self._start = start
        self._end = end
        self.n = self._end - self._start

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self.n)
            self._pixels[start + self._start : stop + self._start : step] = val
        else:
            self._pixels[index + self._start] = val

        if self._pixels.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self.n)
            return self._pixels[start + self._start : stop + self._start : step]
        if index < 0:
            index += len(self)
        if index >= self.n or index < 0:
            raise IndexError
        return self._pixels[index]

    def __len__(self):
        return self.n

    @property
    def brightness(self):
        """
        brightness from the underlying strip.
        """
        return self._pixels.brightness

    @brightness.setter
    def brightness(self, brightness):
        self._pixels.brightness = min(max(brightness, 0.0), 1.0)

    def fill(self, color):
        """
        Fill the used pixel ranges with color.
        """
        self._pixels[self._start : self._end] = [color] * (self.n)

    def show(self):
        """
        Shows the pixels on the underlying strip.
        """
        self._pixels.show()

    @property
    def auto_write(self):
        """
        auto_write from the underlying strip.
        """
        return self._pixels.auto_write

    @auto_write.setter
    def auto_write(self, value):
        self._pixels.auto_write = value


def pulse_generator(period: float, animation_object, white=False):
    """
    Generates a sequence of colors for a pulse, based on the time period specified.
    :param period: Pulse duration in seconds.
    :param animation_object: An animation object to interact with.
    :param white: Whether the pixel strip has a white pixel.
    """
    period = int(period * NANOS_PER_SECOND)
    half_period = period // 2

    last_update = monotonic_ns()
    cycle_position = 0
    last_pos = 0
    while True:
        fill_color = list(animation_object.color)
        now = monotonic_ns()
        time_since_last_draw = now - last_update
        last_update = now
        pos = cycle_position = (cycle_position + time_since_last_draw) % period
        if pos < last_pos:
            animation_object.cycle_complete()
        last_pos = pos
        if pos > half_period:
            pos = period - pos
        intensity = pos / half_period
        if white:
            fill_color[3] = int(fill_color[3] * intensity)
        fill_color[0] = int(fill_color[0] * intensity)
        fill_color[1] = int(fill_color[1] * intensity)
        fill_color[2] = int(fill_color[2] * intensity)
        yield fill_color


class AnimationGroup:
    """
    A group of animations that are active together. An example would be grouping a strip of
    pixels connected to a board and the onboard LED.

    :param members: The animation objects or groups.
    :param bool sync: Synchronises the timing of all members of the group to the settings of the
                      first member of the group. Defaults to ``False``.

    """

    def __init__(self, *members, sync=False):
        if not members:
            raise ValueError("At least one member required in an AnimationGroup")
        self.draw_count = 0
        """Number of animation frames drawn."""
        self.cycle_count = 0
        """Number of animation cycles completed."""
        self.notify_cycles = 1
        """Number of cycles to trigger additional cycle_done notifications after"""
        self._members = list(members)
        self._sync = sync
        self._also_notify = []
        self.cycle_count = 0
        if sync:
            main = members[0]
            main.peers = members[1:]

        # Catch cycle_complete on the last animation.
        self._members[-1].add_cycle_complete_receiver(self._group_done)
        self.cycle_complete_supported = self._members[-1].cycle_complete_supported

    def _group_done(self, animation):  # pylint: disable=unused-argument
        self.cycle_complete()

    def cycle_complete(self):
        """
        Called by some animations when they complete an animation cycle.
        Animations that support cycle complete notifications will have X property set to False.
        Override as needed.
        """
        self.cycle_count += 1
        if self.cycle_count % self.notify_cycles == 0:
            for callback in self._also_notify:
                callback(self)

    def add_cycle_complete_receiver(self, callback):
        """
        Adds an additional callback when the cycle completes.
        :param callback: Additional callback to trigger when a cycle completes.  The callback
                         is passed the animation object instance.
        """
        self._also_notify.append(callback)

    def animate(self):
        """
        Call animate() from your code's main loop.  It will draw all of the animations
        in the group.

        :return: True if any animation draw cycle was triggered, otherwise False.
        """
        if self._sync:
            return self._members[0].animate()

        return any([item.animate() for item in self._members])

    @property
    def color(self):
        """
        Use this property to change the color of all members of the animation group.
        """
        return None

    @color.setter
    def color(self, color):
        for item in self._members:
            item.color = color

    def fill(self, color):
        """
        Fills all pixel objects in the group with a color.
        """
        for item in self._members:
            item.fill(color)

    def freeze(self):
        """
        Freeze all animations in the group.
        """
        for item in self._members:
            item.freeze()

    def resume(self):
        """
        Resume all animations in the group.
        """
        for item in self._members:
            item.resume()

    def reset(self):
        """
        Resets the animations in the group.
        """
        for item in self._members:
            item.reset()


class AnimationSequence:
    """
    A sequence of Animations to run in succession, looping forever.
    Advances manually, or at the specified interval.

    :param members: The animation objects or groups.
    :param int advance_interval: Time in seconds between animations if cycling
                                 automatically. Defaults to ``None``.
    :param bool auto_clear: Clear the pixels between animations. If ``True``, the current animation
                            will be cleared from the pixels before the next one starts.
                            Defaults to ``False``.
    :param bool random_order: Activate the animations in a random order. Defaults to ``False``.
    :param bool auto_reset: Automatically call reset() on animations when changing animations.
    :param bool advance_on_cycle_complete: Automatically advance when `cycle_complete` is triggered
                                           on member animations. All Animations must support
                                           cycle_complete to use this.
    .. code-block:: python

        import board
        import neopixel
        from adafruit_led_animation.animation import AnimationSequence, Blink, Comet, Sparkle
        import adafruit_led_animation.color as color

        strip_pixels = neopixel.NeoPixel(board.A1, 30, brightness=1, auto_write=False)

        blink = Blink(strip_pixels, 0.2, color.RED)
        comet = Comet(strip_pixels, 0.1, color.BLUE)
        sparkle = Sparkle(strip_pixels, 0.05, color.GREEN)

        animations = AnimationSequence(blink, comet, sparkle, advance_interval=1)

        while True:
            animations.animate()
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, *members, advance_interval=None, auto_clear=False, random_order=False,
                 auto_reset=False, advance_on_cycle_complete=False):
        self._members = members
        self._advance_interval = (
            advance_interval * NANOS_PER_SECOND if advance_interval else None
        )
        self._last_advance = monotonic_ns()
        self._current = 0
        self.auto_clear = auto_clear
        self.auto_reset = auto_reset
        self.advance_on_cycle_complete = advance_on_cycle_complete
        self.clear_color = BLACK
        self._paused = False
        self._paused_at = 0
        self._random = random_order
        self._also_notify = []
        self.cycle_count = 0
        self.notify_cycles = 1
        if random_order:
            self._current = random.randint(0, len(self._members) - 1)
        self._color = None
        for member in self._members:
            member.add_cycle_complete_receiver(self._sequence_complete)
        self.cycle_complete_supported = self._members[-1].cycle_complete_supported

    cycle_complete_supported = True

    def cycle_complete(self):
        """
        Called by some animations when they complete an animation cycle.
        Animations that support cycle complete notifications will have X property set to False.
        Override as needed.
        """
        self.cycle_count += 1
        if self.cycle_count % self.notify_cycles == 0:
            for callback in self._also_notify:
                callback(self)

    def _sequence_complete(self, animation):  # pylint: disable=unused-argument
        self.cycle_complete()
        if self.advance_on_cycle_complete:
            self._advance()

    def add_cycle_complete_receiver(self, callback):
        """
        Adds an additional callback when the cycle completes.
        :param callback: Additional callback to trigger when a cycle completes.  The callback
                         is passed the animation object instance.
        """
        self._also_notify.append(callback)

    def _auto_advance(self):
        if not self._advance_interval:
            return
        now = monotonic_ns()
        if now - self._last_advance > self._advance_interval:
            self._last_advance = now
            self._advance()

    def _advance(self):
        if self._random:
            self.random()
        else:
            self.next()

    def activate(self, index):
        """
        Activates a specific animation.
        """
        if isinstance(index, str):
            self._current = [member.name for member in self._members].index(index)
        else:
            self._current = index
        if self.auto_clear:
            self.fill(self.clear_color)
        if self._color:
            self.current_animation.color = self._color

    def next(self):
        """
        Jump to the next animation.
        """
        current = self._current
        self.activate((self._current + 1) % len(self._members))
        if self.auto_reset:
            self.current_animation.reset()
        if current > self._current:
            self.cycle_complete()

    def random(self):
        """
        Jump to a random animation.
        """
        self.activate(random.randint(0, len(self._members) - 1))

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

    @property
    def color(self):
        """
        Use this property to change the color of all animations in the sequence.
        """
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.current_animation.color = color

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

    def reset(self):
        """
        Resets the current animation.
        """
        self.current_animation.reset()
