"""Fire animation, by Uck!"""

if __name__ != '__main__':
    # See unit tests below.  dcfurs doesn't exist when running locally.
    import dcfurs
import random

# Colors, from top to bottom (fire goes from blue on bottom to yellow to red
# to black).
colors = [0, 0x1f0f0f, 0x3f0000, 0xff0000, 0xff7f00, 0xffff00, 0x1f007f,
          0x0000ff]

class fire(object):
    """A simple fire animation, inspired by the classic demo fire effect."""

    def __init__(self):
        # Allocate our internal buffer.  Values in this buffer range from 0
        # to len(colors) - 1.  As the fire values move upward on the screen,
        # these values fall toward 0 (which is black, in the colors array).
        #
        # There's an extra row at the bottom that's filled with random values.
        # That row isn't displayed on the LEDs.
        self.buffer = [[0] * dcfurs.ncols for y in range(dcfurs.nrows + 1)]
        self.interval = 25

    def draw(self):
        self.update()

        for y in range(dcfurs.nrows):
            for x in range(dcfurs.ncols):
                dcfurs.set_pix_rgb(x, y, colors[self.buffer[y][x]])

    def update(self):
        # Fill the bottom (invisible) row with random values.
        for x in range(dcfurs.ncols):
            self.buffer[dcfurs.nrows][x] = random.randint(0, len(colors) - 1)

        # Propagate the fire colors upward, averaging from the pixels below
        # and decreasing the value toward 0.
        for y in range(dcfurs.nrows):
            for x in range(1, dcfurs.ncols - 1):
                value = (self.buffer[y + 1][x - 1] +
                         self.buffer[y + 1][x] +
                         self.buffer[y + 1][x + 1]) // 3
                if random.randint(0, 2) == 0:
                    value -= 1
                self.buffer[y][x] = min(len(colors) - 1, max(0, value))


# Simple unit test to verify that everything should run without
# crashing.  When run locally, there's no dcfurs module, so this
# creates a fake one with the functions used by the animation.
# Note that this isn't perfect, since the environment when running
# on the badge is a bit different (eg. functions like xrange don't
# exist, and the firmware provides a number of objects that don't
# exist here), but it can at least cover some of the basics.
if __name__ == '__main__':
    import unittest

    class FakeDcfurs(object):
        nrows = 7
        ncols = 18
        def set_row(self, row, color):
            pass
        def set_pix_rgb(self, x, y, color):
            pass
        def clear(self):
            pass
    dcfurs = FakeDcfurs()

    class TestPattern(unittest.TestCase):
        def setUp(self):
            self.pattern = fire()

        def test_interface(self):
            self.assertTrue(hasattr(self.pattern, 'interval'))
            self.assertTrue(hasattr(self.pattern, 'draw'))
            self.pattern.draw()
    unittest.main()
