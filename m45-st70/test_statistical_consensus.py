import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("statistical_consensus",Path(__file__).with_name("statistical_consensus.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestStatisticalConsensus(unittest.TestCase):
    def test_deterministic_reproducibility(self):
        self.assertEqual(m.analyze(),m.analyze())
    def test_shared_born_and_noise_model(self):
        for theta,flip in ((0,0),(.3,.05),(-.5,.2)):
            r=m.analyze(theta=theta,observers=3,shots=300,flip=flip,seed=99)
            p=(1+math.sin(theta))/2
            self.assertAlmostEqual(r["shared_ideal_born_probability"],p)
            self.assertAlmostEqual(r["shared_noisy_born_probability"],flip+(1-2*flip)*p)
            self.assertAlmostEqual(r["simultaneous_coverage_guarantee_at_least"],.95)
    def test_simultaneous_intersection(self):
        r=m.analyze(theta=.3,observers=4,shots=1000,flip=.05,seed=2026)
        intervals=[x["simultaneous_theta_interval"] for x in r["observer_reports"]]
        expected_lower=max(x[0] for x in intervals)
        expected_upper=min(x[1] for x in intervals)
        expected=[expected_lower,expected_upper] if expected_lower<=expected_upper else None
        self.assertEqual(r["consensus_interval_intersection"],expected)
        self.assertTrue(all(-math.pi/2<=x[0]<=x[1]<=math.pi/2 for x in intervals))
    def test_zero_flip_and_clipping(self):
        self.assertEqual(m.p_interval(0,10,0,0),(0,0))
        self.assertEqual(m.p_interval(10,10,0,0),(1,1))
        self.assertEqual(m.p_interval(0,10,.1,0),(0,0))
        self.assertEqual(m.p_interval(10,10,.1,0),(1,1))
    def test_invalid(self):
        bad=({"theta":math.pi/2},{"theta":float("nan")},{"observers":1},
             {"observers":True},{"shots":0},{"flip":.5},{"flip":-.1},
             {"alpha":0},{"alpha":1},{"seed":-1},
             {"observers":100,"shots":100001})
        for kwargs in bad:
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):m.analyze(**kwargs)
if __name__=="__main__":unittest.main()
