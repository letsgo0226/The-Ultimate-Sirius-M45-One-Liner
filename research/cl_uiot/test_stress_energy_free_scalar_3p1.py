import unittest
from fractions import Fraction as Q
from stress_energy_free_scalar_3p1 import (
    free_lagrangian,free_eom,stress,divergence_stress,noether_residual,demo
)
class FreeStressTests(unittest.TestCase):
    def setUp(self):
        self.phi=({(2,0,0,0):Q(2),(0,1,0,0):Q(1)},
                  {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})

    def test_offshell_identity(self):
        for m2 in (Q(0),Q(1),Q(7,3)):
            for nu in range(4):
                self.assertEqual(noether_residual(self.phi,nu,m2),{})

    def test_monomial_stress(self):
        for axis in range(4):
            for degree in range(4):
                powers=[0]*4
                powers[axis]=degree
                phi=({tuple(powers):Q(3)},self.phi[1])
                for nu in range(4):
                    self.assertEqual(noether_residual(phi,nu,Q(5,2)),{})

    def test_massless_linear_solution(self):
        phi=({(1,0,0,0):Q(2)}, {(0,1,0,0):Q(3)})
        self.assertEqual(free_eom(phi,Q(0)),({},{ }))
        for nu in range(4):
            self.assertEqual(divergence_stress(phi,nu,Q(0)),{})

    def test_massive_constant_offshell(self):
        phi=({(0,0,0,0):Q(2)}, {})
        self.assertNotEqual(free_eom(phi,Q(3)),({},{}))
        self.assertEqual(free_lagrangian(phi,Q(3)), {(0,0,0,0):Q(-6)})

    def test_energy_density_positive_simple_example(self):
        phi=({(1,0,0,0):Q(2)}, {})
        self.assertEqual(stress(phi,0,0,Q(0)),{(0,0,0,0):Q(2)})

    def test_nonzero_divergence_offshell(self):
        self.assertTrue(any(divergence_stress(self.phi,nu,Q(3))
                            for nu in range(4)))

    def test_bad_index(self):
        with self.assertRaises(ValueError):
            stress(self.phi,4,0)

    def test_demo(self):
        self.assertTrue(demo()["off_shell_translation_noether_identity"])
        self.assertTrue(demo()["on_shell_stress_conserved"])

if __name__=="__main__":
    unittest.main()
