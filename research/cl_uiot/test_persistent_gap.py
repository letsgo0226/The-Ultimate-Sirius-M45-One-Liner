import unittest
from itertools import product
from persistent_gap import *
class GapTests(unittest.TestCase):
    def test_extended_region(self):
        z=(Q(4,5),Q(7,10),Q(7,10))
        self.assertTrue(cone(z))
        self.assertLess(certificate(z)[1],certificate(z)[0])
    def test_grid(self):
        count=0
        for z in product((Q(1,2),Q(7,10),Q(4,5),Q(9,10),Q(1)),repeat=3):
            try:
                if not cone(z):continue
            except ValueError:continue
            r,s=certificate(z)
            self.assertLessEqual(s,r)
            count+=1
        self.assertGreater(count,0)
    def test_diagonal(self):self.assertEqual(certificate((Q(4,5),)*3),(1,1))
    def test_signs(self):
        z=(Q(4,5),Q(7,10),Q(7,10))
        self.assertEqual(certificate(z),certificate((z[0],-z[1],-z[2])))
    def test_invalid(self):
        with self.assertRaises(ValueError):certificate((1,0,0))
