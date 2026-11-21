import unittest
from interval_basin import *
from universal_pauli import evaluate
class IntervalTests(unittest.TestCase):
    def test_enclosure(self):
        w=(Q(7,10),Q(1,10),Q(1,10),Q(1,10))
        b=tuple((v-Q(1,100),v+Q(1,100)) for v in w)
        for (lo,hi),v in zip(step(b,3),evaluate(w)):self.assertTrue(lo<=v<=hi)
    def test_uniform(self):
        self.assertEqual(certify(((Q(24,100),Q(26,100)),)*4)["basin"],"uniform")
    def test_vertices(self):
        for i in range(4):
            b=tuple((Q(99,100),1) if j==i else (0,Q(1,100)) for j in range(4))
            self.assertEqual(certify(b)["basin"],"IXYZ"[i])
    def test_multistep(self):
        w=(Q(7,8),)+(Q(1,24),)*3
        r=certify(tuple((v,v) for v in w),8)
        self.assertEqual(r["basin"],"I")
        self.assertGreater(r["steps"],0)
    def test_split(self):
        b=((0,1),)*4
        a,c=split(b)
        self.assertEqual(a[0],(0,Q(1,2)))
        self.assertEqual(c[0],(Q(1,2),1))
    def test_unknown(self):self.assertIsNone(certify(((0,1),)*4,0)["basin"])
    def test_invalid(self):
        with self.assertRaises(ValueError):box(((0,Q(1,10)),)*4)
