import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("redundant_records",Path(__file__).with_name("redundant_records.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestRedundantRecords(unittest.TestCase):
    def test_perfect_records(self):
        r=m.analyze(12,0.5,0,0.1)
        self.assertAlmostEqual(r["pointer_entropy_bits"],1)
        self.assertAlmostEqual(r["fragment_information_bits"][0],0)
        self.assertTrue(all(abs(v-1)<1e-12 for v in r["fragment_information_bits"][1:]))
        self.assertEqual(r["minimum_fragment_size_for_target"],1)
        self.assertEqual(r["disjoint_fragment_redundancy_lower_bound"],12)
    def test_no_information_at_half_noise(self):
        r=m.analyze(12,0.5,0.5,0.1)
        self.assertTrue(all(abs(v)<1e-12 for v in r["fragment_information_bits"]))
        self.assertIsNone(r["minimum_fragment_size_for_target"])
    def test_information_monotonic(self):
        for q in (0,0.1,0.25,0.5):
            curve=m.analyze(16,0.3,q,0.1)["fragment_information_bits"]
            self.assertTrue(all(a<=b+1e-12 for a,b in zip(curve,curve[1:])))
    def test_no_entropy(self):
        r=m.analyze(8,0,0.1,0.1)
        self.assertEqual(r["pointer_entropy_bits"],0)
        self.assertIsNone(r["disjoint_fragment_redundancy_lower_bound"])
    def test_delta_one_not_spurious(self):
        r=m.analyze(8,0.5,0.5,1)
        self.assertIsNone(r["minimum_fragment_size_for_target"])
    def test_invalid(self):
        for kw in ({"n":0},{"n":65},{"p":-1},{"q":0.6},
                   {"delta":-0.1},{"p":float("nan")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
