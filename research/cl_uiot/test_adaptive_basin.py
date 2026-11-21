import unittest
from adaptive_basin import *
from fractions import Fraction as Q
class CoverageTests(unittest.TestCase):
    def test_zero(self):
        r=cover(budget=0)
        self.assertEqual(r["used"],0)
        self.assertEqual(r["leaves"],((r["root"],0,None,None),))
    def test_budget(self):
        r=cover(budget=7,cap=0)
        self.assertEqual(r["used"],7)
        self.assertTrue(verify(r))
    def test_uniform(self):
        r=cover(((Q(24,100),Q(26,100)),)*4)
        self.assertEqual(counts(r)["uniform"],1)
    def test_partition(self):
        r=cover(budget=1,cap=0)
        self.assertEqual(len(r["leaves"]),2)
        self.assertEqual(tuple(x[0] for x in r["leaves"]),split(r["root"]))
    def test_tampering(self):
        r=cover(budget=0)
        r["leaves"]=()
        self.assertFalse(verify(r))
    def test_depth(self):
        self.assertEqual(cover(depth=0,cap=0)["used"],1)
    def test_invalid(self):
        with self.assertRaises(ValueError):cover(budget=-1)
