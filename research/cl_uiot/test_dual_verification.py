import unittest
from unittest.mock import patch
from fractions import Fraction as Q
from dual_verification import run_dual,verify_dual
from proof_halting import run

class DualVerificationTest(unittest.TestCase):
    def test_grid(self):
        x=("x",)
        for i in range(-8,9):
            for j in range(-8,9):
                p=("*",("+",x,("q",i,3)),("q",j,7))
                z=("+",("*",x,("q",j,7)),("q",i*j,21))
                for b,state in ((z,"HALT_PROOF"),(("+",z,("q",1,999)),"HALT_COUNTEREXAMPLE")):
                    r=run_dual(p,b)
                    self.assertTrue(r["dual_verified"])
                    self.assertEqual(r["state"],state)
    def test_fail_closed(self):
        x=("x",)
        for second in (("UNKNOWN",),("HALT_COUNTEREXAMPLE",0,Q(1))):
            with patch("dual_verification.decide",return_value=second):
                self.assertEqual(run_dual(x,x),{"state":"UNKNOWN","dual_verified":False})
        r=run(x,("q",1,1))
        self.assertFalse(verify_dual(r[:4]+((0,Q(9)),),x,("q",1,1)))
        self.assertFalse(verify_dual(r,x,x))
        with patch("dual_verification.compile_expr",side_effect=ValueError("limit")):
            self.assertFalse(verify_dual(r,x,("q",1,1)))
