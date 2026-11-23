import unittest
from analytic_critical import *

class AnalyticTests(unittest.TestCase):
    def test_default(self):
        c=default_certificate()
        self.assertTrue(c["certified"])
        self.assertLess(c["implicit_lipschitz"],1)
    def test_remainder(self):
        c=default_certificate()
        self.assertLessEqual(c["remainder"],c["radius"]/2)
    def test_smaller(self):self.assertTrue(certificate(Q(1,10**11))["certified"])
    def test_large(self):self.assertFalse(certificate(Q(1,100))["certified"])
    def test_invalid(self):
        with self.assertRaises(ValueError):certificate(0)
