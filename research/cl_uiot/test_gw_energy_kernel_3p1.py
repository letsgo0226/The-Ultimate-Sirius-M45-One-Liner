import unittest
from fractions import Fraction as Q
from maxwell_3p1 import scale
from tt_gravity_wave_3p1 import tt_wave
from gw_energy_kernel_3p1 import kernel,trace_kernel,divergence,demo

class GWEnergyKernelTests(unittest.TestCase):
    def test_linear_plus(self):
        h=tt_wave([0,2],[])
        self.assertEqual(kernel(h,0,0),{(0,0,0,0):Q(8)})
    def test_cross(self):
        h=tt_wave([],[0,3])
        self.assertEqual(kernel(h,0,0),{(0,0,0,0):Q(18)})
    def test_flux(self):
        h=tt_wave([0,0,2],[0,0,3])
        self.assertEqual(kernel(h,0,3),scale(kernel(h,0,0),-1))
        self.assertEqual(kernel(h,3,3),kernel(h,0,0))
    def test_transverse(self):
        h=tt_wave([0,0,2],[0,0,3])
        for a in (1,2):
            for b in range(4):self.assertEqual(kernel(h,a,b),{})
    def test_null_and_conserved(self):
        for n in range(5):
            h=tt_wave([0]*n+[2],[0]*n+[3])
            self.assertEqual(trace_kernel(h),{})
            for b in range(4):self.assertEqual(divergence(h,b),{})
    def test_constant(self):
        self.assertEqual(kernel(tt_wave([2],[3]),0,0),{})
    def test_demo(self):
        self.assertTrue(demo()["nonzero_kernel"])
        self.assertTrue(demo()["conserved_plane_wave_kernel"])
