import unittest
from invariant_capture import *
from universal_pauli import from_bloch
class InvariantCaptureTests(unittest.TestCase):
    def point(self,z):
        return tuple((v,v) for v in from_bloch(*z))
    def test_direct(self):
        self.assertEqual(capture(self.point((Q(5,6),Q(4,5),Q(4,5))))["status"],"invariant_cone")
    def test_uniform(self):
        self.assertEqual(capture(((Q(1,4),Q(1,4)),)*4)["status"],"uniform")
    def test_unknown(self):
        self.assertEqual(capture(((0,1),)*4,0)["status"],"unknown")
    def test_vertex(self):
        self.assertEqual(capture(self.point((1,1,1)))["status"],"I")
    def test_invalid(self):
        with self.assertRaises(ValueError):capture(((0,1),)*4,-1)
