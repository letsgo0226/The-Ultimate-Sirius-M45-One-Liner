import unittest
from certified_continuation import *

class CertifiedTests(unittest.TestCase):
    def test_radius(self):
        self.assertGreater(radius(),Q(1,10**10))
        self.assertTrue(certificate(radius())["certified"])
        self.assertEqual(certificate(radius())["implicit_lipschitz"],Q(6,7))
    def test_tail(self):
        r=radius()
        self.assertEqual(tail(r,r/2,3),r*Q(3,4))
    def test_zero(self):self.assertEqual(tail(radius(),0,2),0)
    def test_decrease(self):
        r=radius()
        self.assertLess(tail(r,r/4,5),tail(r,r/4,4))
    def test_order(self):
        r=radius();e=tail(r,r/4,5)
        self.assertEqual(required_order(r,r/4,e,8),5)
        self.assertIsNone(required_order(r,r/4,e,4))
    def test_transform(self):
        self.assertEqual(transform_error(radius(),3),radius()*Q(6,7)**3)
    def test_invalid(self):
        with self.assertRaises(ValueError):tail(radius(),radius(),3)
