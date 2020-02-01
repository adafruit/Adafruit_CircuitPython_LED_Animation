"""
Adafruit LED Animation library.
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
