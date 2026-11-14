import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("relational_entanglement",Path(__file__).with_name("relational_entanglement.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestRelationalEntanglement(unittest.TestCase):
    def test_product_becomes_bell_in_other_factorization(self):
        r=m.analyze(("1","0","1","0"))
        self.assertAlmostEqual(r["a_frame_concurrence"],0)
        self.assertAlmostEqual(r["b_frame_concurrence"],1)
        self.assertAlmostEqual(r["a_frame_entanglement_entropy_bits"],0)
        self.assertAlmostEqual(r["b_frame_entanglement_entropy_bits"],1)
        self.assertAlmostEqual(r["reference_invariant_b_equals_c_probability"],0.5)
    def test_bell_becomes_product(self):
        r=m.analyze(("1","0","0","1"))
        self.assertAlmostEqual(r["a_frame_concurrence"],1)
        self.assertAlmostEqual(r["b_frame_concurrence"],0)
    def test_computational_basis_is_product_in_both(self):
        for k in range(4):
            amps=tuple("1" if i==k else "0" for i in range(4))
            r=m.analyze(amps)
            self.assertAlmostEqual(r["a_frame_concurrence"],0)
            self.assertAlmostEqual(r["b_frame_concurrence"],0)
    def test_complex_cases_and_invariants(self):
        for amps in (("1","1j","2","-1"),("1+2j","-3j","0.2","4"),
                     ("1","1","1","1")):
            r=m.analyze(amps)
            self.assertLess(r["max_frame_invariant_error"],1e-10)
            for name in ("a_frame_entanglement_entropy_bits","b_frame_entanglement_entropy_bits"):
                self.assertGreaterEqual(r[name],0)
                self.assertLessEqual(r[name],1)
    def test_invalid(self):
        for amps in (("0","0","0","0"),("1","2","3"),("1","nan","0","0")):
            with self.assertRaises(ValueError):m.analyze(amps)
if __name__=="__main__":unittest.main()
