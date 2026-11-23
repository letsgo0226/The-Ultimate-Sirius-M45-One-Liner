import itertools
import unittest


class PrefixRange(unittest.TestCase):
    def test_prefix_range(self):
        for ks in itertools.product(range(-2, 3), repeat=5):
            prefixes = [0]
            for k in ks:
                prefixes.append(prefixes[-1] + k)
            for d in range(4):
                x = d
                bound = d + max(prefixes) - min(prefixes)
                for k in ks:
                    x = max(0, x+k)
                    self.assertLessEqual(x, bound)

    def test_nonpositive_prefix_not_sufficient(self):
        for a in range(1, 21):
            ks = [-a, a]
            x = 0
            for k in ks:
                x = max(0, x+k)
            self.assertEqual(sum(ks), 0)
            self.assertEqual(x, a)
