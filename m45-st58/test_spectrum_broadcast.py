import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("sbs",Path(__file__).with_name("spectrum_broadcast.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestSpectrumBroadcast(unittest.TestCase):
    def test_density_valid(self):
        for n in (1,2,4,8):
            for p,q in ((0.5,0),(0.2,0.1),(1,0.5)):
                with self.subTest(n=n,p=p,q=q):
                    r=m.analyze(n,p,q)
                    self.assertEqual(len(r["joint_density_matrix_diagonal"]),2**(n+1))
                    self.assertTrue(all(v>=0 for v in r["joint_density_matrix_diagonal"]))
                    self.assertAlmostEqual(r["trace"],1,places=12)
                    self.assertGreaterEqual(r["system_environment_mutual_information_bits"],-1e-10)
                    self.assertLessEqual(r["system_environment_mutual_information_bits"],r["system_entropy_bits"]+1e-10)
    def test_exact_sbs(self):
        r=m.analyze(4,0.5,0)
        self.assertTrue(r["exact_sbs_conditional_support_orthogonal"])
        self.assertEqual(r["single_fragment_trace_overlap"],0)
        self.assertAlmostEqual(r["system_environment_mutual_information_bits"],1)
    def test_overlap_not_sbs(self):
        r=m.analyze(4,0.5,0.1)
        self.assertFalse(r["exact_sbs_conditional_support_orthogonal"])
        self.assertGreater(r["single_fragment_trace_overlap"],0)
        self.assertLess(r["system_environment_mutual_information_bits"],1)
    def test_uninformative(self):
        r=m.analyze(4,0.5,0.5)
        self.assertFalse(r["exact_sbs_conditional_support_orthogonal"])
        self.assertAlmostEqual(r["system_environment_mutual_information_bits"],0,places=12)
    def test_fragment_improvement(self):
        a=m.analyze(1,0.5,0.1)
        b=m.analyze(8,0.5,0.1)
        self.assertGreater(b["system_environment_mutual_information_bits"],
                           a["system_environment_mutual_information_bits"])
    def test_invalid(self):
        for kw in ({"n":0},{"n":9},{"n":True},{"p":-0.1},{"q":0.6},{"q":float("nan")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
