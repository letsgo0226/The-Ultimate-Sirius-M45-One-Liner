import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("benchmark",Path(__file__).with_name("active_learning_benchmark.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestActiveLearningBenchmark(unittest.TestCase):
    def test_reproducible(self):
        args=dict(budget=200,batch=20,replications=8,seed=41)
        self.assertEqual(m.analyze(**args),m.analyze(**args))
    def test_policy_metrics(self):
        r=m.analyze(budget=240,batch=20,replications=10)
        self.assertEqual(set(r["policy_summaries"]),set(m.POLICIES))
        self.assertAlmostEqual(r["ideal_born_probability"],(1+math.sin(.3))/2)
        for s in r["policy_summaries"].values():
            self.assertGreaterEqual(s["mean_trials_used"],40)
            self.assertLessEqual(s["mean_trials_used"],240)
            self.assertTrue(0<=s["empirical_coverage"]<=1)
            self.assertTrue(0<=s["target_reached_fraction"]<=1)
            self.assertGreaterEqual(s["mean_interval_width"],0)
    def test_paired_stream_identity(self):
        st73=m.load("st73","m45-st73/adaptive_design.py")
        cal=[False]*100
        sci=[True]*100
        kwargs=(20,100,math.log(4*100/.05),math.pi,.3,st73)
        a=m.run_policy("balanced",cal,sci,*kwargs)
        b=m.run_policy("science_heavy",cal,sci,*kwargs)
        self.assertEqual(a["trials_used"],b["trials_used"])
        self.assertEqual(a["theta_interval"],b["theta_interval"])
    def test_invalid(self):
        for kw in ({"replications":0},{"replications":501},
                   {"budget":100000,"replications":100},
                   {"batch":0},{"alpha":0},{"flip":.5}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
    def test_unknown_policy(self):
        st73=m.load("st73","m45-st73/adaptive_design.py")
        with self.assertRaises(ValueError):
            m.run_policy("unknown",[False]*20,[True]*20,2,20,5,.1,.3,st73)
if __name__=="__main__":unittest.main()
