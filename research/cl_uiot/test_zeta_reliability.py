import unittest
from fractions import Fraction as Q
from zeta_reliability import zeta_bounds,allocation,prefix

class ZetaTests(unittest.TestCase):
    def test_bounds(self):
        self.assertEqual(zeta_bounds(2,1),(Q(3,2),Q(2)))
    def test_refinement(self):
        a,b=zeta_bounds(2,8);c,d=zeta_bounds(2,16)
        self.assertTrue(a<=c<=d<=b)
    def test_schedule(self):
        self.assertEqual(allocation(Q(1,100),1),allocation(Q(1,100),0)/4)
    def test_prefix_sum(self):
        e=Q(1,100)
        self.assertLess(sum(allocation(e,t) for t in range(100)),e)
    def test_prefix(self):
        r=prefix(Q(1,20),Q(1,100),8,625)
        self.assertTrue(r["certified"])
        self.assertLessEqual(r["failure_bound"],Q(1,100))
    def test_block(self):
        self.assertFalse(prefix(Q(1,20),Q(1,100),8,1)["certified"])
    def test_invalid(self):
        with self.assertRaises(ValueError):zeta_bounds(1,8)
