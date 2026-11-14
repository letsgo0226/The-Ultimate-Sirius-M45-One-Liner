import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("environment",Path(__file__).with_name("environment.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestEnvironment(unittest.TestCase):
    def test_no_interaction_pure_system(self):
        r=m.analyze(0.5,0)
        self.assertAlmostEqual(r["reduced_purity"],1)
        self.assertAlmostEqual(r["reduced_von_neumann_entropy_bits"],0)
        self.assertAlmostEqual(r["reduced_coherence_l1"],1)
    def test_orthogonal_environment_records(self):
        r=m.analyze(0.5,math.pi/2)
        self.assertAlmostEqual(r["reduced_purity"],0.5)
        self.assertAlmostEqual(r["reduced_von_neumann_entropy_bits"],1)
        self.assertAlmostEqual(r["reduced_coherence_l1"],0,places=12)
        self.assertEqual(r["joint_purity"],1)
    def test_intermediate(self):
        for p in (0,0.1,0.5,0.9,1):
            for theta in (0,math.pi/6,math.pi/4,math.pi/2):
                with self.subTest(p=p,theta=theta):
                    r=m.analyze(p,theta)
                    self.assertLess(r["max_error_vs_st49_phase_damping"],1e-12)
                    self.assertAlmostEqual(sum(r["reduced_density_matrix"][i][i] for i in range(2)),1)
                    self.assertGreaterEqual(r["reduced_purity"],0.5-1e-12)
                    self.assertLessEqual(r["reduced_purity"],1+1e-12)
    def test_monotonic_coherence_for_balanced_state(self):
        values=[m.analyze(0.5,t)["reduced_coherence_l1"] for t in (0,0.2,0.7,math.pi/2)]
        self.assertEqual(values,sorted(values,reverse=True))
    def test_invalid(self):
        for p,theta in ((-1,0),(2,0),(0.5,-0.1),(0.5,math.pi),
                        (float("nan"),0),(0.5,float("inf"))):
            with self.assertRaises(ValueError):m.analyze(p,theta)
if __name__=="__main__":unittest.main()
