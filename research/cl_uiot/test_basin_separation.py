import unittest
from basin_separation import *
from universal_pauli import from_bloch
from logical_renormalization import depolarizing

class BasinTests(unittest.TestCase):
    def test_formula(self):
        for w in ((Q(7,10),Q(1,10),Q(1,20),Q(3,20)),(Q(1,2),Q(1,2),0,0),depolarizing(Q(1,5))):
            self.assertEqual(closed_bloch(*bloch(w)),bloch(evaluate(w)))
    def test_uniform(self):
        self.assertEqual(classify((Q(1,4),)*4),"uniform")
        self.assertLess(uniform_bound(Q(1,4)),Q(1,4))
    def test_vertices(self):
        for i,c in enumerate("IXYZ"):
            w=tuple(int(i==j) for j in range(4))
            self.assertEqual(evaluate(w),w)
            self.assertEqual(classify(w),"identity" if i==0 else "pauli_"+c)
    def test_lower(self):
        self.assertEqual(orbit(depolarizing(Q(1,8)),4)["basin"],"identity")
    def test_upper(self):
        self.assertEqual(orbit(depolarizing(Q(1,4)),4)["basin"],"uniform")
    def test_unknown(self):self.assertIsNone(orbit(depolarizing(Q(1,8)),0)["basin"])
    def test_invalid(self):
        with self.assertRaises(ValueError):orbit((1,0,0,0),-1)
