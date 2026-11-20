import unittest
from itertools import product
from supercritical_rigidity import *

class RigidityTests(unittest.TestCase):
    def test_ceiling(self):
        self.assertLess(ceiling()**2,Q(2,3))
    def test_witness(self):
        self.assertTrue(certificate((Q(5,6),Q(2,3),Q(2,3)))["central_basin"])
    def test_grid(self):
        count=0
        for z in product((Q(0),Q(1,2),Q(2,3),Q(3,4),Q(5,6)),repeat=3):
            try:r=certificate(z)
            except ValueError:continue
            self.assertLessEqual(r["next_maximum"],r["upper"])
            count+=1
        self.assertGreater(count,0)
    def test_signs(self):
        self.assertEqual(certificate((Q(5,6),Q(2,3),Q(2,3))),certificate((Q(5,6),Q(-2,3),Q(-2,3))))
    def test_invalid(self):
        with self.assertRaises(ValueError):certificate((1,1,1))
