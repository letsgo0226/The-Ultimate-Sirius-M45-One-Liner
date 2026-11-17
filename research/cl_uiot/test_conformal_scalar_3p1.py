import unittest
from fractions import Fraction as Q
from conformal_scalar_3p1 import (
    density,eom_density,variational_residual,first_variation,demo
)
from stress_energy_free_scalar_3p1 import free_lagrangian,free_eom

class ConformalScalarTests(unittest.TestCase):
    def setUp(self):
        self.phi=({(2,0,0,0):Q(2)}, {(0,1,0,0):Q(3)})
        self.delta=({(0,0,1,0):Q(1)}, {(1,0,0,1):Q(2)})
        self.omega={(0,0,0,0):Q(1),(1,0,0,0):Q(1)}

    def test_nonconstant_background_identity(self):
        self.assertEqual(variational_residual(
            self.phi,self.delta,self.omega,Q(3)),{})

    def test_massless_identity(self):
        self.assertEqual(variational_residual(
            self.phi,self.delta,self.omega,Q(0)),{})

    def test_varied_monomials(self):
        for axis in range(4):
            for degree in range(4):
                powers=[0]*4
                powers[axis]=degree
                omega={(0,0,0,0):Q(2),tuple(powers):Q(1)}
                self.assertEqual(variational_residual(
                    self.phi,self.delta,omega,Q(5,3)),{})

    def test_flat_limit_density(self):
        one={(0,0,0,0):Q(1)}
        self.assertEqual(density(self.phi,one,Q(3)),
                         free_lagrangian(self.phi,Q(3)))

    def test_flat_limit_eom(self):
        one={(0,0,0,0):Q(1)}
        self.assertEqual(eom_density(self.phi,one,Q(3)),
                         free_eom(self.phi,Q(3)))

    def test_constant_solution_massless(self):
        phi=({(0,0,0,0):Q(2)}, {})
        self.assertEqual(eom_density(phi,self.omega,Q(0)),({},{}))

    def test_demo(self):
        self.assertTrue(demo()["nonconstant_conformal_variational_identity"])

if __name__=="__main__":
    unittest.main()
