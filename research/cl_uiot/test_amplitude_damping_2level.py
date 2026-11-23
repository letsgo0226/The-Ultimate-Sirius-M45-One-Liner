import unittest
from fractions import Fraction as Q
from amplitude_damping_2level import kraus,evolve,trace_distance_squared,entropy_after
from quantum_entropy_2level import mul,transpose,density,entropy

class DampingTests(unittest.TestCase):
    def test_completeness(self):
        A,L,w=kraus(Q(2,3))
        P=mul(transpose(A),A);R=mul(transpose(L),L)
        self.assertEqual(tuple(tuple(P[i][j]+w*R[i][j] for j in range(2)) for i in range(2)),((1,0),(0,1)))
    def test_composition(self):
        R=evolve(Q(3,4),Q(1,4),Q(2,3),3)
        self.assertEqual(evolve(R[0][0],R[0][1],Q(2,3),4),evolve(Q(3,4),Q(1,4),Q(2,3),7))
    def test_reset(self):
        self.assertEqual(evolve(0,0,0),density(1,0))
    def test_fixed(self):
        self.assertEqual(evolve(1,0,Q(2,3),10),density(1,0))
    def test_convergence(self):
        self.assertLess(trace_distance_squared(Q(1,2),Q(1,4),Q(1,2),10),Q(1,1000000))
    def test_entropy_not_monotone(self):
        self.assertGreater(entropy_after(0,0,Q(1,2),1),entropy(0,0))
    def test_invalid(self):
        with self.assertRaises(ValueError):evolve(1,0,2)
