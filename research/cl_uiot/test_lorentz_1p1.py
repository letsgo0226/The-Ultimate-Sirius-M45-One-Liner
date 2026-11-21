import unittest
from fractions import Fraction as Q
from lorentz_1p1 import apply, boost, lorentz_invariant, mass_shell, minkowski_square, demo

class LorentzTests(unittest.TestCase):
    def test_metric_preserved(self):
        for v in (Q(0), Q(3,5), Q(-3,5)):
            self.assertTrue(lorentz_invariant(boost(v)))

    def test_inverse_boost(self):
        for x in ((Q(0), Q(0)), (Q(1), Q(2)), (Q(5), Q(3))):
            self.assertEqual(apply(boost(Q(-3,5)), apply(boost(Q(3,5)), x)), x)

    def test_mass_shell_preserved(self):
        k = (Q(5), Q(3))
        self.assertTrue(mass_shell(*k, Q(4)))
        self.assertTrue(mass_shell(*apply(boost(Q(3,5)), k), Q(4)))

    def test_generic_exact_vectors(self):
        b = boost(Q(3,5))
        for t in range(-3, 4):
            for x in range(-3, 4):
                p = (Q(t), Q(x))
                self.assertEqual(minkowski_square(p), minkowski_square(apply(b, p)))

    def test_reject_unsupported_boost(self):
        with self.assertRaises(ValueError):
            boost(Q(1,2))

    def test_example(self):
        self.assertTrue(demo()["lorentz_invariant"])
        self.assertTrue(demo()["mass_shell_after"])

if __name__ == "__main__":
    unittest.main()
