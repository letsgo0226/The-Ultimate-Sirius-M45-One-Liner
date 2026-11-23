import unittest
from fractions import Fraction as Q
from independent_identity import decide
from proof_halting import run

class IndependentIdentityTest(unittest.TestCase):
    def test_differential(self):
        x=("x",)
        for i in range(-8,9):
            for j in range(-8,9):
                a,b=("q",i,3),("q",j,7)
                p=("*",("+",x,a),("+",x,b))
                q=("+",("+",("*",x,x),("*",("+",a,b),x)),("*",a,b))
                for rhs in (q,("+",q,("q",1,999))):
                    self.assertEqual(decide(p,rhs)[0],run(p,rhs)[0])
    def test_delayed(self):
        p=("q",1,1)
        for k in range(12):
            p=("*",p,("-",("x",),("q",k,1)))
        self.assertEqual(decide(p,("q",0,1)),("HALT_COUNTEREXAMPLE",12,Q(479001600)))
    def test_limits(self):
        for p in (("q",True,1),("q",1,0),("/",("x",),("x",))):
            self.assertEqual(decide(p,("x",)),("UNKNOWN",))
        p=("x",)
        for _ in range(7):
            p=("*",p,p)
        self.assertEqual(decide(p,p),("UNKNOWN",))
