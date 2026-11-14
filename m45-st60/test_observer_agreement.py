import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("observer_agreement",Path(__file__).with_name("observer_agreement.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestObserverAgreement(unittest.TestCase):
    def test_perfect_records(self):
        r=m.analyze(24,3,0.5,0)
        self.assertEqual(r["observer_count"],8)
        self.assertEqual(r["per_observer_majority_error"],0)
        self.assertEqual(r["pairwise_agreement_probability"],1)
        self.assertEqual(r["all_observers_correct_probability"],1)
        self.assertTrue(r["criteria"]["operational_objectivity"])
    def test_random_records_agreement_not_truth(self):
        r=m.analyze(24,3,0.5,0.5)
        self.assertAlmostEqual(r["per_observer_truth_accuracy"],0.5)
        self.assertAlmostEqual(r["pairwise_agreement_probability"],0.5)
        self.assertFalse(r["criteria"]["operational_objectivity"])
    def test_majority_reduces_error(self):
        a=m.analyze(30,1,0.5,0.1)
        b=m.analyze(30,5,0.5,0.1)
        self.assertGreater(a["per_observer_majority_error"],b["per_observer_majority_error"])
    def test_unanimity_distinct_from_correctness(self):
        r=m.analyze(12,3,0.5,0.2)
        self.assertGreater(r["unanimous_agreement_probability"],r["all_observers_correct_probability"])
    def test_prior_does_not_change_symmetric_accuracy(self):
        a=m.analyze(24,3,0.1,0.2)
        b=m.analyze(24,3,0.9,0.2)
        self.assertEqual(a["per_observer_truth_accuracy"],b["per_observer_truth_accuracy"])
    def test_invalid(self):
        for kw in ({"n":1},{"n":129},{"m":2},{"m":13},{"q":0.7},
                   {"accuracy_threshold":-1},{"agreement_threshold":float("nan")}):
            with self.assertRaises(ValueError):m.analyze(**kw)
if __name__=="__main__":unittest.main()
