if __name__ != '__main__':
    import dcfurs
import random

colors = [0, 0x1f0f0f, 0x3f0000, 0xff0000, 0xff7f00, 0xffff00, 0x1f007f,
          0x0000ff]

class fire(object):
    def __init__(self):
        self.buffer = [[0] * dcfurs.ncols for y in range(dcfurs.nrows + 1)]
        self.interval = 25
        self.counter = 0

    def draw(self):
        self.update()
        self.counter += 1

        for y in range(dcfurs.nrows):
            for x in range(dcfurs.ncols):
                dcfurs.set_pix_rgb(x, y, colors[self.buffer[y][x]])

    def update(self):
        for x in range(dcfurs.ncols):
            self.buffer[dcfurs.nrows][x] = random.randint(0, len(colors) - 1)
        for y in range(dcfurs.nrows):
            for x in range(1, dcfurs.ncols - 1):
                value = (self.buffer[y + 1][x - 1] +
                         self.buffer[y + 1][x] +
                         self.buffer[y + 1][x + 1]) // 3
                if random.randint(0, 2) == 0:
                    value -= 1
                self.buffer[y][x] = min(len(colors) - 1, max(0, value))
                #print 'x(%d) y(%d) value: %r' % (x, y, self.buffer[y][x])

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
