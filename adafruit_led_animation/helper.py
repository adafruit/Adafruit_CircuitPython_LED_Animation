"""
Helper classes for making complex animations.
"""
import math


class AggregatePixels:
    """
    AggregatePixels lets you treat ranges of pixels as single pixels for animation purposes.
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
