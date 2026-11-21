import unittest
from fractions import Fraction as Q
from volterra_factorial_3p1 import bound_parameter,tail_bound,iterate,positive_certificate

class FactorialVolterraTests(unittest.TestCase):
    def test_beyond_contraction(self):
        self.assertEqual(bound_parameter([1],3),9)
        f,e=iterate([1],3,-1,5)
        self.assertEqual(f[2],Q(-1,2))
        self.assertLess(e,Q(1,100))
    def test_tail_decreases(self):
        self.assertLess(tail_bound([1],3,6),tail_bound([1],3,5))
    def test_zero(self):
        self.assertEqual(tail_bound([],10,0),0)
    def test_variable(self):
        self.assertEqual(bound_parameter([1,-2],2),20)
    def test_positive(self):
        f,e=iterate([1],Q(1,2),-1,3)
        self.assertGreater(positive_certificate(f,Q(1,2),e),0)
    def test_not_certified(self):
        f,e=iterate([1],3,-1,5)
        self.assertLess(positive_certificate(f,3,e),0)
    def test_reject(self):
        with self.assertRaises(ValueError):tail_bound([1],10,0)
