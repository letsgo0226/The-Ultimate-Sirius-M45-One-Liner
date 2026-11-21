import unittest
from fractions import Fraction as Q
from klein_gordon_1p1 import (
    add, box, check_covariance, demo, derivative, kg, mul, power, pullback
)
from lorentz_1p1 import boost

class KleinGordonTests(unittest.TestCase):
    def test_wave_operator_on_polynomial(self):
        # box(t^2+x^2) = 2 - 2 = 0.
        self.assertEqual(box({(2,0): Q(1), (0,2): Q(1)}), {})

    def test_mass_term(self):
        self.assertEqual(kg({(0,0): Q(3)}, Q(4)), {(0,0): Q(12)})

    def test_nontrivial_scalar_covariance(self):
        p = {(3,1): Q(2), (0,2): Q(3), (1,0): Q(-1), (0,0): Q(7)}
        for mass_squared in (Q(0), Q(1), Q(7,3)):
            for v in (Q(0), Q(3,5), Q(-3,5)):
                self.assertTrue(check_covariance(p, v, mass_squared))

    def test_many_monomials(self):
        for i in range(5):
            for j in range(5):
                self.assertTrue(check_covariance({(i,j): Q(1)}, Q(3,5), Q(2)))

    def test_pullback_composes_inverse(self):
        p = {(2,1): Q(2), (0,0): Q(5)}
        forward = pullback(p, boost(Q(3,5)))
        self.assertEqual(pullback(forward, boost(Q(-3,5))), p)

    def test_counterexample_nonlorentz_scaling(self):
        p = {(2,0): Q(1)}
        scaling_inverse = ((Q(2), Q(0)), (Q(0), Q(1)))
        self.assertNotEqual(box(pullback(p, scaling_inverse)),
                            pullback(box(p), scaling_inverse))

    def test_demo(self):
        self.assertTrue(demo()["kg_covariant"])

if __name__ == "__main__":
    unittest.main()
