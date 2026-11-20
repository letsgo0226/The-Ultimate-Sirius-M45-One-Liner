import unittest
from fractions import Fraction as Q
from critical_manifold import *
from universal_pauli import jacobian
from logical_renormalization import depolarizing

class CriticalTests(unittest.TestCase):
    def test_polynomial(self):
        for p in (Q(0),Q(1,8),Q(1,2),Q(1)):
            self.assertEqual(tuple(tuple(sum(c*p**i for i,c in enumerate(a)) for a in row) for row in slice_jacobian_polynomials()),jacobian(depolarizing(p)))
    def test_critical(self):
        self.assertEqual(critical_jacobian(),((Q(5,9),)*3,)*3)
    def test_radial(self):
        self.assertTrue(all(sum(r)==Q(5,3) for r in critical_jacobian()))
    def test_transverse(self):
        for v in ((1,-1,0),(0,1,-1)):
            self.assertEqual(tuple(sum(a*b for a,b in zip(r,v)) for r in critical_jacobian()),(0,0,0))
    def test_split(self):
        a,b=split((1,2,3))
        self.assertEqual(a,(2,2,2))
        self.assertEqual(b,(-1,0,1))
    def test_invalid(self):
        with self.assertRaises(ValueError):split((1,2))
