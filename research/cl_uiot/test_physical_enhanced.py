import unittest
from fractions import Fraction as Q
from physical_enhanced import compare
class EnhancedTests(unittest.TestCase):
    def test_zero(self):
        r=compare(budget=0)
        self.assertEqual(r["baseline"],{"unknown":1})
        self.assertFalse(r["combined_complete"])
    def test_point(self):
        r=compare(((Q(1,4),Q(1,4)),)*4)
        self.assertTrue(r["combined_complete"])
        self.assertEqual(r["baseline"],r["tightened"])
    def test_invalid(self):
        with self.assertRaises(ValueError):compare(budget=-1)
    def test_matched(self):
        r=compare(budget=255,depth=8)
        print("PCEGCO matched experiment:",r["used"],r["baseline"],r["tightened"],r["combined_complete"])
        self.assertLessEqual(r["used"],255)
        self.assertEqual(sum(r["baseline"].values()),len(r["leaves"]))
        self.assertEqual(sum(r["tightened"].values()),len(r["leaves"]))
        self.assertGreaterEqual(sum(v for k,v in r["tightened"].items() if k!="unknown"),
                                sum(v for k,v in r["baseline"].items() if k!="unknown"))
