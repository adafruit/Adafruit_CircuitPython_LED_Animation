"""
Helper classes for making complex animations.
"""
import math


class AggregatePixels:
    """
    AggregatePixels lets you treat ranges of pixels as single pixels for animation purposes.

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param iterable pixel_ranges: Pixel ranges (or individual pixels).
    :param bool individual_pixels: Whether pixel_ranges are individual pixels.

    .. code-block:: python

        import board
        import neopixel
        from adafruit_led_animation.helper import AggregatePixels
        pixels = neopixel.NeoPixel(board.D12, 307, auto_write=False)

        tree = AggregatePixels(pixels, [
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
        :param color: Color to fill all pixels referenced by this AggregatePixels definition with.
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


class SubsetPixels:
    """
    SubsetPixels lets you work with a subset of a pixel object.

    :param strip: An object that implements the Neopixel or Dotstar protocol.
    :param int start: Starting pixel number.
    :param int end: Ending pixel number.

    .. code-block:: python

        import board
        import neopixel
        from adafruit_led_animation.helper import SubsetPixels
        pixels = neopixel.NeoPixel(board.D12, 307, auto_write=False)

        star_start = 260
        star_arm = SubsetPixels(pixels, star_start + 7, star_start + 15)
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
            self._pixels[start + self._start:stop + self._start:step] = val
        else:
            self._pixels[index + self._start] = val

        if self._pixels.auto_write:
            self.show()

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self.n)
            return self._pixels[start + self._start:stop + self._start:step]
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
        self._pixels[self._start:self._end] = [color] * (self.n)

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
