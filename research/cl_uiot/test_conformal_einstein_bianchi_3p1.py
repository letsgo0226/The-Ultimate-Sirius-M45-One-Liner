import unittest
from fractions import Fraction as Q
from conformal_einstein_bianchi_3p1 import (
    einstein_numerator,trace_residual,contracted_bianchi_residual,demo
)

class ConformalEinsteinBianchiTests(unittest.TestCase):
    def setUp(self):
        self.omega={(0,0,0,0):Q(2),(2,0,0,0):Q(1),
                    (0,0,2,0):Q(1)}

    def test_flat_zero_tensor(self):
        omega={(0,0,0,0):Q(1)}
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(einstein_numerator(omega,mu,nu),{})

    def test_einstein_tensor_symmetric(self):
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(einstein_numerator(self.omega,mu,nu),
                                 einstein_numerator(self.omega,nu,mu))

    def test_trace_relation(self):
        self.assertEqual(trace_residual(self.omega),{})

    def test_contracted_bianchi(self):
        for nu in range(4):
            self.assertEqual(contracted_bianchi_residual(self.omega,nu),{})

    def test_linear_factor(self):
        omega={(0,0,0,0):Q(2),(1,0,0,0):Q(1)}
        self.assertEqual(trace_residual(omega),{})
        for nu in range(4):
            self.assertEqual(contracted_bianchi_residual(omega,nu),{})

    def test_monomial_factors(self):
        for axis in range(4):
            for degree in range(4):
                exponents=[0]*4
                exponents[axis]=degree
                omega={(0,0,0,0):Q(2)}
                omega[tuple(exponents)]=omega.get(tuple(exponents),Q(0))+Q(1)
                self.assertEqual(trace_residual(omega),{})
                for nu in range(4):
                    self.assertEqual(contracted_bianchi_residual(omega,nu),{})

    def test_invalid_index(self):
        with self.assertRaises(ValueError):
            contracted_bianchi_residual(self.omega,4)

    def test_demo(self):
        self.assertTrue(demo()["contracted_bianchi_all_four_components"])
        self.assertTrue(demo()["einstein_trace_identity"])

if __name__=="__main__":
    unittest.main()
