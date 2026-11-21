import unittest
from fractions import Fraction as Q
from finite_resource_nogo import *

class NoGoTests(unittest.TestCase):
    def test_fixed(self):
        self.assertEqual(fixed_upper(Q(1,10),3),Q(729,1000))
    def test_bounds(self):
        self.assertEqual(survival_bounds([Q(1,10)]*2,[Q(1,5)]*2),(Q(16,25),Q(81,100)))
    def test_crossing(self):
        self.assertEqual(crossing(Q(1,2),Q(1,8),10),3)
        self.assertIsNone(crossing(Q(1,2),Q(1,8),2))
    def test_endpoints(self):
        self.assertEqual(fixed_upper(1,0),1)
        self.assertEqual(fixed_upper(1,1),0)
        self.assertEqual(fixed_upper(0,100),1)
    def test_exact(self):
        self.assertEqual(exact_survival([Q(1,2),Q(1,3)]),Q(1,3))
    def test_summable(self):
        h=[Q(1,2**(t+2)) for t in range(10)]
        self.assertGreaterEqual(exact_survival(h),1-sum(h))
    def test_invalid(self):
        with self.assertRaises(ValueError):survival_bounds([1],[0])
        with self.assertRaises(ValueError):fixed_upper(0,-1)
