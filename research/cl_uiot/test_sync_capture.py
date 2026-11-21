import unittest
from sync_capture import *
from universal_pauli import from_bloch
class CaptureTests(unittest.TestCase):
    def test_entry(self):
        w=from_bloch(Q(5,6),Q(4,5),Q(4,5))
        self.assertEqual(capture(tuple((v,v) for v in w))["status"],"cone_entry")
    def test_uniform(self):
        self.assertEqual(capture(((Q(1,4),Q(1,4)),)*4)["status"],"uniform")
    def test_unknown(self):
        self.assertEqual(capture(((0,1),)*4,0)["status"],"unknown")
    def test_magnitude(self):
        w=from_bloch(Q(1,2),Q(-1,2),Q(-1,2))
        self.assertEqual(magnitudes(tuple((v,v) for v in w)),((Q(1,2),Q(1,2)),)*3)
    def test_invalid(self):
        with self.assertRaises(ValueError):capture(((0,1),)*4,-1)
