import unittest
from fractions import Fraction as Q
from itertools import product
from coordinate_atlas import point,reflect,step
from singularity_atlas import diagnostic,inverse_step,curvature_scaled,reciprocal_curvature

class TestSingularityAtlas(unittest.TestCase):
    def test_horizon(self):
        for m in (Q(1,3),Q(1),Q(2)):
            self.assertEqual(diagnostic(2*m,m),("coordinate_horizon",Q(3,4)/m**4))
            self.assertEqual(diagnostic(0,m),("curvature_singularity",None))
            for r in (m,3*m,m/10):
                self.assertEqual(curvature_scaled(r,m),48*m*m)
                self.assertEqual(reciprocal_curvature(r,m)*diagnostic(r,m)[1],1)
            self.assertEqual(reciprocal_curvature(0,m),0)
    def test_divergence(self):
        for n in range(1,12):
            self.assertEqual(diagnostic(Q(1,n))[1],48*n**6)
    def test_chiral_inverse(self):
        for u,v in product(range(-8,9),repeat=2):
            if u or v:
                p=point(u,v)
                self.assertEqual(reflect(step(reflect(p))),inverse_step(p))
                self.assertEqual(inverse_step(step(p)),p)
    def test_domain(self):
        for r,m in ((-1,1),(1,0),(0,-1)):
            with self.assertRaises(ValueError):
                diagnostic(r,m)
