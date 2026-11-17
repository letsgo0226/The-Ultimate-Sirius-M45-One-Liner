import unittest
from fractions import Fraction as Q
from stress_energy_coupled_3p1 import total_stress,stress_divergence,noether_residual,demo

class CoupledStressTests(unittest.TestCase):
    def setUp(self):
        self.phi=({(1,0,0,0):Q(2),(0,1,0,0):Q(1)},
                  {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
        self.A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)}, {},
                {(0,0,1,0):Q(3)})

    def test_off_shell_identity(self):
        for nu in range(4):
            self.assertEqual(noether_residual(self.phi,self.A,nu,Q(3),Q(2)),{})

    def test_monomial_examples(self):
        for axis in range(4):
            for degree in range(3):
                exponents=[0]*4
                exponents[axis]=degree
                phi=({tuple(exponents):Q(2)},self.phi[1])
                for nu in range(4):
                    self.assertEqual(noether_residual(phi,self.A,nu,Q(5,3),Q(2)),{})

    def test_vacuum_solution(self):
        z=({}, {})
        A=({},{},{},{})
        for nu in range(4):
            self.assertEqual(stress_divergence(z,A,nu,Q(3),Q(2)),{})

    def test_electric_energy_positive(self):
        z=({}, {})
        A=({}, {(1,0,0,0):Q(2)}, {}, {})
        self.assertEqual(total_stress(z,A,0,0,Q(1),Q(2)),
                         {(0,0,0,0):Q(2)})

    def test_symmetric_raised_tensor(self):
        from maxwell_3p1 import ETA,scale
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(scale(total_stress(self.phi,self.A,mu,nu,Q(2),Q(2)),ETA[nu]),
                                 scale(total_stress(self.phi,self.A,nu,mu,Q(2),Q(2)),ETA[mu]))

    def test_demo(self):
        self.assertTrue(demo()["off_shell_total_stress_identity"])

if __name__=="__main__":
    unittest.main()
