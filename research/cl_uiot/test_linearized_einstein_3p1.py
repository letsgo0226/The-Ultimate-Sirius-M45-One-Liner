import unittest
from fractions import Fraction as Q
from linearized_einstein_3p1 import (
    trace,ricci_linear,scalar_linear,einstein_linear,
    bianchi_residual,gauge_shift,gauge_residual,demo
)

class LinearizedEinsteinTests(unittest.TestCase):
    def setUp(self):
        self.h=[[{} for _ in range(4)] for _ in range(4)]
        self.h[0][0]={(0,2,0,0):Q(2)}
        self.h[0][1]=self.h[1][0]={(1,1,0,0):Q(3)}
        self.xi=[{(2,0,0,0):Q(1)}, {}, {(0,0,2,0):Q(2)}, {}]

    def test_bianchi(self):
        for nu in range(4):
            self.assertEqual(bianchi_residual(self.h,nu),{})

    def test_gauge_invariance(self):
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(gauge_residual(self.xi,mu,nu),{})

    def test_gauge_shift_nontrivial(self):
        self.assertTrue(any(gauge_shift(self.xi)[mu][nu]
                            for mu in range(4) for nu in range(4)))

    def test_symmetric_einstein(self):
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(einstein_linear(self.h,mu,nu),
                                 einstein_linear(self.h,nu,mu))

    def test_ricci_trace(self):
        from maxwell_3p1 import ETA,add,scale
        self.assertEqual(scalar_linear(self.h),
                         add(*(scale(ricci_linear(self.h,mu,mu),ETA[mu])
                               for mu in range(4))))

    def test_nontrivial(self):
        self.assertTrue(any(einstein_linear(self.h,mu,nu)
                            for mu in range(4) for nu in range(4)))

    def test_monomials(self):
        for axis in range(4):
            for degree in range(4):
                exp=[0]*4
                exp[axis]=degree
                h=[[{} for _ in range(4)] for _ in range(4)]
                h[1][2]=h[2][1]={tuple(exp):Q(3)}
                for nu in range(4):
                    self.assertEqual(bianchi_residual(h,nu),{})

    def test_zero_tensor(self):
        z=[[{} for _ in range(4)] for _ in range(4)]
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(einstein_linear(z,mu,nu),{})

    def test_reject_asymmetry(self):
        self.h[1][0]={}
        with self.assertRaises(ValueError):
            trace(self.h)

    def test_demo(self):
        self.assertTrue(demo()["linearized_bianchi"])
        self.assertTrue(demo()["gauge_invariance"])

if __name__=="__main__":
    unittest.main()
