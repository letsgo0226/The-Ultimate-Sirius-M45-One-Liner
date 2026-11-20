import unittest
from itertools import product
from global_basin import *

class GlobalBasinTests(unittest.TestCase):
    def test_factor_order(self):
        for x,y,z in product((Q(1,5),Q(1,2),Q(9,10)),repeat=3):
            a,b,c=factors((x,y,z))
            self.assertEqual(4*(a-b),(y*y-x*x)*(5+x*x+y*y-5*z*z))
    def test_center(self):self.assertEqual(angular_step((Q(1,4),)*4)["status"],"central")
    def test_vertex(self):
        self.assertEqual(angular_step((1,0,0,0))["after"],1)
    def test_outside(self):
        r=angular_step((Q(9,10),Q(1,20),Q(1,25),Q(1,100)))
        self.assertEqual(r["status"],"outside")
    def test_zero(self):
        with self.assertRaises(ValueError):spread((0,1,1))
