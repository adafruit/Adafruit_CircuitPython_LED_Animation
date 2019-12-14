"""
Adafruit LED Animation library.
"""

try:
    from micropython import const
except ImportError:
    def const(value):  # pylint: disable=missing-docstring
        return value

NANOS_PER_SECOND = const(1000000000)
NANOS_PER_MS = const(1000000)
