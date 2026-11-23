import unittest
from fractions import Fraction as Q
from correspondence import produce,verify

class TestCorrespondence(unittest.TestCase):
    def test_instances(self):
        for a in range(-8,9):
            for b in range(-8,9):
                self.assertTrue(verify(produce(Q(a,3),Q(b,7))))
    def test_tampering(self):
        r=produce(2,0)
        for k,v in (("residual",Q(1)),("roots",()),("state","HALT_COUNTEREXAMPLE"),
                    ("theorem_id",61),("prime_terms",()),("tableau",()),
                    ("parameters",(Q(2),Q(1)))):
            self.assertFalse(verify(dict(r,**{k:v})))
        self.assertFalse(verify(None))
        self.assertFalse(verify({}))
    def test_tiny(self):
        r=produce(2,Q(1,10**100))
        self.assertTrue(verify(r))
        self.assertEqual(r["state"],"HALT_COUNTEREXAMPLE")
