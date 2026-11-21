import unittest
from itertools import product
from polynomial_enclosure import *
from universal_pauli import evaluate,from_bloch
class PolynomialTests(unittest.TestCase):
    def test_points(self):
        for z in product((Q(-1,2),Q(0),Q(1,2)),repeat=3):
            try:w=from_bloch(*z)
            except ValueError:continue
            b=tuple((v,v) for v in w)
            self.assertEqual(enhanced_step(b),tuple((v,v) for v in evaluate(w)))
    def test_full(self):
        self.assertEqual(enhanced_step(((0,1),)*4),box(((0,1),)*4))
    def test_containment(self):
        b=((Q(1,5),Q(3,10)),)*4
        r=enhanced_step(b)
        for w in set(product((Q(1,5),Q(3,10)),repeat=4)):
            if sum(w)!=1:continue
            self.assertTrue(all(l<=v<=h for (l,h),v in zip(r,evaluate(w))))
        self.assertTrue(all(l<=a<=c<=h for (l,h),(a,c) in zip(step(b),r)))
    def test_square(self):self.assertEqual(square((Q(-1,2),Q(1,4))),(0,Q(1,4)))
    def test_invalid(self):
        with self.assertRaises(ValueError):enhanced_step(((Q(1,2),1),)*4)
