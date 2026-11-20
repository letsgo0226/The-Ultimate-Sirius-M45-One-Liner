import unittest
from fractions import Fraction as Q
from qec_concatenated_5qubit import *

class ConcatenatedTests(unittest.TestCase):
    def test_endpoints(self):
        self.assertEqual((bound(0),bound(1)),(0,1))
    def test_factor(self):
        p=Q(1,20)
        self.assertEqual(bound(p),10*p**2-20*p**3+15*p**4-4*p**5)
    def test_certificate(self):
        for n in range(4):
            self.assertLessEqual(iterate(Q(1,20),n),certified_bound(Q(1,20),n))
    def test_zero(self):
        self.assertEqual(iterate(0,4),0)
    def test_counts(self):
        self.assertEqual(failure_counts()[:2],(0,0))
        self.assertEqual(failure_counts()[2],90)
    def test_exact_bound(self):
        for p in (Q(0),Q(1,20),Q(1,2),Q(1)):
            self.assertLessEqual(depolarizing_failure(p),bound(p))
    def test_invalid(self):
        with self.assertRaises(ValueError):certified_bound(Q(1,10),2)
