import unittest
from fractions import Fraction as Q
from conformal_einstein_hilbert_3p1 import (
    eh_density,first_variation,variation_residual,
    euler_lagrange_density,trace_relation_residual,demo
)
from conformal_geometry_3p1 import box

class ConformalEinsteinHilbertTests(unittest.TestCase):
    def setUp(self):
        self.omega={(0,0,0,0):Q(2),(2,0,0,0):Q(1),
                    (0,0,2,0):Q(1)}
        self.delta={(1,0,0,0):Q(3),(0,1,0,0):Q(2)}

    def test_off_shell_variation(self):
        self.assertEqual(variation_residual(self.omega,self.delta),{})

    def test_trace_relation(self):
        self.assertEqual(trace_relation_residual(self.omega),{})

    def test_constant_flat_limit(self):
        omega={(0,0,0,0):Q(2)}
        self.assertEqual(eh_density(omega),{})
        self.assertEqual(euler_lagrange_density(omega),{})

    def test_monomial_cases(self):
        for axis in range(4):
            for degree in range(5):
                exponent=[0]*4
                exponent[axis]=degree
                omega={(0,0,0,0):Q(2)}
                key=tuple(exponent)
                omega[key]=omega.get(key,Q(0))+Q(1)
                self.assertEqual(variation_residual(omega,self.delta),{})
                self.assertEqual(trace_relation_residual(omega),{})

    def test_linear_factor_zero_euler_lagrange(self):
        omega={(0,0,0,0):Q(2),(1,0,0,0):Q(1)}
        self.assertEqual(euler_lagrange_density(omega),{})
        self.assertEqual(box(omega),{})

    def test_nontrivial_density(self):
        self.assertEqual(eh_density(self.omega),{})  # Box Omega = 2 - 2 = 0\n        curved={(0,0,0,0):Q(2),(2,0,0,0):Q(1)}\n        self.assertNotEqual(eh_density(curved),{})

    def test_demo(self):
        self.assertTrue(demo()["restricted_eh_variation_identity"])
        self.assertTrue(demo()["einstein_trace_consistency"])

if __name__=="__main__":
    unittest.main()
