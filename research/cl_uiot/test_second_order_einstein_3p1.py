import unittest
from fractions import Fraction as Q
from maxwell_3p1 import ETA,scale,add,mul
from second_order_einstein_3p1 import einstein2,ricci2
from tt_gravity_wave_3p1 import tt_wave
from linearized_einstein_3p1 import einstein_linear

class SecondOrderTests(unittest.TestCase):
    def test_zero(self):
        h=[[{} for _ in range(4)] for _ in range(4)]
        self.assertEqual(einstein2(h,0,0),{})
    def test_constant(self):
        h=tt_wave([2],[3])
        self.assertEqual(einstein2(h,0,0),{})
    def test_symmetry(self):
        h=tt_wave([0,0,2],[0,0,3])
        for a in range(4):
            for b in range(a):
                self.assertEqual(einstein2(h,a,b),einstein2(h,b,a))
    def test_quadratic_scaling(self):
        h=tt_wave([0,0,2],[0,0,3])
        hh=[[scale(p,3) for p in row] for row in h]
        self.assertEqual(einstein2(hh,0,0),scale(einstein2(h,0,0),9))
    def test_tt_affine(self):
        h=tt_wave([0,2],[])
        self.assertEqual(einstein2(h,0,0),{(0,0,0,0):Q(2)})
    def test_conformal_affine(self):
        # g=(1+2 eps t) eta; Omega=sqrt(1+2 eps t).
        h=[[{(1,0,0,0):Q(2*ETA[a])} if a==b else {} for b in range(4)] for a in range(4)]
        self.assertEqual(einstein2(h,0,0),{(0,0,0,0):Q(3)})
        self.assertEqual(einstein2(h,1,1),{(0,0,0,0):Q(3)})
