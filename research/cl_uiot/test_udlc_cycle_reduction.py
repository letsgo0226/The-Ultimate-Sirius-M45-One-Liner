import itertools
import unittest


class CycleReduction(unittest.TestCase):
    def test_signed_second_step_reduction(self):
        for d in range(4):
            for seq in itertools.product(list(itertools.product(range(3), range(-4, 3))), repeat=3):
                x = y = d
                for a, z in seq:
                    x = max(0, max(0, x + a) + z)
                    y = max(0, y + a + z)
                    self.assertEqual(x, y)

    def test_strict_cycle_recovery(self):
        for d in range(10):
            x = d
            for n in range(d):
                a = n % 4
                x = max(0, max(0, x + a) - a - 1 - n % 2)
            self.assertEqual(x, 0)
