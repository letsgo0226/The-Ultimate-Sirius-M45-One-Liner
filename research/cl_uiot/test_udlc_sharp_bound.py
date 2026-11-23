import itertools
import unittest


class SharpBoundTests(unittest.TestCase):
    def test_sharp_point_bound(self):
        for d in range(4):
            for ks in itertools.product(range(-2, 3), repeat=5):
                x = d
                prefix = [0]
                for k in ks:
                    x = max(0, x + k)
                    prefix.append(prefix[-1] + k)
                    sharp = max(d + prefix[-1], max(prefix[-1] - s for s in prefix))
                    self.assertEqual(x, sharp)
                    for B in (sharp - 1, sharp, sharp + 1):
                        self.assertEqual(x <= B, d + prefix[-1] <= B and all(prefix[-1] - s <= B for s in prefix))


if __name__ == '__main__':
    unittest.main()
