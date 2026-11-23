import unittest
from stable_extension import *
class ExtensionTests(unittest.TestCase):
    def test_identity(self):
        self.assertTrue(preimage((1,0,0,0),2,lambda w:w[0]==1))
    def test_zero(self):
        self.assertEqual(pullback(((0,1),)*4,0),box(((0,1),)*4))
    def test_exclusion(self):
        self.assertTrue(exclude(((1,1),(0,0),(0,0),(0,0)),((Q(1,4),Q(1,4)),)*4,2))
    def test_overlap(self):
        self.assertFalse(exclude(((0,1),)*4,((Q(1,4),Q(1,4)),)*4,1))
    def test_simplex(self):
        a=((Q(1,2),1),(0,1),(0,1),(0,1))
        b=((0,1),(Q(3,4),1),(0,1),(0,1))
        self.assertFalse(intersects(a,b))
    def test_invalid(self):
        with self.assertRaises(ValueError):pullback(((0,1),)*4,-1)
