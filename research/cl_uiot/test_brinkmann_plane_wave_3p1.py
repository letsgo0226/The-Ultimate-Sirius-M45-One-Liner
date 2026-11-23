import unittest
from fractions import Fraction as Q
from brinkmann_plane_wave_3p1 import perturbation,transverse_laplacian,curvature_components,pullback_residual,determinant
from formal_einstein_3p1 import coefficients
from recursive_tt_vacuum_3p1 import zero
from tt_gravity_wave_3p1 import profile

class BrinkmannTests(unittest.TestCase):
    def test_vacuum(self):
        self.assertEqual(coefficients([perturbation([1,2]),zero(),zero()]),[zero()]*4)
    def test_laplacian(self):
        self.assertEqual(transverse_laplacian([1,2,3]),{})
    def test_curvature(self):
        self.assertEqual(curvature_components([2]),(profile([-2]),profile([2])))
    def test_pullback(self):
        self.assertEqual(pullback_residual(2,3,-4,5,6,10,2),(0,0))
    def test_off_shell(self):
        self.assertEqual(pullback_residual(2,0,0,3,0,0,1),(4,-9))
    def test_determinant(self):
        self.assertEqual(determinant(),-1)
