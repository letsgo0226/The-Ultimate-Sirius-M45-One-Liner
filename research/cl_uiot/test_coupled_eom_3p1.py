import unittest
from fractions import Fraction as Q
from coupled_eom_3p1 import (
    eom_scalar,matter_current,divergence,noether_residual,
    gauge_equation_residual,demo
)

Z={}
A0=(Z,Z,Z,Z)

class CoupledEOMTests(unittest.TestCase):
    def setUp(self):
        self.phi=({(1,0,0,0):Q(2),(0,1,0,0):Q(1)},
                  {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
        self.A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {},
                {(0,0,1,0):Q(3)})

    def test_free_massless_linear_field_on_shell(self):
        phi=({(1,0,0,0):Q(1)}, {(0,1,0,0):Q(1)})
        self.assertEqual(eom_scalar(phi,A0,Q(0),Q(1)),({},{ }))
        self.assertEqual(divergence(matter_current(phi,A0,Q(1))),{})

    def test_massive_constant_is_off_shell(self):
        phi=({(0,0,0,0):Q(2)}, {})
        self.assertNotEqual(eom_scalar(phi,A0,Q(3),Q(1)),({},{ }))

    def test_off_shell_noether_identity(self):
        for m2 in (Q(0),Q(1),Q(7,3)):
            for q in (Q(1),Q(2),Q(-3,2)):
                self.assertEqual(noether_residual(self.phi,self.A,m2,q),{})

    def test_polynomial_monomials(self):
        for axis in range(4):
            for degree in range(4):
                exponents=[0]*4
                exponents[axis]=degree
                phi=({tuple(exponents):Q(3)},self.phi[1])
                self.assertEqual(noether_residual(phi,self.A,Q(2),Q(3,2)),{})

    def test_generic_field_not_on_shell(self):
        self.assertTrue(any(gauge_equation_residual(self.phi,self.A,Q(2))))
        self.assertTrue(any(eom_scalar(self.phi,self.A,Q(3),Q(2))))

    def test_trivial_coupled_solution(self):
        phi=({}, {})
        self.assertEqual(eom_scalar(phi,A0,Q(5),Q(2)),({},{}))
        self.assertEqual(gauge_equation_residual(phi,A0,Q(2)),({},{},{},{}))

    def test_noether_identity_not_offshell_conservation(self):
        self.assertFalse(demo()["matter_current_conserved_off_shell"])
        self.assertTrue(demo()["off_shell_noether_identity"])

    def test_demo(self):
        self.assertTrue(demo()["off_shell_noether_identity"])
        self.assertFalse(demo()["gauge_equations_satisfied"])

if __name__=="__main__":
    unittest.main()
