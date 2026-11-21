import unittest
from fractions import Fraction as Q
from qec_minimum_resources import plan,mission_plan
from qec_concatenated_5qubit import iterate

class ResourceTests(unittest.TestCase):
    def test_no_encoding(self):
        self.assertEqual(plan(Q(1,100),Q(1,10),1)["depth"],0)
    def test_minimum(self):
        p,e=Q(1,20),Q(1,10000)
        r=plan(p,e,625)
        self.assertTrue(r["certified"])
        self.assertLessEqual(iterate(p,r["depth"]),e)
        self.assertGreater(iterate(p,r["depth"]-1),e)
        self.assertEqual(r["data_qubits"],5**r["depth"])
    def test_budget(self):
        self.assertFalse(plan(Q(1,20),Q(1,10000),24)["certified"])
    def test_zero(self):
        self.assertTrue(plan(0,Q(1,1000000),1)["certified"])
    def test_noncontraction(self):
        self.assertFalse(plan(1,Q(1,10),625)["certified"])
    def test_mission(self):
        self.assertEqual(mission_plan(Q(1,20),Q(1,100),100,625),plan(Q(1,20),Q(1,10000),625))
    def test_invalid(self):
        with self.assertRaises(ValueError):plan(0,0,1)
