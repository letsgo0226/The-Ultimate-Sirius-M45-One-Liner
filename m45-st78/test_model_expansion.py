import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st78",Path(__file__).with_name("model_expansion.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestModelExpansion(unittest.TestCase):
    def test_candidate_sizes(self):
        g=m.grid()
        self.assertEqual(len(g["stationary"]),125)
        self.assertEqual(len(g["science_drift"]),625)
    def test_phase_drift_only_in_science(self):
        h=(.55,.05,.2,.3)
        self.assertEqual(m.probability(h,"reference_zero","early"),
                         m.probability(h,"reference_zero","late"))
        self.assertEqual(m.probability(h,"reference_one","early"),
                         m.probability(h,"reference_one","late"))
        self.assertAlmostEqual(m.probability(h,"science","late")-
                               m.probability(h,"science","early"),.3)
    def test_posterior_and_score(self):
        g=m.grid()["stationary"]
        obs=[("reference_zero","early",1,10),("science","late",6,10)]
        w=m.posterior(g,obs)
        self.assertAlmostEqual(sum(w),1)
        self.assertTrue(math.isfinite(m.predictive_log_score(g,w,obs)))
    def test_reproducible_and_locked_test(self):
        a=m.analyze(shots=8,seed=17)
        self.assertEqual(a,m.analyze(shots=8,seed=17))
        self.assertIn(a["selected_model_by_validation"],m.grid())
        self.assertAlmostEqual(a["locked_test_selected_model_score"],
             a["locked_test_mean_log_scores"][a["selected_model_by_validation"]])
    def test_invalid(self):
        for kw in ({"theta":math.pi/2},{"q01":.5},{"q10":-.1},
                   {"drift":.6},{"shots":0},{"shots":201},{"seed":-1}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
