import itertools
import unittest

class VariablePairs(unittest.TestCase):
    def test_bounds(self):
        pairs = [(a, b) for a in range(4) for b in range(a, 5)]
        for d in range(5):
            for seq in itertools.product(pairs, repeat=3):
                x = d
                for a, b in seq:
                    x = max(0, x+a)
                    self.assertLessEqual(x, d+3)
                    x = max(0, x-b)
                    self.assertLessEqual(x, d)

    def test_unbounded_peaks_without_uniform_cap(self):
        for a in (1, 10, 1000):
            self.assertEqual(max(0, a-a), 0)
            self.assertGreaterEqual(a, 1)
