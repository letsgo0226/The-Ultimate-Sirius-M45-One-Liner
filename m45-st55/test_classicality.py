import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("classicality",Path(__file__).with_name("classicality.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestClassicality(unittest.TestCase):
    def test_dephasing_reduces_coherence(self):
        a=m.analyze(64,0.7,1)
        b=m.analyze(64,0.7,0)
        self.assertGreater(a["observables"]["coherence_l1"],b["observables"]["coherence_l1"])
        self.assertAlmostEqual(a["observables"]["majority_failure_probability"],
                               b["observables"]["majority_failure_probability"])
    def test_concentration(self):
        a=m.analyze(4,0.7,0)
        b=m.analyze(256,0.7,0)
        self.assertGreater(a["observables"]["z_fraction_std"],b["observables"]["z_fraction_std"])
        self.assertGreater(a["observables"]["majority_failure_probability"],
                           b["observables"]["majority_failure_probability"])
    def test_hoeffding(self):
        for p in (0.1,0.3,0.7,0.9):
            for n in (1,2,16,128,256):
                r=m.analyze(n,p,0)
                o=r["observables"]
                self.assertLessEqual(o["majority_failure_probability"],
                                     o["hoeffding_failure_upper_bound"]+1e-10)
    def test_no_majority_target_at_half(self):
        r=m.analyze(64,0.5,0)
        self.assertIsNone(r["observables"]["majority_success_probability"])
        self.assertFalse(r["criteria"]["stable_majority"])
        self.assertFalse(r["criteria"]["operational_classicality"])
    def test_thresholds_are_operational(self):
        r=m.analyze(256,0.7,0,0.05,0.05)
        self.assertTrue(r["criteria"]["operational_classicality"])
        strict=m.analyze(256,0.7,0,0.05,0)
        self.assertFalse(strict["criteria"]["operational_classicality"])
    def test_bad_inputs(self):
        for kw in ({"n":0},{"n":257},{"p":-1},{"gamma":2},
                   {"coherence_tolerance":-1},{"majority_error_tolerance":float("nan")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
