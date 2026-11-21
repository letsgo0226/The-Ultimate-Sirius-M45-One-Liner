import unittest
from fractions import Fraction as Q
from zero_tableau import certificate,run
from zero_tableau_checker import verify

class TestZeroTableau(unittest.TestCase):
    def test_certificate(self):
        c=certificate()
        self.assertTrue(verify(c))
        self.assertTrue(verify(c[::-1]))
        for bad in ((),(c[0],c[0]),(c[0],),None,
                    (c[0],(("!A","B"),"positive_factor","A")),
                    ((("A","!B"),"positive_factor","A"),c[1])):
            self.assertFalse(verify(bad))
    def test_instances(self):
        for a in range(-8,9):
            for b in range(-8,9):
                out=run(Q(a,3),Q(b,7))
                self.assertEqual(out["state"],"HALT_PROOF" if b==0 else "HALT_COUNTEREXAMPLE")
                self.assertEqual(out["residual"]==0,b==0)
                self.assertTrue(verify(out["certificate"]))
