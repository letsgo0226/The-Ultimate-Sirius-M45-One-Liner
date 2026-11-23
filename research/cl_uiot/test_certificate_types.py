import unittest
from fractions import Fraction as Q
from correspondence import produce,verify
from algebraic_zero import verify as verify_root

class TestCertificateTypes(unittest.TestCase):
    def test_noncanonical(self):
        for m in (0,1):
            r=produce(0,m)
            for idx,bad in ((0,0.5),(1,float(r["roots"][0][1])),(2,float(r["roots"][0][2])),(3,float(r["roots"][0][3]))):
                row=list(r["roots"][0])
                row[idx]=bad
                roots=(tuple(row),)+r["roots"][1:]
                self.assertFalse(verify(dict(r,roots=roots)))
                self.assertFalse(verify_root(r["residual"],roots[0]))
            self.assertFalse(verify(dict(r,parameters=list(r["parameters"]))))
            self.assertTrue(verify(r))
        r=produce(0,1)
        row=r["roots"][1]
        self.assertFalse(verify_root(Q(1),(row[0],True,row[2],True)))
