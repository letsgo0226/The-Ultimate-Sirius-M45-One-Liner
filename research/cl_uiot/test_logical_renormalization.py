import unittest
from fractions import Fraction as Q
from logical_renormalization import *

class RenormalizationTests(unittest.TestCase):
    def test_slice(self):
        for p in (0,Q(1,20),Q(1,2),Q(3,4),1):
            self.assertEqual(renormalize(depolarizing(p)),depolarizing(scalar(p)))
    def test_fixed(self):
        self.assertEqual(scalar(0),0)
        self.assertEqual(scalar(Q(3,4)),Q(3,4))
    def test_derivatives(self):
        self.assertEqual(derivative(0),0)
        self.assertEqual(derivative(Q(3,4)),0)
    def test_threshold(self):
        lo,hi=threshold_bracket(20)
        self.assertLessEqual(scalar(lo),lo)
        self.assertGreaterEqual(scalar(hi),hi)
        self.assertLess(hi-lo,Q(1,10**6))
        self.assertTrue(Q(13,100)<lo<hi<Q(15,100))
    def test_basins(self):
        self.assertLess(scalar(Q(1,10)),Q(1,10))
        self.assertGreater(scalar(Q(1,5)),Q(1,5))
        self.assertLess(scalar(1),Q(3,4)+Q(1,4))
        self.assertGreater(scalar(1),Q(3,4))
    def test_iteration(self):
        self.assertEqual(iterate_scalar(Q(1,20),2),scalar(scalar(Q(1,20))))
    def test_invalid(self):
        with self.assertRaises(ValueError):threshold_bracket(-1)
