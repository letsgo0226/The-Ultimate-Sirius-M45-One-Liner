import unittest
from fractions import Fraction as Q
from brinkmann_metaplectic_3p1 import bracket,commutator_jet,shear,drift,split_step,multiply
from brinkmann_symplectic_3p1 import J

class MetaplecticTests(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(bracket([1,0,0,0],[0,1,0,0]),1)
    def test_variable(self):
        self.assertFalse(any(v for M in commutator_jet([1,2,3],2,7) for row in M for v in row))
    def test_flat(self):
        self.assertFalse(any(v for M in commutator_jet([],0,4) for row in M for v in row))
    def test_factors(self):
        for F in (shear(Q(2,3)),drift(Q(1,5)),split_step(3,Q(2,7))):
            self.assertEqual(tuple(tuple(bracket(a,b) for b in F) for a in F),J)
    def test_reverse(self):
        self.assertEqual(multiply(split_step(3,Q(2,7)),split_step(3,Q(-2,7))),drift(0))
    def test_zero_potential(self):
        self.assertEqual(split_step(0,Q(3,7)),drift(Q(3,7)))
