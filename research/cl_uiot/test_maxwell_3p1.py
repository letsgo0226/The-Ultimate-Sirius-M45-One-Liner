import unittest
from fractions import Fraction as Q
from maxwell_3p1 import (strength,gauge_shift,lagrangian,maxwell_divergence,
                         current_divergence,check_bianchi,check_gauge_invariance,
                         deriv,check_A,demo)

Z={}
class Maxwell3p1Tests(unittest.TestCase):
    def setUp(self):
        self.A=({(0,1,0,0):Q(2)}, {(2,0,0,0):Q(1)},
                {(0,0,1,0):Q(3)}, {(0,0,0,1):Q(4)})
        self.chi={(1,1,1,0):Q(2),(0,0,0,2):Q(1)}

    def test_electric_field_component(self):
        self.assertEqual(strength(self.A,0,1), {})

    def test_gauge_invariance(self):
        self.assertTrue(check_gauge_invariance(self.A,self.chi))

    def test_pure_gauge(self):
        pure=gauge_shift((Z,Z,Z,Z),self.chi)
        self.assertEqual(lagrangian(pure),{})
        self.assertTrue(check_bianchi(pure))

    def test_bianchi_identity(self):
        self.assertTrue(check_bianchi(self.A))

    def test_current_conservation(self):
        self.assertEqual(current_divergence(maxwell_divergence(self.A)),{})

    def test_monomial_stress(self):
        for axis in range(4):
            for power in range(1,5):
                exponents=[0]*4
                exponents[axis]=power
                A=[{}, {}, {}, {}]
                A[(axis+1)%4]={tuple(exponents):Q(3)}
                A=tuple(A)
                self.assertTrue(check_bianchi(A))
                self.assertEqual(current_divergence(maxwell_divergence(A)),{})
                self.assertTrue(check_gauge_invariance(A,self.chi))

    def test_magnetic_field_sign(self):
        A=({}, {}, {(0,0,1,0):Q(2)}, {})
        self.assertEqual(strength(A,1,2), {})
        A=({}, {}, {(0,1,0,0):Q(2)}, {})
        self.assertEqual(strength(A,1,2), {(0,0,0,0):Q(2)})
        self.assertEqual(lagrangian(A), {(0,0,0,0):Q(-2)})

    def test_invalid_potential(self):
        with self.assertRaises(ValueError):
            check_A(({},{}))

    def test_demo(self):
        self.assertTrue(demo()["gauge_invariant"])
        self.assertTrue(demo()["bianchi_identity"])

if __name__=="__main__":
    unittest.main()
