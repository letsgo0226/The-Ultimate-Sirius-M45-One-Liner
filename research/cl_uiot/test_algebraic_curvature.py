import unittest
from fractions import Fraction as Q
from algebraic_curvature import *

class AlgebraicTests(unittest.TestCase):
    def test_field(self):
        self.assertEqual(K(0,1)**2,6)
        self.assertEqual(K(1,1)*K(1,-1),-5)
    def test_fixed(self):
        self.assertEqual(tuple(a[0] for a in jet((0,0,0,0))),critical())
    def test_radial(self):
        a=jet((-3,1,1,1))
        self.assertEqual(tuple(x[1] for x in a),(K(-5),)+(K(Q(5,3)),)*3)
    def test_transverse(self):
        for v in ((0,1,-1,0),(0,0,1,-1),(0,1,0,-1)):
            self.assertEqual(tuple(a[1] for a in jet(v)),(K(),)*4)
    def test_flat_quadratic(self):
        for v in ((0,1,-1,0),(0,0,1,-1),(0,1,0,-1)):
            self.assertEqual(curvature(v),0)
    def test_conservation(self):
        self.assertEqual(tuple(map(sum,zip(*jet((0,1,2,-3))))),(K(1),)+(K(),)*5)
    def test_invalid(self):
        with self.assertRaises(ValueError):curvature((-3,1,1,1))
