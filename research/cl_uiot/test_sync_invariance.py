import unittest
from itertools import product
from sync_invariance import *
class InvarianceTests(unittest.TestCase):
    def test_subcritical(self):
        z=(Q(4,5),Q(3,5),Q(3,5))
        self.assertEqual(region(z),"subcritical")
        self.assertTrue(cone(invariant_step(z)))
    def test_ratio(self):
        z=(Q(9,10),Q(4,5),Q(4,5))
        self.assertEqual(region(z),"ratio")
        self.assertTrue(cone(invariant_step(z)))
    def test_vertex(self):self.assertEqual(invariant_step((1,1,1)),(1,1,1))
    def test_grid(self):
        count=0
        for z in product((Q(1,2),Q(3,5),Q(4,5),Q(9,10),Q(1)),repeat=3):
            try:r=region(z)
            except ValueError:continue
            if r is None:continue
            self.assertIsNotNone(region(invariant_step(z)))
            count+=1
        self.assertGreater(count,0)
    def test_outside(self):
        with self.assertRaises(ValueError):invariant_step((1,0,0))
