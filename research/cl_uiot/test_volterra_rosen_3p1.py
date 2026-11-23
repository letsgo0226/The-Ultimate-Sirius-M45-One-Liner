import unittest
from fractions import Fraction as Q
from volterra_rosen_3p1 import contraction_bound,step,iterate,positivity_bound

class VolterraTests(unittest.TestCase):
    def test_constant(self):
        f,e=iterate([1],Q(1,2),-1,2)
        self.assertEqual(f,[1,0,Q(-1,2),0,Q(1,24)])
        self.assertEqual(e,Q(1,448))
    def test_hyperbolic(self):
        self.assertEqual(iterate([1],Q(1,2),1,2)[0],[1,0,Q(1,2),0,Q(1,24)])
    def test_variable(self):
        self.assertEqual(step([0,2],[1],-1),[1,0,0,Q(-1,3)])
    def test_positive(self):
        self.assertEqual(positivity_bound([1],Q(1,2)),Q(6,7))
    def test_zero(self):
        self.assertEqual(iterate([],1,1,0),([1],0))
    def test_reject(self):
        with self.assertRaises(ValueError):iterate([1],1,1,2)
        with self.assertRaises(ValueError):iterate([1],-1,1,2)
