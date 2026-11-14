import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("self_calibration",Path(__file__).with_name("self_calibration.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestSelfCalibration(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(m.analyze(),m.analyze())
    def test_born_and_calibration_structure(self):
        r=m.analyze(theta=.3,actual=(.02,.15,.04),assumed=(.02,.02,.04),
                    calibration_shots=1000,science_shots=1000)
        self.assertAlmostEqual(r["shared_ideal_born_probability"],(1+math.sin(.3))/2)
        self.assertAlmostEqual(r["simultaneous_coverage_lower_bound"],.95)
        self.assertEqual(len(r["observers"]),3)
        for report in r["observers"]:
            self.assertLessEqual(report["flip_rate_confidence_interval"][0],
                                 report["flip_rate_confidence_interval"][1])
            self.assertLessEqual(report["calibrated_theta_confidence_interval"][0],
                                 report["calibrated_theta_confidence_interval"][1])
    def test_exact_inverse(self):
        p=.7
        for q in (0,.1,.3,.49):
            r=q+(1-2*q)*p
            interval=m.inverted_probability_interval([r,r],[q,q])
            self.assertAlmostEqual(interval[0],p)
            self.assertAlmostEqual(interval[1],p)
    def test_unidentifiable_boundary(self):
        self.assertEqual(m.inverted_probability_interval([.3,.7],[.2,.5]),[0.,1.])
    def test_interval_contains_valid_model(self):
        for q in (.02,.1,.35):
            p=.65
            r=q+(1-2*q)*p
            lo,hi=m.inverted_probability_interval([r-.02,r+.02],
                                                   [max(0,q-.01),min(.5,q+.01)])
            self.assertLessEqual(lo,p)
            self.assertGreaterEqual(hi,p)
    def test_invalid(self):
        cases=({"theta":math.pi/2},{"theta":float("nan")},
               {"actual":(.1,.2),"assumed":(.1,)},
               {"actual":(.1,.5),"assumed":(.1,.2)},
               {"calibration_shots":0},{"science_shots":0},
               {"alpha":0},{"alpha":1},{"seed":-1})
        for kw in cases:
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
