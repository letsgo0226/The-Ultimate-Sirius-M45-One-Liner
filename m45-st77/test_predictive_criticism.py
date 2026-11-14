import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st77",Path(__file__).with_name("predictive_criticism.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestPredictiveCriticism(unittest.TestCase):
    def test_binomial(self):
        self.assertAlmostEqual(sum(m.binomial_pmf(k,10,.3) for k in range(11)),1)
        self.assertEqual(m.binomial_pmf(0,10,0),1)
        self.assertEqual(m.binomial_pmf(10,10,1),1)
    def test_predictive_mixture(self):
        h=[("symmetric",.3,.1,.1),("asymmetric",.7,.2,.3)]
        w=[.4,.6]
        pmf=m.predictive_pmf(h,w,"science",10)
        self.assertAlmostEqual(sum(pmf),1)
        self.assertTrue(all(0<=v<=1 for v in pmf))
        c=m.predictive_check(pmf,4)
        self.assertTrue(0<=c["two_sided_predictive_tail_area"]<=1)
    def test_reproducible(self):
        kw=dict(train_shots=8,holdout_shots=10,seed=17)
        self.assertEqual(m.analyze(**kw),m.analyze(**kw))
    def test_outputs(self):
        r=m.analyze(train_shots=8,holdout_shots=10)
        self.assertEqual(set(r["holdout_checks"]),set(m.ACTIONS))
        self.assertAlmostEqual(r["posterior_symmetric"]+r["posterior_asymmetric"],1)
        self.assertAlmostEqual(r["flag_threshold_per_action"],.05/3)
        self.assertTrue(all(v["heldout_trials"]==10 for v in r["holdout_checks"].values()))
    def test_invalid(self):
        for kw in ({"theta":math.pi/2},{"q01":.5},{"q10":-.1},
                   {"holdout_shots":0},{"holdout_shots":201},
                   {"science_drift":.6},{"alpha":0},{"seed":-1},
                   {"prior_symmetric":1}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
