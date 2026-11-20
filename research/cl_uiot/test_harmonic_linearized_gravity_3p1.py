import unittest
from fractions import Fraction as Q
from harmonic_linearized_gravity_3p1 import (
    trace_reverse,harmonic_constraint,reduced_einstein,
    reduction_residual,gauge_constraint_shift_residual,demo
)
from linearized_einstein_3p1 import einstein_linear

class HarmonicLinearizedGravityTests(unittest.TestCase):
    def setUp(self):
        self.h=[[{} for _ in range(4)] for _ in range(4)]
        self.h[0][0]={(0,2,0,0):Q(2)}
        self.h[0][1]=self.h[1][0]={(1,1,0,0):Q(3)}
        self.xi=[{(2,0,0,0):Q(1)}, {}, {(0,0,2,0):Q(2)}, {}]

    def test_general_reduction(self):
        for a in range(4):
            for b in range(4):
                self.assertEqual(reduction_residual(self.h,a,b),{})

    def test_trace_reversal_involution(self):
        self.assertEqual(trace_reverse(trace_reverse(self.h)),self.h)

    def test_gauge_constraint_transformation(self):
        for nu in range(4):
            self.assertEqual(gauge_constraint_shift_residual(self.xi,nu),{})

    def test_zero_harmonic_wave(self):
        z=[[{} for _ in range(4)] for _ in range(4)]
        for nu in range(4):
            self.assertEqual(harmonic_constraint(z,nu),{})
        for a in range(4):
            for b in range(4):
                self.assertEqual(einstein_linear(z,a,b),
                                 reduced_einstein(z,a,b))

    def test_constant_harmonic_field(self):
        h=[[{} for _ in range(4)] for _ in range(4)]
        h[1][1]={(0,0,0,0):Q(3)}
        for nu in range(4):
            self.assertEqual(harmonic_constraint(h,nu),{})
        for a in range(4):
            for b in range(4):
                self.assertEqual(einstein_linear(h,a,b),reduced_einstein(h,a,b))

    def test_nonzero_constraint(self):
        self.assertTrue(any(harmonic_constraint(self.h,nu)
                            for nu in range(4)))

    def test_monomial_reduction(self):
        for axis in range(4):
            for degree in range(4):
                exp=[0]*4
                exp[axis]=degree
                h=[[{} for _ in range(4)] for _ in range(4)]
                h[2][3]=h[3][2]={tuple(exp):Q(2)}
                for a in range(4):
                    for b in range(4):
                        self.assertEqual(reduction_residual(h,a,b),{})

    def test_demo(self):
        self.assertTrue(demo()["general_reduction_identity"])
        self.assertTrue(demo()["gauge_constraint_transformation"])

if __name__=="__main__":
    unittest.main()
