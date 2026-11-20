import unittest
from fractions import Fraction as Q
from brinkmann_geodesic_3p1 import shifted,jet,fundamental,wronskian_jet

class GeodesicTests(unittest.TestCase):
    def test_flat(self):
        self.assertEqual(jet([],2,3,4,-1,4),[3,4,0,0,0])
    def test_oscillator(self):
        self.assertEqual(jet([1],0,1,0,-1,4),[1,0,Q(-1,2),0,Q(1,24)])
    def test_hyperbolic(self):
        self.assertEqual(jet([1],0,1,0,1,4),[1,0,Q(1,2),0,Q(1,24)])
    def test_shift(self):
        self.assertEqual(shifted([1,2,3],2),[17,14,3])
    def test_wronskian(self):
        for sign in (-1,1):
            self.assertEqual(wronskian_jet([1,2,3],2,sign,8),[1]+[0]*7)
    def test_invalid(self):
        with self.assertRaises(ValueError):jet([1],0,1,0,1,0)
