import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("regularize",Path(__file__).with_name("regularize.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestRegularization(unittest.TestCase):
    def test_normalization(self):
        report=m.experiment("@@@SKKS")
        self.assertEqual(report["conclusion"],"NORMAL_OBSERVED")
        self.assertEqual(report["observed_normal_form"],"S")
        self.assertTrue(m.verify(report))
    def test_budget_is_not_halting_oracle(self):
        report=m.experiment("@@@SKKS",(0,1))
        self.assertEqual(report["conclusion"],"UNRESOLVED_WITHIN_TESTED_BUDGETS")
        self.assertTrue(m.verify(report))
    def test_tape_cap(self):
        r=m.evaluate("@@@SKKS",8,1)
        self.assertEqual(r["status"],"CAP_EXCEEDED")
    def test_tamper(self):
        report=m.experiment("@@@SKKS")
        report["runs"][-1]["result"]="K"
        self.assertFalse(m.verify(report))
    def test_invalid_budget(self):
        with self.assertRaises(ValueError):
            m.evaluate("S",-1)
if __name__=="__main__":
    unittest.main()
