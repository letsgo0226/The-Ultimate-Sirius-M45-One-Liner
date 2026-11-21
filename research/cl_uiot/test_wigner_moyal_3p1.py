import unittest
from fractions import Fraction as Q
from wigner_moyal_3p1 import bidifferential,moyal_coefficient,hamiltonian,liouville

class MoyalTests(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(moyal_coefficient({(1,0,0,0):1},{(0,1,0,0):1},0),{(0,0,0,0):1})
    def test_quadratic(self):
        w={(5,4,3,2):Q(3)}
        for r in (1,2,3):
            self.assertEqual(moyal_coefficient(hamiltonian(2),w,r),{})
    def test_transport(self):
        self.assertEqual(liouville(2,{(1,0,0,0):1}),{(0,1,0,0):-1})
    def test_stationary(self):
        self.assertEqual(liouville(3,hamiltonian(3)),{})
    def test_cubic_counterexample(self):
        a={(3,0,0,0):1};b={(0,3,0,0):1}
        self.assertEqual(moyal_coefficient(a,b,1),{(0,0,0,0):Q(-3,2)})
        self.assertEqual(moyal_coefficient(a,b,2),{})
    def test_invalid(self):
        with self.assertRaises(ValueError):moyal_coefficient({}, {},-1)
