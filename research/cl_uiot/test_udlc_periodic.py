import unittest

class TestPeriodicDamage(unittest.TestCase):
    def test_cycle_recurrence_and_bounds(self):
        for d in range(13):
            for a in range(7):
                for b in range(9):
                    x = d
                    for n in range(20):
                        self.assertEqual(x, max(0, d+n*(a-b)))
                        peak = max(0, x+a)
                        if b >= a:
                            self.assertLessEqual(peak, d+a)
                        if b > a and n >= d:
                            self.assertEqual(x, 0)
                            self.assertEqual(peak, a)
                        x = max(0, peak-b)

    def test_zero_not_absorbing_inside_cycle(self):
        self.assertEqual(max(0, 0+3), 3)
        self.assertEqual(max(0, 3-5), 0)

if __name__ == "__main__":
    unittest.main()
