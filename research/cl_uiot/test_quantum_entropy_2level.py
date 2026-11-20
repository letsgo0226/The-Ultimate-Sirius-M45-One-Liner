import unittest
from fractions import Fraction as Q
from quantum_entropy_2level import density,rotation,evolve,invariants,entropy,measurement_entropy,mul,transpose

class EntropyTests(unittest.TestCase):
    def test_unitary(self):
        U=rotation(Q(2,3))
        self.assertEqual(mul(U,transpose(U)),((1,0),(0,1)))
    def test_spectrum(self):
        a,b=Q(3,4),Q(1,8)
        R=evolve(a,b,Q(2,3))
        self.assertEqual(invariants(a,b),invariants(R[0][0],R[0][1]))
        self.assertEqual(entropy(a,b),entropy(R[0][0],R[0][1]))
    def test_pure(self):
        R=evolve(1,0,Q(1,3))
        self.assertEqual(invariants(R[0][0],R[0][1]),(0,1))
        self.assertEqual(entropy(R[0][0],R[0][1]),0)
    def test_mixed(self):
        self.assertEqual(entropy(Q(1,2),0),1)
        self.assertEqual(evolve(Q(1,2),0,2),density(Q(1,2),0))
    def test_measurement(self):
        self.assertEqual(entropy(Q(1,2),Q(1,2)),0)
        self.assertEqual(measurement_entropy(Q(1,2),Q(1,2)),1)
    def test_invalid(self):
        with self.assertRaises(ValueError):density(Q(1,2),1)
