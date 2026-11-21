import unittest
from fractions import Fraction as Q
from conformal_trace_counterexample_3p1 import example,demo
from conformal_einstein_bianchi_3p1 import einstein_numerator
from conformal_einstein_hilbert_3p1 import euler_lagrange_density
from conformal_geometry_3p1 import scalar_curvature_numerator

class ConformalTraceCounterexampleTests(unittest.TestCase):
    def setUp(self):
        self.omega={(0,0,0,0):Q(2),(1,0,0,0):Q(1)}

    def test_restricted_stationary(self):
        self.assertEqual(euler_lagrange_density(self.omega),{})

    def test_zero_scalar_curvature(self):
        self.assertEqual(scalar_curvature_numerator(self.omega),{})

    def test_nonzero_einstein_tensor(self):
        self.assertTrue(any(einstein_numerator(self.omega,mu,nu)
                            for mu in range(4) for nu in range(4)))

    def test_spatial_diagonal_component(self):
        self.assertNotEqual(einstein_numerator(self.omega,1,1),{})

    def test_trace_identity(self):
        self.assertTrue(example()["trace_identity"])

    def test_bianchi_identity(self):
        self.assertTrue(example()["bianchi_identity"])

    def test_variational_identity(self):
        self.assertTrue(example()["variational_identity"])

    def test_flat_comparison(self):
        flat={(0,0,0,0):Q(2)}
        for mu in range(4):
            for nu in range(4):
                self.assertEqual(einstein_numerator(flat,mu,nu),{})

    def test_demo(self):
        self.assertTrue(demo()["full_vacuum_einstein_equation_fails"])
        self.assertTrue(demo()["geometric_consistency"])

if __name__=="__main__":
    unittest.main()
