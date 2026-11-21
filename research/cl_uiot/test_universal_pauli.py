import unittest
from fractions import Fraction as Q
from universal_pauli import *
from logical_renormalization import depolarizing,derivative

class UniversalPauliTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(sum(c for d in coefficients() for k,c in d),1024)
    def test_map(self):
        w=(Q(7,10),Q(1,10),Q(1,20),Q(3,20))
        self.assertEqual(evaluate(w),logical_distribution(w))
    def test_identity(self):
        self.assertEqual(jacobian((1,0,0,0)),((0,0,0),)*3)
    def test_uniform(self):
        w=(Q(1,4),)*4
        self.assertEqual(evaluate(w),w)
        self.assertEqual(jacobian(w),((0,0,0),)*3)
    def test_radial_derivative(self):
        p=Q(1,8)
        self.assertTrue(all(sum(r)==derivative(p) for r in jacobian(depolarizing(p))))
    def test_bloch(self):
        w=(Q(7,10),Q(1,10),Q(1,20),Q(3,20))
        self.assertEqual(from_bloch(*bloch(w)),w)
        self.assertEqual(bloch_map(*bloch(w)),bloch(logical_distribution(w)))
    def test_invalid(self):
        with self.assertRaises(ValueError):from_bloch(1,1,-1)
