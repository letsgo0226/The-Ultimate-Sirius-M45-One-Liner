import unittest
from fractions import Fraction as Q
from recursive_residual import *
class RefinementTests(unittest.TestCase):
    def test_zero(self):
        a=initial()
        self.assertEqual(refine(a,0)["leaves"],a)
    def test_preserve(self):
        a=initial(((Q(1,4),Q(1,4)),)*4)
        r=refine(a)
        self.assertTrue(r["complete"])
        self.assertEqual(refine(r["leaves"])["leaves"],r["leaves"])
    def test_nested(self):
        a=refine(initial(),1,2,0)["leaves"]
        r=refine(a,5,2,0)
        self.assertLessEqual(r["used"],5)
        for b,d,s,t in r["leaves"]:
            self.assertTrue(any(all(x<=u<=v<=y for (x,y),(u,v) in zip(c,b)) for c,*_ in a))
    def test_invalid(self):
        with self.assertRaises(ValueError):refine(initial(),-1)
    def test_experiment(self):
        from collections import Counter
        a=refine(initial(),127,6,1)
        b=refine(a["leaves"],255,4,1)
        print("RRRO refinement:",b["used"],dict(Counter(v[2] for v in b["leaves"])),b["complete"])
        self.assertLessEqual(b["used"],255)
