import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("frame_switch",Path(__file__).with_name("frame_switch.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestFrameSwitch(unittest.TestCase):
    def test_invariants(self):
        for amplitudes in (("1","1j","2","-1"),("1","0","0","0"),
                           ("0","0","1","0"),("1","1","1","1"),
                           ("1+2j","-3j","0.2","4")):
            for phase in (0,0.5,3.14159):
                with self.subTest(amplitudes=amplitudes,phase=phase):
                    r=m.analyze(amplitudes,phase)
                    self.assertLess(r["max_frame_invariant_error"],1e-10)
    def test_permutation_involution(self):
        a=m.normalize(("1","2","3","4"))
        self.assertEqual(m.switch_a_to_b(m.switch_a_to_b(a)),a)
    def test_lift_is_symmetric(self):
        a=m.normalize(("1","1j","0","-1"))
        full=m.lift_to_three_qubits(a)
        self.assertAlmostEqual(sum(abs(z)**2 for z in full),1)
        for i in range(8):self.assertAlmostEqual(abs(full[i]-full[i^7]),0)
    def test_frame_coordinate_changes(self):
        a=m.normalize(("1","2","3","4"))
        b=m.switch_a_to_b(a)
        self.assertNotEqual(a,b)
        self.assertAlmostEqual(m.probability_equal_b_c(a,"A"),
                               m.probability_equal_b_c(b,"B"))
    def test_bad_inputs(self):
        for kw in ({"amplitudes":("0","0","0","0")},
                   {"amplitudes":("1","2","3")},
                   {"amplitudes":("1","nan","0","0")},
                   {"phase":float("nan")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
