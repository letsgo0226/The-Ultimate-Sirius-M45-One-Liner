import unittest
from hybrid_elimination import *
class HybridTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(refine(initial(),0)["leaves"],initial())
    def test_uniform(self):
        b=((Q(1,4),Q(1,4)),)*4
        self.assertEqual(capture_hybrid(b),"uniform")
    def test_preserve(self):
        b=((Q(1,4),Q(1,4)),)*4
        a=((b,0,"uniform","uniform"),)
        self.assertEqual(refine(a)["leaves"],a)
    def test_experiment(self):
        a=refine(initial(),255,8)
        b=refine(a["leaves"],255,12)
        for r in (a,b):
            print("HEGEO matched experiment:",r["used"],r["baseline"],r["hybrid"],r["complete"])
            self.assertLessEqual(r["used"],255)
            self.assertTrue(all(x=="unknown" or y!="unknown" for _,_,x,y in r["leaves"]))
        self.assertTrue(all(v in b["leaves"] for v in a["leaves"] if v[2]!="unknown" or v[3]!="unknown"))
    def test_invalid(self):
        with self.assertRaises(ValueError):refine(initial(),-1)
