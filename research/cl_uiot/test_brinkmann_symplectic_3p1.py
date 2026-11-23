import unittest
from fractions import Fraction as Q
from brinkmann_symplectic_3p1 import generator,hamiltonian,energy_rate,flow_jet,symplectic_residual,J

class SymplecticTests(unittest.TestCase):
    def test_generator(self):
        A=generator(3)
        for a in range(4):
            for b in range(4):
                self.assertEqual(sum(A[r][a]*J[r][b]+J[a][r]*A[r][b] for r in range(4)),0)
    def test_initial(self):
        self.assertEqual(flow_jet([1],0,0)[0],tuple(tuple(int(a==b) for b in range(4)) for a in range(4)))
    def test_variable_curvature(self):
        self.assertFalse(any(v for M in symplectic_residual([1,2,3],2,7) for row in M for v in row))
    def test_flat(self):
        self.assertFalse(any(v for M in symplectic_residual([],0,4) for row in M for v in row))
    def test_energy(self):
        self.assertEqual(hamiltonian(2,[3,4,1,2]),18)
    def test_explicit_time_dependence(self):
        self.assertEqual(energy_rate(3,[3,4,1,2]),12)
