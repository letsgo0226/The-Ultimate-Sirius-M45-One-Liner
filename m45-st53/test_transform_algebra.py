import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path
spec=importlib.util.spec_from_file_location("transform_algebra",Path(__file__).with_name("transform_algebra.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestTransforms(unittest.TestCase):
    def test_group_relations(self):
        self.assertEqual(m.operator("HH"),m.I)
        self.assertEqual(m.operator("ZZ"),m.I)
        self.assertEqual(m.operator("HZHZHZHZ"),m.I)
        self.assertEqual(m.compose(m.H,m.Z),m.operator("ZH"))
        self.assertEqual(m.compose(m.Z,m.H),m.operator("HZ"))
    def test_inverse(self):
        for word in ("","H","Z","HZ","ZHZ","HHZZHZ"):
            op=m.operator(word)
            self.assertEqual(m.compose(op,m.inverse(op)),m.I)
    def test_covariance(self):
        for word in ("","H","Z","HZ","ZH","HZH","ZHZ"):
            for x,z in (("0","0"),("3/5","4/5"),("-1/2","1/2")):
                r=m.report(x,z,word)
                self.assertTrue(all(v["covariant"] for v in r["contexts"].values()))
    def test_state_not_identical_to_context(self):
        s=m.state("3/5","4/5")
        h=m.transform(m.H,s)
        self.assertEqual(m.probability(h,"X"),m.probability(s,"Z"))
        self.assertNotEqual(m.probability(h,"X"),m.probability(s,"X"))
    def test_norm_preserved(self):
        s=m.state("3/5","4/5")
        for word in ("H","Z","HZ","ZHZ"):
            t=m.transform(m.operator(word),s)
            self.assertEqual(s[0]**2+s[1]**2,t[0]**2+t[1]**2)
    def test_bad_input(self):
        with self.assertRaises(ValueError):m.state("1","1")
        with self.assertRaises(ValueError):m.operator("Y")
        with self.assertRaises(ValueError):m.operator("H"*65)
        with self.assertRaises(ValueError):m.probability(m.state(0,0),"Y")
if __name__=="__main__":unittest.main()
