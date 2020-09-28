from adafruit_led_animation.animation import Animation

class Volume(Animation):
    """
    Animate the brightness and number of pixels based on volume.
    :param pixel_object: The initialised LED object.
    :param float speed: Animation update speed in seconds, e.g. ``0.1``.
    :param brightest_color: Color at max volume ``(r, g, b)`` tuple, or ``0x000000`` hex format
    """

    def __init__(self, pixel_object, speed, brightest_color, decoder, max_volume=500, name=None):
        self._decoder = decoder
        self._num_pixels = len(pixel_object)
        self._max_volume = max_volume
        self._brigthest_color = brightest_color
        super().__init__(pixel_object, speed, brightest_color, name=name)

    def _set_color(self, brightest_color):
        self.colors = [brightest_color]

    def map_range(self, x, in_min, in_max, out_min, out_max):
        mapped = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if out_min <= out_max:
            return max(min(mapped, out_max), out_min)

        return min(max(mapped, out_max), out_min)

    def draw(self):
        red = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._brigthest_color[0]))
        green = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._brigthest_color[1]))
        blue = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._brigthest_color[2]))

        lit_pixels = int(self.map_range(self._decoder.rms_level, 0, self._max_volume, 0, self._num_pixels))
        if lit_pixels > self._num_pixels:
            lit_pixels = self._num_pixels

        self.pixel_object[0:lit_pixels] = [(red,green,blue)] * lit_pixels
        self.pixel_object[lit_pixels:self._num_pixels] = [(0,0,0)] * (self._num_pixels-lit_pixels)
