import unittest
from fractions import Fraction as Q
from adaptive_reliability import allocation,remaining,prefix,conservative_depth
from qec_concatenated_5qubit import iterate

class AdaptiveTests(unittest.TestCase):
    def test_budget_identity(self):
        e=Q(1,100)
        self.assertEqual(sum(allocation(e,t) for t in range(9))+remaining(e,9),e)
    def test_prefix(self):
        r=prefix(Q(1,20),Q(1,100),8,625)
        self.assertTrue(r["certified"])
        self.assertLessEqual(r["failure_bound"]+r["unallocated"],Q(1,100))
    def test_block(self):
        r=prefix(Q(1,20),Q(1,100),8,1)
        self.assertFalse(r["certified"])
        self.assertEqual(r["blocked_cycle"],0)
    def test_certificate(self):
        for t in range(8):
            n=conservative_depth(Q(1,20),Q(1,100),t)
            self.assertLessEqual(iterate(Q(1,20),n),allocation(Q(1,100),t))
    def test_zero(self):
        self.assertEqual(conservative_depth(0,Q(1,100),100),0)
    def test_empty(self):
        self.assertEqual(prefix(0,Q(1,100),0,1)["unallocated"],Q(1,100))
    def test_invalid(self):
        with self.assertRaises(ValueError):allocation(0,1)
