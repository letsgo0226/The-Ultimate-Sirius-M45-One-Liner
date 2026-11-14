import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("micro_macro",Path(__file__).with_name("micro_macro.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestMicroMacro(unittest.TestCase):
    def test_distribution_normalization(self):
        for n in (1,2,16,100,256):
            for p in (0,0.1,0.5,0.9,1):
                d=m.binomial(n,p)
                self.assertEqual(len(d),n+1)
                self.assertAlmostEqual(math.fsum(d),1,places=12)
                self.assertTrue(all(v>=0 for v in d))
    def test_ties_and_majority(self):
        a=m.analyze(2,0.5,0)
        self.assertAlmostEqual(a["macro"]["majority_plus"],0.25)
        self.assertAlmostEqual(a["macro"]["tie"],0.5)
        self.assertAlmostEqual(a["macro"]["majority_minus"],0.25)
        b=m.analyze(3,0.5,0)
        self.assertAlmostEqual(b["macro"]["majority_plus"],0.5)
        self.assertAlmostEqual(b["macro"]["tie"],0)
    def test_dephasing_changes_x_not_macro_z(self):
        a=m.analyze(17,0.7,0)
        b=m.analyze(17,0.7,1)
        self.assertAlmostEqual(a["macro"]["majority_plus"],b["macro"]["majority_plus"])
        self.assertAlmostEqual(a["single_qubit"]["Z"]["plus"],b["single_qubit"]["Z"]["plus"])
        self.assertNotAlmostEqual(a["single_qubit"]["X"]["plus"],b["single_qubit"]["X"]["plus"])
    def test_concentration(self):
        a=m.analyze(4,0.7,0)
        b=m.analyze(100,0.7,0)
        self.assertLess(b["macro"]["fraction_standard_deviation"],
                        a["macro"]["fraction_standard_deviation"])
    def test_extremes(self):
        self.assertEqual(m.analyze(5,0,0)["macro"]["majority_plus"],0)
        self.assertEqual(m.analyze(5,1,0)["macro"]["majority_plus"],1)
    def test_bad_parameters(self):
        for n,p in ((0,0.5),(257,0.5),(4,-0.1),(4,float("nan"))):
            with self.assertRaises(ValueError):m.binomial(n,p)
if __name__=="__main__":unittest.main()
