import unittest
from fractions import Fraction as Q
from unittest.mock import patch
from symbolic_algebra import encode_expr
from uecv_review import identity,report

class IntegratedReviewTest(unittest.TestCase):
    def test_pipeline(self):
        x=("x",)
        for k in range(-16,17):
            a=encode_expr(("+",x,("q",k,7)))
            b=encode_expr(x)
            r=identity(a,b)
            self.assertTrue(r["dual_verified"])
            self.assertEqual(r["energy"],Q(k*k,49))
            self.assertEqual(r["state"],"HALT_PROOF" if k==0 else "HALT_COUNTEREXAMPLE")
            self.assertEqual(len(r["zeros"]),1 if k==0 else 2)
            self.assertEqual(report(r),report(identity(a,b)))
    def test_fail_closed(self):
        a=encode_expr(("q",2**100,1))
        b=encode_expr(("q",0,1))
        self.assertEqual(identity(a,b,128),{"state":"UNKNOWN"})
        self.assertEqual(identity(0,b),{"state":"UNKNOWN"})
        self.assertEqual(identity(a,b,True),{"state":"UNKNOWN"})
        with patch("uecv_review.run_dual",return_value={"state":"UNKNOWN","dual_verified":False}):
            self.assertEqual(identity(a,b),{"state":"UNKNOWN"})
