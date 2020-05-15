from time import monotonic_ns

from adafruit_led_animation import NANOS_PER_SECOND
from adafruit_led_animation.animation import Animation, Chase, Comet
from adafruit_led_animation.color import BLACK, colorwheel


class Rainbow(Animation):
    """
    The classic rainbow color wheel.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation refresh rate in seconds, e.g. ``0.1``.
    :param period: Period to cycle the rainbow over.  Default 5.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, pixel_object, speed, period=5, name=None):
        super().__init__(pixel_object, speed, BLACK, name=name)
        self._period = period
        self._generator = self._color_wheel_generator()

    cycle_complete_supported = True

    def _color_wheel_generator(self):
        period = int(self._period * NANOS_PER_SECOND)

        last_update = monotonic_ns()
        cycle_position = 0
        last_pos = 0
        while True:
            cycle_completed = False
            now = monotonic_ns()
            time_since_last_draw = now - last_update
            last_update = now
            pos = cycle_position = (cycle_position + time_since_last_draw) % period
            if pos < last_pos:
                cycle_completed = True
            last_pos = pos
            wheel_index = int((pos / period) * 256)
            self.pixel_object[:] = [
                colorwheel((i + wheel_index) % 255)
                for i, _ in enumerate(self.pixel_object)
            ]
            self.show()
            if cycle_completed:
                self.cycle_complete()
            yield

    def draw(self):
        next(self._generator)

    def reset(self):
        """
        Resets the animation.
        """
        self._generator = self._color_wheel_generator()


class RainbowChase(Chase):
    """
    Chase pixels in one direction, like a theater marquee but with rainbows!

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed rate in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param size: Number of pixels to turn on in a row.
    :param spacing: Number of pixels to turn off in a row.
    :param reverse: Reverse direction of movement.
    :param wheel_step: How many colors to skip in `colorwheel` per bar (default 8)
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        size=2,
        spacing=3,
        reverse=False,
        name=None,
        wheel_step=8,
    ):
        self._num_colors = 256 // wheel_step
        self._colors = [colorwheel(n % 256) for n in range(0, 512, wheel_step)]
        self._color_idx = 0
        super().__init__(pixel_object, speed, 0, size, spacing, reverse, name)

    def bar_color(self, n, pixel_no=0):
        return self._colors[self._color_idx - n]

    def cycle_complete(self):
        self._color_idx = (self._color_idx + self._direction) % len(self._colors)
        super().cycle_complete()


class RainbowComet(Comet):
    """
    A rainbow comet animation.

    :param pixel_object: The initialised LED object.
    :param float speed: Animation speed in seconds, e.g. ``0.1``.
    :param color: Animation color in ``(r, g, b)`` tuple, or ``0x000000`` hex format.
    :param int tail_length: The length of the comet. Defaults to 10. Cannot exceed the number of
                            pixels present in the pixel object, e.g. if the strip is 30 pixels
                            long, the ``tail_length`` cannot exceed 30 pixels.
    :param bool reverse: Animates the comet in the reverse order. Defaults to ``False``.
    :param bool bounce: Comet will bounce back and forth. Defaults to ``True``.
    :param int colorwheel_offset: Offset from start of colorwheel (0-255).
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        pixel_object,
        speed,
        tail_length=10,
        reverse=False,
        bounce=False,
        colorwheel_offset=0,
        name=None,
    ):
        self._colorwheel_is_tuple = isinstance(colorwheel(0), tuple)
        self._colorwheel_offset = colorwheel_offset

        super().__init__(pixel_object, speed, 0, tail_length, reverse, bounce, name)

    def _calc_brightness(self, n, color):
        brightness = (n * self._color_step) + self._color_offset
        if not self._colorwheel_is_tuple:
            color = (color & 0xFF, ((color & 0xFF00) >> 8), (color >> 16))
        return [int(i * brightness) for i in color]

    def __recompute_color(self, color):
        factor = int(256 / self._tail_length)
        self._comet_colors = [BLACK] + [
            self._calc_brightness(
                n,
                colorwheel(
                    int((n * factor) + self._color_offset + self._colorwheel_offset)
                    % 256
                ),
            )
            for n in range(self._tail_length - 1)
        ]
        self._reverse_comet_colors = list(reversed(self._comet_colors))
        self._computed_color = color
