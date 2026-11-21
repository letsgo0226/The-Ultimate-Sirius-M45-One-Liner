import unittest
from fractions import Fraction as Q
from exact_zero import enclosure,matrix_residual

class TestExactZero(unittest.TestCase):
    def test_zero_prefix(self):
        v=enclosure([0]*10)
        self.assertEqual(v["lower"],0)
        self.assertEqual(v["status"],"UNKNOWN")
        self.assertEqual(v["upper"],Q(1,29))
    def test_nonzero(self):
        v=enclosure([1,0],2)
        self.assertEqual(v["lower"],Q(1,8))
        self.assertEqual(v["status"],"NONZERO")
        self.assertEqual(enclosure([Q(1,10**100)],2)["status"],"NONZERO")
    def test_nested_prefix(self):
        for s in range(2,7):
            a=[Q(i%3,7) for i in range(64)]
            full=enclosure(a,s)
            for n in range(1,64):
                v=enclosure(a[:n],s)
                self.assertLessEqual(v["lower"],full["lower"])
                self.assertLessEqual(full["lower"],v["upper"])
    def test_matrix(self):
        for a in range(-8,9):
            for b in range(-8,9):
                self.assertEqual(matrix_residual(Q(a,3),Q(b,7))==0,b==0)
    def test_invalid(self):
        for r in ([],[-1],[0.0],[True]):
            with self.assertRaises(ValueError):
                enclosure(r)
        for s in (1,2.0,17):
            with self.assertRaises(ValueError):
                enclosure([0],s)
