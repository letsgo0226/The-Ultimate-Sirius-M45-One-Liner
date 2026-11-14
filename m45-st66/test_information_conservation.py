import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("information_conservation",Path(__file__).with_name("information_conservation.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestInformationConservation(unittest.TestCase):
    def test_product_to_bell_information_redistribution(self):
        r=m.analyze(("1","0","1","0"))
        a,b=r["a_frame"],r["b_frame"]
        self.assertAlmostEqual(a["global_purity"],1)
        self.assertAlmostEqual(b["global_purity"],1)
        self.assertAlmostEqual(a["first_subsystem_entropy_bits"],0)
        self.assertAlmostEqual(a["second_subsystem_entropy_bits"],0)
        self.assertAlmostEqual(b["first_subsystem_entropy_bits"],1)
        self.assertAlmostEqual(b["second_subsystem_entropy_bits"],1)
        self.assertAlmostEqual(r["subsystem_mutual_information_change_bits"],2)
        self.assertAlmostEqual(r["invariant_relational_b_equals_c_probability"],0.5)
    def test_reverse(self):
        r=m.analyze(("1","0","0","1"))
        self.assertAlmostEqual(r["subsystem_mutual_information_change_bits"],-2)
    def test_pure_product_basis(self):
        for i in range(4):
            amps=tuple("1" if j==i else "0" for j in range(4))
            r=m.analyze(amps)
            self.assertAlmostEqual(r["subsystem_mutual_information_change_bits"],0)
            self.assertLess(r["max_invariant_error"],1e-10)
    def test_complex_amplitudes(self):
        for amps in (("1","1j","2","-1"),("1+2j","-3j","0.2","4"),
                     ("1","1","1","1")):
            r=m.analyze(amps)
            self.assertLess(r["max_invariant_error"],1e-10)
            for f in ("a_frame","b_frame"):
                self.assertAlmostEqual(r[f]["global_purity"],1)
                self.assertAlmostEqual(r[f]["global_entropy_bits"],0)
                self.assertAlmostEqual(r[f]["first_subsystem_entropy_bits"],
                                       r[f]["second_subsystem_entropy_bits"])
    def test_invalid(self):
        for amps in (("0","0","0","0"),("1","2","3"),("1","nan","0","0")):
            with self.assertRaises(ValueError):m.analyze(amps)
if __name__=="__main__":unittest.main()
