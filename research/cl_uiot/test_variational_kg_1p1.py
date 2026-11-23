import unittest
from fractions import Fraction as Q
from variational_kg_1p1 import (
    check_variational_identity, check_lagrangian_covariance,
    euler_lagrange, lagrangian, demo
)

class VariationalKGTests(unittest.TestCase):
    def test_constant_field_mass_term(self):
        phi = {(0,0): Q(3)}
        self.assertEqual(euler_lagrange(phi, Q(4)), {(0,0): Q(-12)})
        self.assertEqual(lagrangian(phi, Q(4)), {(0,0): Q(-18)})

    def test_massless_linear_solution(self):
        phi = {(1,0): Q(2), (0,1): Q(3)}
        self.assertEqual(euler_lagrange(phi, Q(0)), {})

    def test_variational_identity_on_monomials(self):
        for i in range(5):
            for j in range(5):
                for m2 in (Q(0), Q(1), Q(7,3)):
                    self.assertTrue(check_variational_identity({(i,j): Q(2)}, m2))

    def test_lagrangian_covariance(self):
        phi = {(3,1): Q(2), (0,2): Q(3), (1,0): Q(-1), (0,0): Q(7)}
        for v in (Q(0), Q(3,5), Q(-3,5)):
            for m2 in (Q(0), Q(1), Q(7,3)):
                self.assertTrue(check_lagrangian_covariance(phi, v, m2))

    def test_not_stationary_for_generic_massive_constant(self):
        self.assertNotEqual(euler_lagrange({(0,0): Q(1)}, Q(1)), {})

    def test_demo(self):
        self.assertTrue(demo()["euler_lagrange_equals_negative_kg"])
        self.assertTrue(demo()["lagrangian_lorentz_covariant"])

if __name__ == "__main__":
    unittest.main()
