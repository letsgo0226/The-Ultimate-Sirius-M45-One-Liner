import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("invariants",Path(__file__).with_name("invariants.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestInvariants(unittest.TestCase):
    def test_invariant_z_and_macro(self):
        r=m.report(32,0.7,0,1)
        self.assertTrue(all(r["invariants"].values()))
        self.assertTrue(all(r["context_dependent"].values()))
        self.assertAlmostEqual(r["z_plus"][0],r["z_plus"][1])
        self.assertNotAlmostEqual(r["x_plus"][0],r["x_plus"][1])
    def test_equal_gamma_no_change(self):
        r=m.report(9,0.7,0.4,0.4)
        self.assertTrue(all(r["invariants"].values()))
        self.assertFalse(any(r["context_dependent"].values()))
    def test_z_eigenstate(self):
        r=m.report(7,1,0,1)
        self.assertFalse(any(r["context_dependent"].values()))
        self.assertTrue(all(r["invariants"].values()))
    def test_reject_bad(self):
        for args in ((0,0.7,0,1),(4,-1,0,1),(4,0.5,-1,1),(4,0.5,0,float("nan"))):
            with self.assertRaises(ValueError):m.report(*args)
if __name__=="__main__":unittest.main()
