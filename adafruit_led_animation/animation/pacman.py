# SPDX-FileCopyrightText: 2025 Bob Loeffler
# SPDX-FileCopyrightText: 2025 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

"""
`adafruit_led_animation.animation.pacman`
================================================================================

PacMan Animation for CircuitPython helper library for LED animations.
PACMAN ANIMATION Adapted from https://github.com/wled-dev/WLED/pull/4536 # by BobLoeffler68

* Author(s): Bob Loeffler, Jose D. Montoya

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


"""

import time

from adafruit_led_animation.animation import Animation
from adafruit_led_animation.color import (
    BLACK,
    BLUE,
    CYAN,
    ORANGE,
    PURPLE,
    RED,
    WHITE,
    YELLOW,
)

ORANGEYELLOW = (255, 136, 0)


class Pacman(Animation):
    """
    Simulate the Pacman game in a single led strip.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed rate in seconds, e.g. ``0.1``.
    """

    def __init__(
        self,
        pixel_object,
        speed,
        color=WHITE,
        name=None,
    ):
        self.num_leds = len(pixel_object)
        self.pacman = [YELLOW, 10]
        self.ghosts_original = [[RED, 6], [PURPLE, 4], [CYAN, 2], [ORANGE, 0]]
        self.ghosts = [[RED, 6], [PURPLE, 4], [CYAN, 2], [ORANGE, 0]]
        self.direction = 1
        self.black_dir = -1
        self.flag = "beep"
        self.power_pellet = [ORANGEYELLOW, self.num_leds]
        self.ghost_timer = time.monotonic()
        if self.num_leds > 150:
            self.start_blinking_ghosts = self.num_leds // 4
        else:
            self.start_blinking_ghosts = self.num_leds // 3

        super().__init__(pixel_object, speed, color, name=name)

    on_cycle_complete_supported = True

    def draw(self):
        """
        Draw the Pacman animation.
        :param led_object: led object
        :param neopixel_list: list of neopixel colors
        :param int num_leds: number of leds.
        :param int duration: duration in seconds. Default is 15 seconds
        """
        pixel_list = self.pixel_object
        pixel_list[-1] = self.power_pellet[0]

        delta = time.monotonic() - self.ghost_timer
        if delta > 1:
            if self.power_pellet[0] == ORANGEYELLOW:
                self.power_pellet[0] = BLACK
            else:
                self.power_pellet[0] = ORANGEYELLOW
            pixel_list[self.power_pellet[1] - 1] = self.power_pellet[0]

            self.ghost_timer = time.monotonic()

        if self.pacman[1] >= self.num_leds - 2:
            self.direction = self.direction * -1
            self.black_dir = self.black_dir * -1
            for ghost in self.ghosts:
                ghost[0] = BLUE

        pixel_list[self.pacman[1]] = self.pacman[0]
        pixel_list[self.pacman[1] + self.black_dir] = BLACK
        self.pacman[1] += self.direction

        if self.ghosts[3][1] <= self.start_blinking_ghosts and self.direction == -1:
            if self.flag == "beep":
                for i, ghost in enumerate(self.ghosts):
                    ghost[0] = BLACK
                self.flag = "bop"
            else:
                for i, ghost in enumerate(self.ghosts):
                    ghost[0] = self.ghosts_original[i][0]
                self.flag = "beep"

        for i, ghost in enumerate(self.ghosts):
            pixel_list[ghost[1]] = ghost[0]
            pixel_list[ghost[1] + self.black_dir] = BLACK
            ghost[1] += self.direction

        if self.ghosts[3][1] <= 0:
            self.direction = self.direction * -1
            self.black_dir = self.black_dir * -1
            for i, ghost in enumerate(self.ghosts):
                ghost[0] = self.ghosts_original[i][0]
