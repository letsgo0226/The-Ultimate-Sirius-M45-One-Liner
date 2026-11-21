import unittest
from itertools import product
from cross_critical import *
class CrossCriticalTests(unittest.TestCase):
    def test_grid(self):
        count=0
        for z in product((Q(0),Q(1,2),Q(2,3),Q(4,5),Q(5,6)),repeat=3):
            try:r=deficit(z)
            except ValueError:continue
            self.assertLessEqual(r["next_maximum"],r["upper"])
            count+=1
        self.assertGreater(count,0)
    def test_diagonal(self):
        r=deficit((Q(5,6),)*3)
        self.assertEqual(r["upper"],r["next_maximum"])
    def test_weak(self):
        self.assertTrue(deficit((Q(5,6),Q(1,2),Q(1,2)))["central_basin"])
    def test_signs(self):
        a,b=Q(5,6),Q(2,3)
        self.assertEqual(deficit((a,b,b)),deficit((a,-b,-b)))
    def test_invalid(self):
        with self.assertRaises(ValueError):deficit((1,1,1))
