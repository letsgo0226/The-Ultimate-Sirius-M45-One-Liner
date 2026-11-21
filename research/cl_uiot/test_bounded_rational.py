import unittest
from fractions import Fraction as Q
from bounded_rational import bounded,request

class BoundedRationalTest(unittest.TestCase):
    def test_exact(self):
        for i in range(-8,9):
            for j in range(-8,9):
                a,b=Q(i,3),Q(j,7)
                for op,v in (("+",a+b),("-",a-b),("*",a*b)):
                    self.assertEqual(bounded(op,a,b,32),v)
                if b:
                    self.assertEqual(bounded("/",a,b,32),a/b)
    def test_budget(self):
        self.assertEqual(request("*",2**100,2**100,128),{"state":"UNKNOWN","reason":"resource_limit"})
        self.assertEqual(request("+",Q(1,2**100),Q(1,2**101),128)["state"],"UNKNOWN")
        self.assertEqual(request("*",2**100,0,64)["state"],"UNKNOWN")
        self.assertEqual(request("/",1,0)["reason"],"invalid_request")
        self.assertEqual(request("+",True,1)["reason"],"invalid_request")
        self.assertEqual(request("+",0.1,1)["reason"],"invalid_request")
        self.assertEqual(bounded("*",2**50,2**50,128),2**100)
