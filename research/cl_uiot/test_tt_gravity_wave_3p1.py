import unittest
from fractions import Fraction as Q
from tt_gravity_wave_3p1 import tt_wave,tidal,demo
from linearized_einstein_3p1 import trace,box,gauge_shift,einstein_linear
from harmonic_linearized_gravity_3p1 import harmonic_constraint
from maxwell_3p1 import add

class TTWaveTests(unittest.TestCase):
    def setUp(self):
        self.h=tt_wave([0,0,2],[0,0,0,3])
    def test_trace(self):
        self.assertEqual(trace(self.h),{})
    def test_harmonic(self):
        for i in range(4):self.assertEqual(harmonic_constraint(self.h,i),{})
    def test_wave(self):
        for row in self.h:
            for p in row:self.assertEqual(box(p),{})
    def test_vacuum(self):
        for i in range(4):
            for j in range(4):self.assertEqual(einstein_linear(self.h,i,j),{})
    def test_plus_tidal(self):
        self.assertEqual(tidal(self.h,1,1),{(0,0,0,0):Q(-2)})
        self.assertEqual(tidal(self.h,2,2),{(0,0,0,0):Q(2)})
    def test_cross_tidal(self):
        self.assertEqual(tidal(tt_wave([],[0,0,3]),1,2),{(0,0,0,0):Q(-3)})
    def test_pure_gauge(self):
        xi=[{(2,1,0,0):Q(3)}, {}, {(3,0,0,0):Q(2)}, {}]
        g=gauge_shift(xi)
        for i in range(1,4):
            for j in range(1,4):
                self.assertEqual(tidal(g,i,j),{})
                shifted=[[add(self.h[a][b],g[a][b]) for b in range(4)] for a in range(4)]
                self.assertEqual(tidal(shifted,i,j),tidal(self.h,i,j))
    def test_demo(self):
        self.assertTrue(demo()["vacuum"])
        self.assertTrue(demo()["nonzero_tidal_curvature"])
