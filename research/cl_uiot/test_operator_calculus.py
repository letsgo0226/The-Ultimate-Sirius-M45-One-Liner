import unittest
from fractions import Fraction as Q
from operator_calculus import evaluate,reference,verify,apply_prefix,reduce_expr
from direct_limit import embed

class TestOperatorCalculus(unittest.TestCase):
    def test_matrix(self):
        x=("x",)
        for k in range(-8,9):
            t=((-1,Q(k,3)),(0,1))
            for j in range(-8,9):
                e=("*",("+",x,("q",j,7)),("*",x,x))
                r=evaluate(e,t)
                self.assertEqual(r,reference(e,t))
                self.assertTrue(verify(e,t,r))
                self.assertFalse(verify(e,t,((Q(999),Q(0)),r[1])))
                self.assertFalse(verify(e,t,tuple(tuple(float(v) for v in row) for row in r)))
    def test_prefix(self):
        x=("x",)
        e=("+",("*",x,x),("*",("q",2,3),x))
        self.assertEqual(reduce_expr(e),(Q(1),Q(2,3)))
        for n in range(1,65):
            v=tuple(Q(i-3,7) for i in range(n))
            self.assertEqual(apply_prefix(e,embed(v)),embed(apply_prefix(e,v)))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            evaluate(("x",),((2,),))
