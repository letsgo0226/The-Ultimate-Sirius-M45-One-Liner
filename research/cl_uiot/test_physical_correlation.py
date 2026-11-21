import unittest
from physical_correlation import *
from universal_pauli import from_bloch
class CorrelationTests(unittest.TestCase):
    def test_full(self):self.assertEqual(bloch_hull(((0,1),)*4),((-1,1),)*3)
    def test_pair(self):
        b=((Q(2,5),Q(3,5)),(Q(2,5),Q(3,5)),(0,Q(1,5)),(0,Q(1,5)))
        self.assertEqual(bloch_hull(b)[0],(Q(3,5),1))
    def test_point(self):
        z=(Q(1,2),Q(-1,2),Q(-1,2))
        self.assertEqual(bloch_hull(tuple((v,v) for v in from_bloch(*z))),tuple((v,v) for v in z))
    def test_uniform(self):
        b=((Q(1,5),Q(3,10)),)*4
        self.assertEqual(capture(b)["status"],"uniform")
    def test_invalid(self):
        with self.assertRaises(ValueError):bloch_hull(((Q(1,2),1),)*4)
