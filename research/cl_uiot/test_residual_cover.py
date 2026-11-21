import unittest
from residual_cover import experiment
class ResidualTests(unittest.TestCase):
    def test_full_root(self):
        r=experiment(127,6,1)
        print("GRSEO full-root experiment:",r["used"],r["counts"],r["complete"])
        self.assertLessEqual(r["used"],127)
        self.assertEqual(r["counts"].get("unknown",0),len(r["unresolved"]))
        self.assertEqual(r["complete"],not r["unresolved"])
    def test_zero(self):
        r=experiment(0)
        self.assertFalse(r["complete"])
        self.assertEqual(r["counts"],{"unknown":1})
