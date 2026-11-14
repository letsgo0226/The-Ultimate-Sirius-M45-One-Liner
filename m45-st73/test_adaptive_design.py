import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("adaptive_design",Path(__file__).with_name("adaptive_design.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestAdaptiveDesign(unittest.TestCase):
    def test_reproducible(self):
        self.assertEqual(m.analyze(),m.analyze())
    def test_budget_and_history(self):
        r=m.analyze(budget=1200,batch=50,target_width=.1)
        self.assertLessEqual(r["total_trials_used"],1200)
        self.assertEqual(r["total_trials_used"],r["calibration_trials_used"]+r["science_trials_used"])
        self.assertEqual(r["history"][-1]["trials"],r["total_trials_used"])
        self.assertEqual(r["history"][-1]["theta_interval"],r["final_theta_confidence_interval"])
        self.assertAlmostEqual(r["confidence_coverage_lower_bound"],.95)
    def test_born_and_noise(self):
        for theta,q in ((0,0),(.3,.15),(-.4,.3)):
            r=m.analyze(theta=theta,flip=q,budget=200,batch=20)
            p=(1+math.sin(theta))/2
            self.assertAlmostEqual(r["ideal_born_probability"],p)
            self.assertAlmostEqual(r["observed_science_probability"],q+(1-2*q)*p)
    def test_interval_validity(self):
        for nq,nr in ((20,20),(50,100),(1000,1000)):
            lo,hi=m.interval(0,nq,nr//2,nr,math.log(400))
            self.assertLessEqual(lo,hi)
            self.assertGreaterEqual(lo,-math.pi/2)
            self.assertLessEqual(hi,math.pi/2)
        self.assertEqual(m.interval(10,20,10,20,100),[-math.pi/2,math.pi/2])
    def test_early_stop(self):
        r=m.analyze(budget=1000,batch=20,target_width=math.pi)
        self.assertEqual(r["stopping_reason"],"target_reached")
        self.assertEqual(r["total_trials_used"],40)
    def test_invalid(self):
        cases=({"theta":math.pi/2},{"flip":.5},{"budget":1},{"batch":0},
               {"budget":10,"batch":6},{"alpha":0},{"seed":-1},
               {"target_width":0},{"target_width":float("nan")})
        for kw in cases:
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
