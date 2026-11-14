import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("dynamical_broadcast",Path(__file__).with_name("dynamical_broadcast.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestDynamicBroadcast(unittest.TestCase):
    def test_perfect_records_and_partial_trace(self):
        r=m.analyze(4,0.5,math.pi/2)
        self.assertTrue(r["global_state_pure"])
        self.assertTrue(all(v["exact_sbs_for_observed_fragment"] for v in r["fragment_diagnostics"][1:4]))
        self.assertFalse(r["fragment_diagnostics"][4]["exact_sbs_for_observed_fragment"])
        self.assertFalse(r["fragment_diagnostics"][0]["exact_sbs_for_observed_fragment"])
        self.assertLess(r["system_reduced_coherence_l1"],1e-12)
    def test_no_interaction(self):
        r=m.analyze(4,0.5,0)
        self.assertAlmostEqual(r["system_reduced_coherence_l1"],1)
        self.assertFalse(any(v["exact_sbs_for_observed_fragment"] for v in r["fragment_diagnostics"]))
    def test_full_environment_retains_coherence(self):
        for n in (1,2,4,8):
            r=m.analyze(n,0.3,math.pi/2)
            self.assertAlmostEqual(r["fragment_diagnostics"][-1]["off_diagonal_block_trace_norm"],
                                   2*math.sqrt(0.3*0.7))
    def test_more_discarded_records_reduce_cross_block(self):
        r=m.analyze(8,0.5,math.pi/3)
        values=[v["off_diagonal_block_trace_norm"] for v in r["fragment_diagnostics"]]
        self.assertTrue(all(a<=b+1e-12 for a,b in zip(values,values[1:])))
        self.assertFalse(any(v["exact_sbs_for_observed_fragment"] for v in r["fragment_diagnostics"]))
    def test_system_coherence_reduces_with_n(self):
        a=m.analyze(1,0.5,math.pi/3)
        b=m.analyze(8,0.5,math.pi/3)
        self.assertGreater(a["system_reduced_coherence_l1"],b["system_reduced_coherence_l1"])
    def test_bad_inputs(self):
        for kw in ({"n":0},{"n":13},{"n":True},{"p":0},{"p":1},
                   {"theta":-0.1},{"theta":math.pi},{"theta":float("nan")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
