import unittest
from fractions import Fraction as Q
from proof_halting import run,verify

class TestProofHalting(unittest.TestCase):
    def test_grid(self):
        x=("x",)
        for i in range(-8,9):
            for j in range(-8,9):
                a,b=("q",i,3),("q",j,7)
                p=("*",x,("+",a,b))
                q=("+",("*",x,a),("*",x,b))
                r=run(p,q)
                self.assertEqual(r[0],"HALT_PROOF")
                self.assertTrue(verify(r,p,q))
                s=("+",q,("q",1,999))
                r=run(p,s)
                self.assertEqual(r[0],"HALT_COUNTEREXAMPLE")
                self.assertTrue(verify(r,p,s))
                self.assertFalse(verify(r,p,q))
    def test_roots(self):
        x=("x",)
        p=("q",1,1)
        for i in range(12):
            p=("*",p,("-",x,("q",i,1)))
        z=("q",0,1)
        r=run(p,z)
        self.assertEqual(r[4],(12,Q(479001600)))
        self.assertTrue(verify(r,p,z))
        self.assertFalse(verify(r[:4]+((12,479001600.0),),p,z))
    def test_unknown(self):
        a=("/",("x",),("x",))
        self.assertEqual(run(a,("x",)),("UNKNOWN",))
        self.assertFalse(verify(("UNKNOWN",),a,("x",)))
