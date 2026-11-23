import unittest
from fractions import Fraction as Q
from stinespring_2level import unitary,transpose,mul,embed,joint,partial_trace,recover,purity
from amplitude_damping_2level import evolve
from quantum_entropy_2level import density

class DilationTests(unittest.TestCase):
    def test_unitary(self):
        U=unitary(Q(1,3))
        self.assertEqual(mul(U,transpose(U)),tuple(tuple(int(i==j) for j in range(4)) for i in range(4)))
    def test_channel(self):
        t=Q(1,3)
        self.assertEqual(partial_trace(joint(Q(1,2),Q(1,4),t),"S"),evolve(Q(1,2),Q(1,4),unitary(t)[2][2]))
    def test_full_transfer(self):
        R=joint(Q(3,4),Q(1,4),1)
        self.assertEqual(partial_trace(R,"S"),density(1,0))
        self.assertEqual(partial_trace(R,"E"),density(Q(3,4),Q(1,4)))
    def test_recovery(self):
        self.assertEqual(recover(joint(Q(3,4),Q(1,4),Q(2,3)),Q(2,3)),density(Q(3,4),Q(1,4)))
    def test_purity(self):
        self.assertEqual(purity(joint(Q(1,2),Q(1,4),Q(1,3))),purity(embed(Q(1,2),Q(1,4))))
    def test_correlations(self):
        R=joint(0,0,Q(1,3))
        self.assertEqual(purity(R),1)
        self.assertLess(purity(partial_trace(R,"S")),1)
    def test_invalid(self):
        with self.assertRaises(ValueError):unitary(2)
