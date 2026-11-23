import unittest
from fractions import Fraction
from godel_dirichlet import factor,reconstruct,evaluate,derivative_log_signature

class TestGodelDirichlet(unittest.TestCase):
    def test_roundtrip(self):
        for g in range(1,10001):
            t=factor(g)
            self.assertEqual(reconstruct(t),g)
            self.assertEqual(derivative_log_signature(t),t)
    def test_values(self):
        t=factor(60)
        self.assertEqual(t,((2,2),(3,1),(5,1)))
        self.assertEqual(evaluate(t,0),4)
        self.assertEqual(evaluate(t,1),Fraction(23,15))
        self.assertEqual(evaluate(t,-1),12)
        self.assertEqual(evaluate((),0),0)
    def test_invalid(self):
        for t in (((4,1),),((2,0),),((3,1),(2,1)),((2,1),(2,2)),((2,27),)):
            with self.assertRaises(ValueError):
                reconstruct(t)
        for g in (0,-1,True,10**8+1):
            with self.assertRaises(ValueError):
                factor(g)
