import unittest
from fractions import Fraction as Q
from conformal_geometry_3p1 import (
    christoffel_numerator,ricci_numerator,scalar_curvature_numerator,
    contraction_residual,scalar_wave_relation,demo
)

class ConformalGeometryTests(unittest.TestCase):
    def setUp(self):
        self.omega={(0,0,0,0):Q(2),(2,0,0,0):Q(1),
                    (0,0,2,0):Q(1)}
        self.phi=({(1,0,0,0):Q(2)}, {(0,1,0,1):Q(3)})

    def test_flat_connection_and_curvature(self):
        one={(0,0,0,0):Q(1)}
        for rho in range(4):
            for mu in range(4):
                for nu in range(4):
                    self.assertEqual(christoffel_numerator(one,rho,mu,nu),{})
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(ricci_numerator(one,mu,nu),{})
        self.assertEqual(scalar_curvature_numerator(one),{})

    def test_connection_lower_indices_symmetric(self):
        for rho in range(4):
            for mu in range(4):
                for nu in range(4):
                    self.assertEqual(christoffel_numerator(self.omega,rho,mu,nu),
                                     christoffel_numerator(self.omega,rho,nu,mu))

    def test_ricci_symmetric(self):
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(ricci_numerator(self.omega,mu,nu),
                                 ricci_numerator(self.omega,nu,mu))

    def test_ricci_scalar_contraction(self):
        self.assertEqual(contraction_residual(self.omega),{})

    def test_linear_omega_zero_scalar_curvature(self):
        omega={(0,0,0,0):Q(2),(1,0,0,0):Q(1)}
        self.assertEqual(scalar_curvature_numerator(omega),{})
        self.assertNotEqual(ricci_numerator(omega,0,0),{})

    def test_scalar_wave_equivalence(self):
        self.assertEqual(scalar_wave_relation(self.phi,self.omega,Q(3)),({},{}))

    def test_monomial_cases(self):
        for axis in range(4):
            for degree in range(4):
                exponents=[0]*4
                exponents[axis]=degree
                omega={(0,0,0,0):Q(2),tuple(exponents):Q(1)}
                self.assertEqual(contraction_residual(omega),{})
                self.assertEqual(scalar_wave_relation(self.phi,omega,Q(5,3)),({},{}))

    def test_demo(self):
        self.assertTrue(demo()["ricci_contraction"])
        self.assertTrue(demo()["curved_scalar_wave_identity"])

if __name__=="__main__":
    unittest.main()
