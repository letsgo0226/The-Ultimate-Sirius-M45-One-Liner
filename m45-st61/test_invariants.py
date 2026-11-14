import importlib.util
import itertools
import unittest
from fractions import Fraction
from pathlib import Path
spec=importlib.util.spec_from_file_location("invariants",Path(__file__).with_name("invariants.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestObserverInvariants(unittest.TestCase):
    def test_frame_covariance(self):
        for n in range(6):
            for letters in itertools.product("HZ",repeat=n):
                for axis in ("X","Z"):
                    with self.subTest(word="".join(letters),axis=axis):
                        r=m.analyze("3/5","4/5","".join(letters),axis,"1/10")
                        self.assertTrue(r["covariant_probability_equal"])
                        self.assertEqual(r["frame_invariant_purity"],"1")
                        self.assertEqual(r["frame_invariant_determinant"],"0")
    def test_mixed_state_invariants(self):
        for word in ("","H","Z","HZ","ZHHZ"):
            r=m.analyze("1/5","2/5",word,"X","1/4")
            self.assertEqual(r["frame_invariant_purity"],str(Fraction(3,5)))
            self.assertEqual(r["frame_invariant_determinant"],str(Fraction(1,5)))
            self.assertEqual(r["calibrated_expectation"],"1/5")
    def test_noise_at_half_is_unidentifiable(self):
        with self.assertRaises(ValueError):m.analyze(flip="1/2")
    def test_invalid(self):
        for kw in ({"x":"1","z":"1"},{"word":"Q"},{"axis":"Y"},
                   {"flip":"-1/10"},{"flip":"1/2"},{"x":"not-number"},
                   {"x":"1000001"},{"word":"H"*65}):
            with self.assertRaises(ValueError):m.analyze(**kw)
    def test_noncommuting_word_actions(self):
        self.assertNotEqual(m.operator("HZ"),m.operator("ZH"))
if __name__=="__main__":unittest.main()
