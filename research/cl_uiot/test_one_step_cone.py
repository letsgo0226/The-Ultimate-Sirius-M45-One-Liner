import unittest
from one_step_cone import prove
class OneStepTests(unittest.TestCase):
    def test_cover(self):
        self.assertEqual(prove(),(True,831,26,None))
    def test_insufficient(self):
        self.assertFalse(prove(0)[0])
    def test_invalid(self):
        with self.assertRaises(ValueError):prove(-1)
