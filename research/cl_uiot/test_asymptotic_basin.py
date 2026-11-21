import unittest
from asymptotic_basin import *
class CompletenessTests(unittest.TestCase):
    def test_schedule(self):
        self.assertEqual(schedule(3),{"budget":15,"depth":3,"cap":3,"digits":4})
    def test_root(self):
        self.assertTrue(verify(stage(0)))
    def test_uniform(self):
        r=stage(2,((Q(24,100),Q(26,100)),)*4)
        self.assertEqual(r["leaves"][0][2],"uniform")
    def test_bound(self):
        self.assertEqual(error_bound(Q(1,100),1,3),Q(5120,100)+Q(1,1000))
    def test_zero(self):
        self.assertEqual(error_bound(Q(1,7),0,1),Q(1,7))
    def test_invalid(self):
        with self.assertRaises(ValueError):schedule(-1)
