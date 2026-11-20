import unittest
from itertools import product
from angular_sync import *

class AngularTests(unittest.TestCase):
    def test_identity(self):
        for x,y,z in product((Q(1,5),Q(4,5),Q(1)),repeat=3):
            a,b=crossing_identity(x,y,z)
            self.assertEqual(a,b)
    def test_grid(self):
        for z in product((Q(4,5),Q(9,10),Q(1)),repeat=3):
            a,b=ratio_step(z)
            self.assertLessEqual(b,a)
            if a>1:self.assertLess(b,a)
    def test_diagonal(self):self.assertEqual(ratio_step((1,1,1)),(1,1))
    def test_signs(self):
        self.assertEqual(ratio_step((1,Q(-9,10),Q(-9,10))),ratio_step((1,Q(9,10),Q(9,10))))
    def test_invalid(self):
        with self.assertRaises(ValueError):ratio_step((1,0,0))
