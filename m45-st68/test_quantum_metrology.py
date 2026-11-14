import importlib.util
import math
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("quantum_metrology",Path(__file__).with_name("quantum_metrology.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestQuantumMetrology(unittest.TestCase):
    def test_optimal_binary_measurement(self):
        for theta in (-0.8,0,0.3,0.8):
            r=m.analyze(("1","1j","0","0"),theta)
            self.assertAlmostEqual(r["a_frame_quantum_fisher_information"],1)
            self.assertAlmostEqual(r["b_frame_quantum_fisher_information"],1)
            self.assertAlmostEqual(r["binary_relational_measurement"]["fisher_information"],1)
            self.assertAlmostEqual(r["single_copy_quantum_cramer_rao_variance_bound"],1)
    def test_generator_eigenstate_zero_qfi(self):
        r=m.analyze(("1","1","0","0"),0.2)
        self.assertAlmostEqual(r["a_frame_quantum_fisher_information"],0)
        self.assertIsNone(r["single_copy_quantum_cramer_rao_variance_bound"])
    def test_frame_invariance(self):
        for amplitudes in (("1","1j","0","0"),("1","0","1","0"),
                           ("1","1j","2","-1"),("1+2j","-3j","0.2","4")):
            for theta in (-1.2,0.1,1.1):
                r=m.analyze(amplitudes,theta)
                self.assertLess(r["max_frame_invariant_error"],1e-10)
                fi=r["binary_relational_measurement"]["fisher_information"]
                if fi is not None:
                    self.assertLessEqual(fi,r["a_frame_quantum_fisher_information"]+1e-10)
    def test_invalid(self):
        for kw in ({"amplitudes":("0","0","0","0")},
                   {"amplitudes":("1","2","3")},
                   {"theta":float("nan")},{"theta":float("inf")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
