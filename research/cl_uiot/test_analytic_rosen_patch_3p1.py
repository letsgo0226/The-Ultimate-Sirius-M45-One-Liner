import unittest
from fractions import Fraction as Q
from formal_einstein_3p1 import coefficients
from tt_gravity_wave_3p1 import profile,tt_wave
from recursive_tt_vacuum_3p1 import solve,zero
from analytic_rosen_patch_3p1 import transverse_metric,metric_coefficients

class RosenPatchTests(unittest.TestCase):
    def test_signature(self):
        self.assertEqual(transverse_metric(Q(1,2),1),(Q(-9,4),Q(-1,4)))
    def test_boundary(self):
        with self.assertRaises(ValueError):transverse_metric(1,1)
    def test_exact_polynomial_vacuum(self):
        h=tt_wave([0,-2],[])
        j=zero()
        j[1][1]=j[2][2]=profile([0,0,-1])
        self.assertEqual(coefficients([h,j,zero(),zero()]),[zero()]*5)
    def test_recursive_agreement(self):
        h=tt_wave([0,-2],[])
        j=zero()
        j[1][1]=j[2][2]=profile([0,0,-1])
        self.assertEqual(solve([0,-2],[],4),[h,j,zero(),zero()])
    def test_coefficients(self):
        self.assertEqual(metric_coefficients(),((-1,-2,-1),(-1,2,-1)))
