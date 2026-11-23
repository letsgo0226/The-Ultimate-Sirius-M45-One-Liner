import unittest
from global_pauli import *
from basin_separation import closed_bloch
from algebraic_curvature import K

class GlobalPauliTests(unittest.TestCase):
    def test_full_coefficients(self):self.assertEqual(fourier(),expected())
    def test_count(self):self.assertEqual(len(fixed_types()),9)
    def test_vertices(self):
        for s in fixed_signs():self.assertEqual(closed_bloch(*map(Q,s)),s)
    def test_threshold(self):
        a=K(0,Q(1,3))
        for s in fixed_signs():
            x,y,z=[a*t for t in s]
            for b,c,d in ((x,y,z),(y,z,x),(z,x,y)):
                self.assertEqual(b*(5*c*c+5*d*d-b**4-5*c*c*d*d)*Q(1,4),b)
    def test_center(self):self.assertEqual(closed_bloch(0,0,0),(0,0,0))
