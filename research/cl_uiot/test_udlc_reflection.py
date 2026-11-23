import itertools
import unittest


class ReflectionTests(unittest.TestCase):
    def test_running_minimum_identity(self):
        for d in range(4):
            for increments in itertools.product(range(-2, 3), repeat=5):
                damage, prefix, floor = d, 0, -d
                self.assertEqual(damage, prefix - floor)
                for k in increments:
                    damage = max(0, damage + k)
                    prefix += k
                    floor = min(floor, prefix)
                    self.assertEqual(damage, prefix - floor)


if __name__ == '__main__':
    unittest.main()
