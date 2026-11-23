import unittest
from fractions import Fraction as Q
from analytic_nonflat_rosen_3p1 import metric_series,scaled_tidal,tail_bound
from formal_einstein_3p1 import coefficients
from tt_gravity_wave_3p1 import profile
from recursive_tt_vacuum_3p1 import zero

class NonflatRosenTests(unittest.TestCase):
    def test_coefficients(self):
        h=metric_series(4)
        self.assertEqual(h[1][1][1],profile([0,0,1]))
        self.assertEqual(h[1][2][2],profile([0,0,-1]))
        self.assertEqual(h[3][1][1],profile([0,0,0,0,Q(-1,3)]))
    def test_vacuum(self):
        self.assertEqual(coefficients(metric_series(6)),[zero()]*7)
    def test_nonflat(self):
        self.assertEqual(scaled_tidal(Q(1,2)),(Q(-1,4),Q(1,4)))
    def test_tail(self):
        self.assertGreater(tail_bound(2,Q(1,2)),Q(1,48))
        self.assertLess(tail_bound(4,Q(1,2)),tail_bound(2,Q(1,2)))
        self.assertEqual(tail_bound(4,0),0)
    def test_invalid(self):
        with self.assertRaises(ValueError):tail_bound(2,1)
        with self.assertRaises(ValueError):metric_series(-1)
