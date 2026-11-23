import unittest
from fractions import Fraction as Q
from maxwell_3p1 import ETA
from second_order_bianchi_3p1 import divergence2,bianchi2_residual
from linearized_einstein_3p1 import einstein_linear
from tt_gravity_wave_3p1 import tt_wave

class SecondOrderBianchiTests(unittest.TestCase):
    def check_identity(self,h):
        for b in range(4):self.assertEqual(bianchi2_residual(h,b),{})
    def test_zero(self):
        self.check_identity([[{} for _ in range(4)] for _ in range(4)])
    def test_conformal_off_shell(self):
        h=[[{(3,0,0,0):Q(ETA[a])} if a==b else {} for b in range(4)] for a in range(4)]
        self.check_identity(h)
        self.assertTrue(any(divergence2(h,b) for b in range(4)))
    def test_general_off_shell(self):
        h=[[{} for _ in range(4)] for _ in range(4)]
        h[0][0]={(2,1,0,0):Q(2)}
        h[0][2]=h[2][0]={(1,0,2,0):Q(3)}
        h[3][3]={(0,1,0,2):Q(1)}
        self.check_identity(h)
    def test_tt_vacuum(self):
        h=tt_wave([0,0,2],[0,0,3])
        for a in range(4):
            for b in range(4):self.assertEqual(einstein_linear(h,a,b),{})
        for b in range(4):self.assertEqual(divergence2(h,b),{})
