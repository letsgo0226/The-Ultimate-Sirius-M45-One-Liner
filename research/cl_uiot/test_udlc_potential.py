import itertools
import unittest


class PotentialBound(unittest.TestCase):
    def test_bounded_potential(self):
        for p in itertools.product(range(4), repeat=4):
            for d in range(p[0] + 1):
                for slack in itertools.product(range(3), repeat=3):
                    x = d
                    for j, s in enumerate(slack):
                        k = p[j+1] - p[j] - s
                        x = max(0, x+k)
                        self.assertLessEqual(x, p[j+1])
                        self.assertLessEqual(x, max(p))

    def test_positive_steps_allowed(self):
        x = 0
        for _ in range(20):
            x = max(0, x+3)
            self.assertEqual(x, 3)
            x = max(0, x-3)
            self.assertEqual(x, 0)
