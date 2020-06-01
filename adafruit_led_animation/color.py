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
"""Color variables made available for import for CircuitPython LED animations library.

RAINBOW is a list of colors to use for cycling through.
"""
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GOLD = (255, 222, 30)
PINK = (242, 90, 255)
AQUA = (50, 255, 255)
JADE = (0, 255, 40)
AMBER = (255, 100, 0)

RAINBOW = (RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)


try:
    try:
        # Backwards compat for 5.3.0 and prior
        from _pixelbuf import colorwheel  # pylint: disable=unused-import
    except ImportError:
        from _pixelbuf import wheel as colorwheel  # pylint: disable=unused-import
except ImportError:
    # Ensure we have a wheel if not built in
    def colorwheel(pos):
        """Input a value 0 to 255 to get a color value.
        The colours are a transition r - g - b - back to r."""
        if pos < 0 or pos > 255:
            return 0, 0, 0
        if pos < 85:
            return int(255 - pos * 3), int(pos * 3), 0
        if pos < 170:
            pos -= 85
            return 0, int(255 - pos * 3), int(pos * 3)
        pos -= 170
        return int(pos * 3), 0, int(255 - (pos * 3))


def calculate_intensity(color, intensity=1.0):
    """
    Takes a RGB[W] color tuple and adjusts the intensity.
    :param float intensity:
    :param color: color value (tuple, list or int)
    :return: color
    """
    # Note: This code intentionally avoids list comprehensions and intermediate variables
    # for an approximately 2x performance gain.
    if isinstance(color, int):
        return (
            (int((color & 0xFF0000) * intensity) & 0xFF0000)
            | (int((color & 0xFF00) * intensity) & 0xFF00)
            | (int((color & 0xFF) * intensity) & 0xFF)
        )

    if len(color) == 3:
        return (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity),
        )
    if len(color) == 4 and isinstance(color[3], float):
        return (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity),
            color[3],
        )
    return (
        int(color[0] * intensity),
        int(color[1] * intensity),
        int(color[2] * intensity),
        int(color[3] * intensity),
    )
