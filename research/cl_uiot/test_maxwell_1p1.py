import unittest
from fractions import Fraction as Q
from maxwell_1p1 import (
    field_strength, gauge_shift, lagrangian, euler_lagrange,
    maxwell_divergence, current_conserved, check_gauge_invariance, demo
)

class MaxwellTests(unittest.TestCase):
    def setUp(self):
        self.A = ({(1,1):Q(2)}, {(2,0):Q(3),(0,1):Q(1)})
        self.chi = {(3,1):Q(2),(0,2):Q(1)}

    def test_exact_curvature(self):
        self.assertEqual(field_strength(self.A), {(1,0):Q(4)})

    def test_gauge_invariance(self):
        self.assertTrue(check_gauge_invariance(self.A,self.chi))

    def test_pure_gauge_has_zero_curvature(self):
        pure = gauge_shift(({},{}),self.chi)
        self.assertEqual(field_strength(pure), {})
        self.assertEqual(lagrangian(pure), {})

    def test_variational_maxwell_identity(self):
        self.assertEqual(euler_lagrange(self.A),maxwell_divergence(self.A))

    def test_current_conservation(self):
        for i in range(4):
            for j in range(4):
                A=({(i,j):Q(2)}, {(j,i):Q(3)})
                self.assertTrue(current_conserved(maxwell_divergence(A)))

    def test_nonconserved_external_current_rejected(self):
        j=({(1,0):Q(1)}, {})
        self.assertFalse(current_conserved(j))

    def test_gauge_shift_does_not_change_source(self):
        self.assertEqual(maxwell_divergence(self.A),
                         maxwell_divergence(gauge_shift(self.A,self.chi)))

    def test_demo(self):
        self.assertTrue(demo()["gauge_invariant"])
        self.assertTrue(demo()["induced_current_conserved"])

if __name__ == "__main__":
    unittest.main()
