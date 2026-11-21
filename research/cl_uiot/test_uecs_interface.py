import unittest,json
from fractions import Fraction as Q
from symbolic_algebra import encode_expr
from uecs_interface import identity_request,operator_request,correspondence_request,report
from certificate_codec import decode

class TestUECSInterface(unittest.TestCase):
    def test_identity(self):
        x=("x",)
        for k in range(-8,9):
            a=encode_expr(("+",x,("q",k,7)))
            b=encode_expr(x)
            r=identity_request(a,b)
            self.assertTrue(r["verified"])
            self.assertEqual(r["energy"],Q(k*k,49))
            self.assertEqual(r["state"],"HALT_PROOF" if not k else "HALT_COUNTEREXAMPLE")
            self.assertEqual(json.loads(report(r))["state"],r["state"])
    def test_operator(self):
        g=encode_expr(("*",("x",),("x",)))
        self.assertEqual(operator_request(g,((-1,3),(0,1)))["matrix"],((Q(1),Q(0)),(Q(0),Q(1))))
        self.assertEqual(operator_request(g,((2,),)),{"state":"UNKNOWN"})
    def test_correspondence(self):
        for m in (Q(0),Q(1,10**100)):
            r=correspondence_request(2,m)
            self.assertTrue(r["verified"])
            self.assertEqual(decode(r["certificate_code"])["state"],r["state"])
            self.assertTrue(json.loads(report(r))["verified"])
    def test_unknown(self):
        self.assertEqual(identity_request(0,1),{"state":"UNKNOWN"})
        self.assertEqual(correspondence_request(1.0,0),{"state":"UNKNOWN"})
