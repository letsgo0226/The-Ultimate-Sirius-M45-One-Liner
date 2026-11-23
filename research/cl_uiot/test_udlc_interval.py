import itertools
import unittest


class IntervalExcursion(unittest.TestCase):
    def test_interval_bounds(self):
        for ks in itertools.product(range(-2, 3), repeat=5):
            s = [0]
            for k in ks:
                s.append(s[-1] + k)
            B = max(s[j]-s[i] for j in range(len(s)) for i in range(j+1))
            for d in range(4):
                x = d
                for j in range(len(s)):
                    if j:
                        x = max(0, x+ks[j-1])
                    self.assertLessEqual(x, d+B)
                    for i in range(j+1):
                        self.assertLessEqual(s[j]-s[i], x)

    def test_negative_drift(self):
        x = 0
        for _ in range(100):
            x = max(0, x-3)
            x = max(0, x+2)
            self.assertEqual(x, 2)
