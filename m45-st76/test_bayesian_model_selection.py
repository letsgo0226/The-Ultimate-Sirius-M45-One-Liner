import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st76",Path(__file__).with_name("bayesian_model_selection.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestBayesianModelSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h=m.grid()
    def test_prior_normalization(self):
        w=m.posterior(self.h,[],.3)
        self.assertAlmostEqual(sum(w),1)
        self.assertAlmostEqual(m.model_probability(self.h,w),.3)
        self.assertEqual(len(self.h),1100)
    def test_predictive_information_nonnegative(self):
        w=m.posterior(self.h,[("reference_zero",3,10),("reference_one",8,10)],.5)
        for a in ("reference_zero","reference_one","science"):
            gain=m.expected_model_information(self.h,w,a)
            self.assertGreaterEqual(gain,0)
            self.assertLessEqual(gain,math.log(2)+1e-10)
    def test_symmetric_and_asymmetric_probabilities(self):
        h=("asymmetric",.6,.1,.2)
        self.assertAlmostEqual(m.outcome_probability(h,"reference_zero"),.1)
        self.assertAlmostEqual(m.outcome_probability(h,"reference_one"),.8)
        self.assertAlmostEqual(m.outcome_probability(h,"science"),.52)
    def test_deterministic(self):
        args=dict(steps=4,cal_shots=4,science_shots=4,seed=7)
        a=m.analyze(**args)
        self.assertEqual(a,m.analyze(**args))
        self.assertEqual(len(a["trace"]),5)
        self.assertAlmostEqual(a["posterior_symmetric"]+a["posterior_asymmetric"],1)
        self.assertTrue(-math.pi/2<a["posterior_mean_theta"]<math.pi/2)
        self.assertEqual(len(a["observations"]),7)
    def test_invalid(self):
        for kw in ({"theta":math.pi/2},{"q01":.5},{"q10":-.1},
                   {"steps":-1},{"steps":51},{"seed":-1},
                   {"prior_symmetric":0},{"prior_symmetric":1},
                   {"cal_shots":-1},{"science_shots":1001}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
