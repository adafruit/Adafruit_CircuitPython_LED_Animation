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
`adafruit_led_animation.group`
================================================================================

Animation group helper for CircuitPython helper library for LED animations..


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

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation.git"


class AnimationGroup:
    """
    A group of animations that are active together. An example would be grouping a strip of
    pixels connected to a board and the onboard LED.

    :param members: The animation objects or groups.
    :param bool sync: Synchronises the timing of all members of the group to the settings of the
                      first member of the group. Defaults to ``False``.

    """

    def __init__(self, *members, sync=False, name=None):
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
        self.name = name
        if sync:
            main = members[0]
            main.peers = members[1:]

        # Catch cycle_complete on the last animation.
        self._members[-1].add_cycle_complete_receiver(self._group_done)
        self.cycle_complete_supported = self._members[-1].cycle_complete_supported

    def __str__(self):
        return "<AnimationGroup %s: %s>" % (self.__class__.__name__, self.name)

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

    def show(self):
        """
        Draws the current animation group members.
        """
        for item in self._members:
            item.show()
