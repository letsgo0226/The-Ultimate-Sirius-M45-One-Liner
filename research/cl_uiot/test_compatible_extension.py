import unittest
from itertools import product
from reversible_machine import step,backward
from compatible_extension import embed,frozen_step

class TestExtension(unittest.TestCase):
    def test_counterexample(self):
        s=(0,0,(1,0))
        self.assertNotEqual(step(embed(s)),embed(step(s)))
    def test_frozen(self):
        for n in (1,2,4):
            for t in product((0,1),repeat=2*n):
                for q,h in product(range(2),range(n)):
                    s=(q,h,t)
                    a=frozen_step(s,n)
                    self.assertEqual(frozen_step(a,n,True),s)
                    self.assertEqual(frozen_step(frozen_step(s,n,True),n),s)
                    self.assertEqual(a[2][n:],t[n:])
                    base=(q,h,t[:n])
                    self.assertEqual(frozen_step(embed(base),n),embed(step(base)))
