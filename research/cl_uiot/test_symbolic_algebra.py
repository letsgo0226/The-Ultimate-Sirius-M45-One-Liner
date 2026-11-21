import unittest
from fractions import Fraction as Q
from symbolic_algebra import normalize,equivalent,encode_expr,decode_expr
from certificate_codec import G

class TestSymbolicAlgebra(unittest.TestCase):
    def test_identities(self):
        x=("x",)
        for i in range(-8,9):
            for j in range(-8,9):
                a,b=("q",i,3),("q",j,7)
                lhs=("*",("+",x,a),("+",x,b))
                rhs=("+",("+",("*",x,x),("*",("+",a,b),x)),("*",a,b))
                self.assertTrue(equivalent(lhs,rhs))
                self.assertEqual(normalize(lhs),(Q(i*j,21),Q(i,3)+Q(j,7),Q(1)))
                self.assertEqual(decode_expr(encode_expr(lhs)),lhs)
        self.assertFalse(equivalent(x,("q",0,1)))
        self.assertEqual(normalize(("-",x,x)),(Q(0),))
    def test_invalid(self):
        for e in (("q",True,1),("q",1,0),("q",1.0,1),("/",("x",),("x",)),("x",1)):
            with self.assertRaises(ValueError):
                normalize(e)
        for b in (b'["x"] ',b'["q",true,1]',b'null'):
            with self.assertRaises(ValueError):
                decode_expr(G(b))
