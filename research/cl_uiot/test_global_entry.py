import unittest
from global_entry import *
from fractions import Fraction as Q
class EntryTests(unittest.TestCase):
    def test_uniform(self):
        r=cover(((Q(1,4),Q(1,4)),)*4)
        self.assertTrue(r["complete"])
        self.assertTrue(verify(r))
    def test_zero_budget(self):
        r=cover(((0,1),)*4,0)
        self.assertFalse(r["complete"])
        self.assertEqual(len(r["leaves"]),1)
    def test_split(self):
        r=cover(((0,1),)*4,1,2,0)
        self.assertFalse(r["complete"])
        self.assertEqual(len(r["leaves"]),2)
        self.assertTrue(verify(r))
    def test_tamper(self):
        r=cover(((0,1),)*4,0)
        r["complete"]=True
        self.assertFalse(verify(r))
    def test_invalid(self):
        with self.assertRaises(ValueError):cover(((0,1),)*4,-1)
