import unittest
from fractions import Fraction as Q
from algebraic_zero import roots,verify,residual_at,matrix_roots

class TestAlgebraicZero(unittest.TestCase):
    def test_exact(self):
        for a in range(33):
            for b in range(1,17):
                c=Q(a,b)
                rr=roots(c)
                self.assertEqual(sum(r[3] for r in rr),2)
                for r in rr:
                    self.assertTrue(verify(c,r))
                    self.assertEqual(residual_at(c,r),(0,0))
                    self.assertIn((1-r[0],-r[1],r[2],r[3]),rr)
                self.assertEqual(len(rr),1 if c==0 else 2)
    def test_tiny(self):
        c=Q(1,10**200)
        self.assertEqual(len(roots(c)),2)
        self.assertTrue(verify(c,roots(c)[0]))
        self.assertFalse(verify(c,roots(0)[0]))
    def test_matrix(self):
        for a in range(-8,9):
            for b in range(-8,9):
                self.assertEqual(len(matrix_roots(Q(a,3),Q(b,7))),1 if b==0 else 2)
    def test_invalid(self):
        for c in (-1,0.0,True):
            with self.assertRaises(ValueError):
                roots(c)
        self.assertFalse(verify(1,(Q(1,2),1,Q(1),2)))
