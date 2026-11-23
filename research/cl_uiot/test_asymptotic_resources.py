import unittest
from fractions import Fraction as Q
from qec_concatenated_5qubit import bound,iterate
from qec_minimum_resources import plan
from asymptotic_resources import bracket,depth_interval,zeta_interval
from zeta_reliability import allocation

class AsymptoticTests(unittest.TestCase):
    def test_one_step(self):
        for k in range(101):
            p=Q(k,100)
            self.assertLessEqual(p*p,bound(p))
            self.assertLessEqual(bound(p),10*p*p)
    def test_iterates(self):
        for p in (Q(1,100),Q(1,20),Q(9,100)):
            for n in range(5):
                a,b=bracket(p,n)
                self.assertLessEqual(a,iterate(p,n))
                self.assertLessEqual(iterate(p,n),b)
    def test_depth(self):
        p,e=Q(1,20),Q(1,10**9)
        a,b=depth_interval(p,e,6)
        n=plan(p,e,5**6)["depth"]
        self.assertTrue(a<=n<=b)
    def test_zeta(self):
        p=Q(1,20)
        for t in (0,10,100):
            a,b=zeta_interval(p,Q(1,100),t,6)
            n=plan(p,allocation(Q(1,100),t),5**6)["depth"]
            self.assertTrue(a<=n<=b)
    def test_unresolved(self):
        self.assertEqual(depth_interval(Q(1,20),Q(1,1000),0),(None,None))
    def test_zero_depth(self):
        self.assertEqual(depth_interval(Q(1,20),Q(1,10),0),(0,0))
    def test_invalid(self):
        with self.assertRaises(ValueError):bracket(0,1)
