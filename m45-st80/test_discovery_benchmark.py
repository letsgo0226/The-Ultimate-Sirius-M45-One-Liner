import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st80",Path(__file__).with_name("discovery_benchmark.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestDiscoveryBenchmark(unittest.TestCase):
    def test_summary(self):
        s=m.summarize([1,2,3,4])
        self.assertAlmostEqual(s["mean"],2.5)
        self.assertEqual(len(s["normal_approx_95pct_ci"]),2)
    def test_reproducible(self):
        a=m.benchmark(replicates=2,shots=4,seed=19)
        self.assertEqual(a,m.benchmark(replicates=2,shots=4,seed=19))
        self.assertEqual(set(a["scenario_results"]),set(m.SCENARIOS))
        for scenario,report in a["scenario_results"].items():
            self.assertEqual(len(report["replicate_results"]),2)
            self.assertEqual(sum(report["selected_model_counts"].values()),2)
            self.assertTrue(math.isfinite(report["paired_gain_summary"]["mean"]))
            for row in report["replicate_results"]:
                self.assertAlmostEqual(row["paired_gain"],
                    row["evolved_locked_log_score"]-row["fixed_locked_log_score"])
    def test_invalid(self):
        for kw in ({"replicates":1},{"replicates":101},{"shots":0},
                   {"shots":201},{"seed":-1},{"complexity_penalty":-1},
                   {"complexity_penalty":float("nan")}):
            with self.subTest(kw=kw):
                with self.assertRaises(ValueError):m.benchmark(**kw)
if __name__=="__main__":unittest.main()
