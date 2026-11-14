import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st79",Path(__file__).with_name("model_evolution.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestModelEvolution(unittest.TestCase):
    def test_grid_sizes(self):
        g=m.candidates()
        self.assertEqual(len(g),4)
        self.assertEqual(len(g["stationary"]),125)
        for name in g:
            if name!="stationary":
                self.assertEqual(len(g[name]),625)
    def test_mutation_locality(self):
        base=(.55,.05,.15,0.,0.,0.)
        variants={"science_drift":(.55,.05,.15,.3,0.,0.),
                  "reference_zero_drift":(.55,.05,.15,0.,.3,0.),
                  "reference_one_drift":(.55,.05,.15,0.,0.,.3)}
        for name,h in variants.items():
            for action in m.ACTIONS:
                delta=m.probability(h,action,"late")-m.probability(base,action,"late")
                self.assertAlmostEqual(delta,.3 if action==name.replace("_drift","") else 0.)
    def test_reproducible_and_test_locked(self):
        r=m.analyze(shots=8,seed=17)
        self.assertEqual(r,m.analyze(shots=8,seed=17))
        self.assertFalse(r["test_used_for_selection"])
        self.assertEqual(len(r["validation_selection_audit"]),4)
        self.assertEqual(sum(x["selected"] for x in r["validation_selection_audit"]),1)
        self.assertTrue(math.isfinite(r["locked_test_selected_model_mean_log_score"]))
    def test_invalid(self):
        for kw in ({"theta":math.pi/2},{"q01":.5},{"q10":-.1},
                   {"late_science_drift":.6},{"shots":0},{"shots":201},
                   {"complexity_penalty":-1},{"complexity_penalty":float("nan")}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
