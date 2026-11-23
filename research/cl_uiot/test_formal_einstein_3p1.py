import unittest
from fractions import Fraction as Q
from maxwell_3p1 import ETA,add
from formal_einstein_3p1 import coefficients
from linearized_einstein_3p1 import einstein_linear
from second_order_einstein_3p1 import einstein2
from tt_gravity_wave_3p1 import tt_wave
from tt_backreaction_3p1 import correction

def zero():return [[{} for _ in range(4)] for _ in range(4)]

class FormalEinsteinTests(unittest.TestCase):
    def test_flat(self):
        self.assertEqual(coefficients([]),[zero()])
    def test_lower_orders(self):
        h=tt_wave([0,2],[0,0,1])
        G=coefficients([h,zero(),zero()])
        for a in range(4):
            for b in range(4):
                self.assertEqual(G[1][a][b],einstein_linear(h,a,b))
                self.assertEqual(G[2][a][b],einstein2(h,a,b))
    def test_backreaction(self):
        p,c=[0,2],[0,0,1]
        G=coefficients([tt_wave(p,c),correction(p,c)])
        self.assertEqual(G,[zero(),zero(),zero()])
    def test_conformal_third_order(self):
        h=[[{(1,0,0,0):Q(2*ETA[a])} if a==b else {} for b in range(4)] for a in range(4)]
        G=coefficients([h,zero(),zero()])
        self.assertEqual(G[3][0][0],{(1,0,0,0):Q(-12)})
    def test_fourth_order(self):
        h=[[{(1,0,0,0):Q(2*ETA[a])} if a==b else {} for b in range(4)] for a in range(4)]
        self.assertEqual(coefficients([h,zero(),zero(),zero()])[4][0][0],{(2,0,0,0):Q(36)})
