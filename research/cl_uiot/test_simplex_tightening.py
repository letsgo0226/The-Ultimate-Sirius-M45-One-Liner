import unittest
from simplex_tightening import *
class TighteningTests(unittest.TestCase):
    def test_hull(self):
        b=((Q(3,4),1),(0,1),(0,1),(0,1))
        self.assertEqual(tighten(b),((Q(3,4),1),(0,Q(1,4)),(0,Q(1,4)),(0,Q(1,4))))
    def test_idempotent(self):
        b=tighten(((Q(1,2),Q(3,4)),(0,Q(1,2)),(0,Q(1,2)),(0,Q(1,2))))
        self.assertEqual(tighten(b),b)
    def test_full(self):self.assertEqual(tighten(((0,1),)*4),box(((0,1),)*4))
    def test_capture(self):
        b=((Q(19,20),1),(0,1),(0,1),(0,1))
        self.assertEqual(capture_tight(b)["status"],"I")
    def test_invalid(self):
        with self.assertRaises(ValueError):tighten(((Q(1,2),1),)*4)
    def test_lower(self):
        b=((0,Q(1,4)),)*4
        self.assertEqual(tighten(b),((Q(1,4),Q(1,4)),)*4)
