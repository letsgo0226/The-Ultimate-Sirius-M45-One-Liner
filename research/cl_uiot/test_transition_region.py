import unittest
from itertools import product
from transition_region import *
class TransitionTests(unittest.TestCase):
    def test_grid(self):
        for z in product(range(-5,6),repeat=3):
            z=tuple(Q(x,5) for x in z)
            try:maximum(z)
            except ValueError:continue
            r=compare(z)
            self.assertLessEqual(r["next_maximum"],r["upper"])
    def test_diagonal(self):
        for m in (Q(1,2),Q(4,5),Q(9,10),Q(1)):
            r=compare((m,)*3)
            self.assertEqual(r["next_maximum"],r["upper"])
    def test_extended(self):
        z=(Q(4,5),)*3
        self.assertTrue(compare(z)["central_basin"])
        self.assertLess(contraction(z),1)
    def test_axis(self):self.assertEqual(compare((1,0,0))["next_maximum"],Q(1,4))
    def test_invalid(self):
        with self.assertRaises(ValueError):contraction((1,1,1))
        with self.assertRaises(ValueError):maximum((1,1,0))
