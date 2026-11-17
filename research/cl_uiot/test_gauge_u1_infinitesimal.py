import unittest
from fractions import Fraction as Q
from gauge_u1_infinitesimal import (
    J, covariant, gauge_variation, gauge_potential_variation,
    check_infinitesimal_covariance, demo
)
from klein_gordon_1p1 import derivative, scale

class GaugeU1Tests(unittest.TestCase):
    def setUp(self):
        self.v = ({(2,0):Q(2),(0,1):Q(3)}, {(1,1):Q(1),(0,0):Q(4)})
        self.A = ({(1,0):Q(2)}, {(0,1):Q(-1)})
        self.alpha = {(1,1):Q(2),(1,0):Q(1)}

    def test_generator_square(self):
        self.assertEqual(J(J(self.v)), (scale(self.v[0],-1),scale(self.v[1],-1)))

    def test_nonconstant_local_gauge(self):
        for mu in (0,1):
            self.assertTrue(check_infinitesimal_covariance(
                self.v,self.A,self.alpha,mu,Q(2)))

    def test_varied_polynomials(self):
        for i in range(4):
            for j in range(4):
                v=({(i,j):Q(3)}, {(j,i):Q(-2)})
                alpha={(j,i):Q(2),(0,0):Q(1)}
                for mu in (0,1):
                    self.assertTrue(check_infinitesimal_covariance(
                        v,self.A,alpha,mu,Q(3,2)))

    def test_constant_global_phase(self):
        constant={(0,0):Q(2)}
        for mu in (0,1):
            self.assertEqual(gauge_potential_variation(constant,mu), {})

    def test_wrong_sign_breaks_covariance(self):
        # The gauge potential shift is essential for local alpha.
        from gauge_u1_infinitesimal import vadd, pmulvec, vscale
        mu=0
        wrong=vadd(covariant(gauge_variation(self.v,self.alpha),self.A,mu,Q(2)),
                   vscale(pmulvec(scale(gauge_potential_variation(self.alpha,mu,Q(2)),-1),J(self.v)),Q(2)))
        expected=gauge_variation(covariant(self.v,self.A,mu,Q(2)),self.alpha)
        self.assertNotEqual(wrong,expected)

    def test_reject_zero_charge(self):
        with self.assertRaises(ValueError):
            check_infinitesimal_covariance(self.v,self.A,self.alpha,0,Q(0))

    def test_demo(self):
        self.assertTrue(demo()["first_order_gauge_covariance"])

if __name__ == "__main__":
    unittest.main()
