import unittest
from fractions import Fraction as Q
from tt_backreaction_3p1 import correction,residual
from tt_gravity_wave_3p1 import profile

class TTBackreactionTests(unittest.TestCase):
    def check_wave(self,p,c):
        for a in range(4):
            for b in range(4):
                self.assertEqual(residual(p,c,a,b),{})
    def test_zero(self):
        self.check_wave([],[])
    def test_affine_plus(self):
        self.check_wave([0,2],[])
        self.assertEqual(correction([0,2],[])[1][1],profile([0,0,-1]))
    def test_cross(self):
        self.check_wave([],[1,2,3])
    def test_mixed(self):
        self.check_wave([1,2,3],[2,0,0,4])
    def test_constant(self):
        self.assertEqual(correction([2],[3]),[[{} for _ in range(4)] for _ in range(4)])
