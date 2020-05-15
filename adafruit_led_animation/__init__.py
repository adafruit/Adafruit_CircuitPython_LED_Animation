# The MIT License (MIT)
#
# Copyright (c) 2020 Roy Hooper
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
Timing for Adafruit LED Animation library.

Author(s): Roy Hooper
"""

try:
    from micropython import const
except ImportError:

    def const(value):  # pylint: disable=missing-docstring
        return value


try:
    from time import monotonic_ns
except ImportError:
    import time

    def monotonic_ns():
        """
        Implementation of monotonic_ns for platforms without time.monotonic_ns
        """
        return int(time.time() * NANOS_PER_SECOND)


NANOS_PER_SECOND = const(1000000000)
NANOS_PER_MS = const(1000000)
