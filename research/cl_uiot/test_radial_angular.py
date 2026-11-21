import unittest
from itertools import product
from radial_angular import *

class RadialAngularTests(unittest.TestCase):
    def test_diagonal(self):
        for a in (Q(4,5),Q(9,10),Q(1)):
            r=radial((a,a,a))
            self.assertEqual(r["next_mean"],scalar(a))
            self.assertEqual(r["error"],0)
    def test_grid(self):
        for z in product((Q(4,5),Q(9,10),Q(1)),repeat=3):
            try:from_bloch(*z)
            except ValueError:continue
            r=radial(z)
            self.assertLessEqual(r["lower"],r["next_mean"])
            self.assertLessEqual(r["next_mean"],r["upper"])
    def test_drift(self):
        self.assertLess(drift(Q(4,5)),0)
        self.assertGreater(drift(Q(9,10)),0)
        self.assertEqual(drift(1),0)
    def test_signs(self):
        self.assertEqual(radial((Q(9,10),)*3),radial((Q(9,10),Q(-9,10),Q(-9,10))))
    def test_invalid(self):
        with self.assertRaises(ValueError):radial((0,0,0))
