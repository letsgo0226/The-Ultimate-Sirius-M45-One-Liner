import unittest
from fractions import Fraction as Q
from physical_error_floor import *
from qec_concatenated_5qubit import depolarizing_failure,iterate

class FloorTests(unittest.TestCase):
    def test_witness(self):
        self.assertEqual(sum(c!="I" for c in witness()),2)
        self.assertNotIn(residual(witness()),stabilize())
    def test_one_level(self):
        p=Q(1,20)
        self.assertEqual(1-concatenate(p,1)[0],depolarizing_failure(p))
        self.assertGreaterEqual(depolarizing_failure(p),single_floor(p))
    def test_support(self):
        p=Q(1,20)
        for n in range(3):
            w=concatenate(p,n)
            self.assertEqual(sum(w),1)
            self.assertTrue(all(x>=full_support_floor(p,n)>0 for x in w))
    def test_upper(self):
        p=Q(1,20)
        self.assertLessEqual(1-concatenate(p,2)[0],iterate(p,2))
    def test_zero(self):
        self.assertEqual(concatenate(0,2),(1,0,0,0))
    def test_nonuniform(self):
        self.assertEqual(sum(logical_distribution((Q(1,2),Q(1,2),0,0))),1)
    def test_invalid(self):
        with self.assertRaises(ValueError):concatenate(Q(1,2),-1)
