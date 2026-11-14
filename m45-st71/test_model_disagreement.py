import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("model_disagreement",Path(__file__).with_name("model_disagreement.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestModelDisagreement(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(m.analyze(),m.analyze())
    def test_correct_calibration_has_coverage_guarantee(self):
        r=m.analyze(actual=(.02,.08,.15),assumed=(.02,.08,.15),shots=1000)
        self.assertTrue(r["assumption_based_coverage_guaranteed"])
        self.assertEqual(r["assumption_based_consensus_intersection"],
                         r["oracle_calibrated_consensus_intersection"])
        self.assertAlmostEqual(r["oracle_simultaneous_coverage_at_least"],.95)
    def test_misspecified_calibration_is_not_certified(self):
        r=m.analyze()
        self.assertFalse(r["assumption_based_coverage_guaranteed"])
        self.assertFalse(r["observers"][2]["calibration_correct"])
        self.assertAlmostEqual(r["shared_ideal_born_probability"],
                               (1+math.sin(.3))/2)
    def test_interval_monotonic_and_clipped(self):
        for q in (0,.1,.4):
            lo,hi=m.confidence_interval(0,10,q,.1)
            self.assertLessEqual(lo,hi)
            self.assertGreaterEqual(lo,-math.pi/2)
            self.assertLessEqual(hi,math.pi/2)
        self.assertEqual(m.parse_rates("0,0.1,0.2"),[0,.1,.2])
    def test_invalid(self):
        for bad in ("", "0.5,0.1", "-0.1,0.1","nan,0.1","abc,0.1"):
            with self.assertRaises(ValueError):m.parse_rates(bad)
        for kw in ({"theta":math.pi/2},{"shots":0},{"alpha":1},
                   {"seed":-1},{"actual":(.1,.2),"assumed":(.1,)},
                   {"actual":(.1,.5),"assumed":(.1,.2)}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
