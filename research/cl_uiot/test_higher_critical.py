import unittest
from higher_critical import *

class HigherCriticalTests(unittest.TestCase):
    def test_witness(self):
        self.assertEqual(radial_cubic((0,1,1,-2)),K(-45))
    def test_formula(self):
        for u,v in ((1,1),(1,2),(2,-3),(1,-1),(0,2)):
            t=(0,u,v,-u-v)
            self.assertEqual(cubic_graph(t),cubic_formula(t))
    def test_sign_reversal(self):
        self.assertEqual(cubic_graph((0,-1,-1,2)),-cubic_graph((0,1,1,-2)))
    def test_zero(self):
        self.assertEqual(cubic_graph((0,1,-1,0)),0)
    def test_invariance(self):
        v=(0,2,1,-3)
        self.assertEqual(Q(5,3)*cubic_graph(v)+radial_cubic(v),0)
    def test_invalid(self):
        with self.assertRaises(ValueError):cubic_graph((1,0,0,-1))
