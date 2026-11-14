import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("observer_estimation",Path(__file__).with_name("observer_estimation.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestObserverEstimation(unittest.TestCase):
    def test_born_covariance_and_fisher(self):
        for theta in (-1.0,-0.4,0,0.3,1.0):
            r=m.analyze(theta,500,42)
            self.assertLess(r["max_born_covariance_error"],1e-10)
            self.assertAlmostEqual(r["shared_born_probability"],(1+math.sin(theta))/2)
            self.assertAlmostEqual(r["quantum_fisher_information"],1)
            self.assertAlmostEqual(r["classical_fisher_information"],1)
            self.assertAlmostEqual(r["asymptotic_standard_error_per_observer"],1/math.sqrt(500))
    def test_reproducible(self):
        self.assertEqual(m.analyze(0.2,250,99),m.analyze(0.2,250,99))
    def test_estimates_not_forced_equal(self):
        r=m.analyze(0.3,1000,2026)
        self.assertEqual(r["estimate_disagreement"],
                         abs(r["a_observer"]["theta_estimate"]-r["b_observer"]["theta_estimate"]))
    def test_boundary_samples(self):
        self.assertAlmostEqual(m.estimate(0,10),-math.pi/2)
        self.assertAlmostEqual(m.estimate(10,10),math.pi/2)
    def test_invalid(self):
        for kwargs in ({"theta":math.pi/2},{"theta":float("nan")},
                       {"shots":0},{"shots":1.5},{"seed":-1}):
            with self.assertRaises(ValueError):m.analyze(**kwargs)
if __name__=="__main__":unittest.main()
