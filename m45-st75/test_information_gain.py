import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("information_gain",Path(__file__).with_name("information_gain.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestInformationGain(unittest.TestCase):
    def test_expected_variance_reduction_identity(self):
        # Beta(2,3) posterior: Var=6/(25*6)=.04.
        self.assertAlmostEqual(m.expected_variance_reduction(0,0,2,3,5),.02)
        self.assertEqual(m.expected_variance_reduction(0,0,2,3,0),0)
    def test_decision_and_risk_finite(self):
        for counts in ((0,20,10,20),(2,50,40,50),(15,20,5,20)):
            risk,gq,gr=m.theta_risk_and_gains(*counts,10)
            self.assertTrue(all(math.isfinite(v) and v>=0 for v in (risk,gq,gr)))
            self.assertIn(m.choose(*counts,10),("calibration","science"))
    def test_reproducibility(self):
        args=dict(budget=200,batch=20,replications=6,seed=77)
        self.assertEqual(m.analyze(**args),m.analyze(**args))
    def test_four_policies_and_budget(self):
        r=m.analyze(budget=240,batch=20,replications=8)
        self.assertEqual(set(r["policy_summaries"]),
                         {"balanced","science_heavy","adaptive","expected_risk"})
        for s in r["policy_summaries"].values():
            self.assertTrue(40<=s["mean_trials"]<=240)
            self.assertTrue(0<=s["empirical_coverage"]<=1)
            self.assertTrue(0<=s["target_reached_fraction"]<=1)
        self.assertAlmostEqual(r["frequentist_simultaneous_coverage_lower_bound_per_replication"],.95)
    def test_invalid(self):
        for kw in ({"replications":0},{"budget":1},{"batch":0},
                   {"flip":.5},{"alpha":1},{"seed":-1},
                   {"budget":100000,"replications":100}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
