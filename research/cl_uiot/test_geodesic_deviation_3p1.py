import unittest
from fractions import Fraction as Q
from geodesic_deviation_3p1 import acceleration,tt_response_residual,demo
from tt_gravity_wave_3p1 import tt_wave
from linearized_einstein_3p1 import gauge_shift

class GeodesicDeviationTests(unittest.TestCase):
    def test_plus(self):
        h=tt_wave([0,0,2],[])
        self.assertEqual(acceleration(h,[1,0,0]),({(0,0,0,0):Q(-2)},{},{}))
        self.assertEqual(acceleration(h,[0,1,0]),({},{(0,0,0,0):Q(2)},{}))
    def test_cross(self):
        self.assertEqual(acceleration(tt_wave([],[0,0,3]),[1,0,0]),
                         ({},{(0,0,0,0):Q(-3)},{}))
    def test_longitudinal(self):
        self.assertEqual(acceleration(tt_wave([0,0,2],[0,0,3]),[0,0,1]),({},{},{}))
    def test_affine(self):
        self.assertEqual(acceleration(tt_wave([1,2],[3,4]),[1,2,3]),({},{},{}))
    def test_response(self):
        for n in range(5):
            h=tt_wave([0]*n+[2],[0]*n+[3])
            self.assertEqual(tt_response_residual(h,[1,2,3]),({},{},{}))
    def test_pure_gauge(self):
        h=gauge_shift([{(2,1,0,0):Q(3)}, {}, {(3,0,0,0):Q(2)}, {}])
        self.assertEqual(acceleration(h,[1,2,3]),({},{},{}))
    def test_demo(self):
        self.assertTrue(demo()["tt_response_identity"])
        self.assertTrue(demo()["nonzero_tidal_response"])
