import unittest
from fractions import Fraction as Q
from second_order_gauge_3p1 import transform,covariance_residual,equation
from tt_gravity_wave_3p1 import tt_wave
from tt_backreaction_3p1 import correction

def zero():
    return [[{} for _ in range(4)] for _ in range(4)]

class SecondOrderGaugeTests(unittest.TestCase):
    def setUp(self):
        self.X=[{(2,0,0,0):Q(1)}, {(1,1,0,0):Q(2)}, {}, {}]
    def test_zero_generator(self):
        h=tt_wave([0,1],[])
        self.assertEqual(transform([{}, {}, {}, {}],h,zero()),(h,zero()))
    def test_pure_gauge(self):
        h,j=transform(self.X,zero(),zero())
        self.assertEqual(equation(h,j),zero())
    def test_off_shell(self):
        h=zero()
        h[0][0]={(0,3,0,0):Q(2)}
        self.assertEqual(covariance_residual(self.X,h,zero()),zero())
    def test_tt_solution(self):
        p,c=[0,2],[0,0,1]
        h,j=transform(self.X,tt_wave(p,c),correction(p,c))
        self.assertEqual(equation(h,j),zero())
