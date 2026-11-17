import unittest
from fractions import Fraction as Q
from coupled_scalar_u1_3p1 import (
    J,dot,D,delta_D,delta_u,delta_A,check_covariance,
    coupled_lagrangian,first_order_lagrangian_variation,demo
)
from maxwell_3p1 import add,deriv,scale

class CoupledScalarU1Tests(unittest.TestCase):
    def setUp(self):
        self.u=({(2,0,0,0):Q(2),(0,1,0,0):Q(1)},
                {(0,0,1,1):Q(3),(0,0,0,0):Q(4)})
        self.A=({(0,1,0,0):Q(2)}, {(1,0,0,0):Q(1)},
                {}, {(0,0,1,0):Q(3)})
        self.alpha={(1,1,0,0):Q(2),(0,0,0,1):Q(1)}

    def test_generator_antisymmetry(self):
        self.assertEqual(dot(self.u,J(self.u)),{})

    def test_covariant_derivative(self):
        self.assertTrue(check_covariance(self.u,self.A,self.alpha,Q(2)))

    def test_full_action_density_first_order(self):
        self.assertEqual(first_order_lagrangian_variation(
            self.u,self.A,self.alpha,Q(3),Q(2)),{})

    def test_monomial_stress(self):
        for axis in range(4):
            for power in range(4):
                exponents=[0]*4
                exponents[axis]=power
                u=({tuple(exponents):Q(3)},self.u[1])
                for q in (Q(1),Q(3,2),Q(-2)):
                    self.assertTrue(check_covariance(u,self.A,self.alpha,q))
                    self.assertEqual(first_order_lagrangian_variation(
                        u,self.A,self.alpha,Q(5,3),q),{})

    def test_pure_gauge_shift_curvature_zero(self):
        dA=delta_A(self.alpha,Q(2))
        from maxwell_3p1 import strength
        for mu in range(4):
            for nu in range(mu+1,4):
                self.assertEqual(strength(dA,mu,nu),{})

    def test_wrong_potential_sign_breaks(self):
        # Drop delta A term: local derivative of alpha remains uncancelled.
        from coupled_scalar_u1_3p1 import vmul
        du=delta_u(self.u,self.alpha)
        self.assertNotEqual(D(du,self.A,0,Q(2)),
                            vmul(self.alpha,J(D(self.u,self.A,0,Q(2)))))

    def test_zero_charge_rejected(self):
        with self.assertRaises(ValueError):
            delta_A(self.alpha,Q(0))

    def test_demo(self):
        self.assertTrue(demo()["coupled_lagrangian_first_order_invariant"])

if __name__=="__main__":
    unittest.main()
