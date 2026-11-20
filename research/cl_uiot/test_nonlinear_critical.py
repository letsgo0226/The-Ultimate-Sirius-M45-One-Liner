import unittest
from fractions import Fraction as Q
from nonlinear_critical import *
from universal_pauli import evaluate
from logical_renormalization import depolarizing

class NonlinearTests(unittest.TestCase):
    def test_jet(self):
        w=depolarizing(Q(1,8));v=(0,1,-1,0);t=Q(1,100)
        self.assertEqual(tuple(sum(c*t**i for i,c in enumerate(a)) for a in jet(w,v)),evaluate(tuple(x+t*y for x,y in zip(w,v))))
    def test_conservation(self):
        a=jet(depolarizing(Q(1,8)),(0,1,-1,0))
        self.assertEqual(tuple(map(sum,zip(*a))),(1,0,0,0,0,0))
    def test_hessian(self):
        w=depolarizing(Q(1,8));u=(0,1,-1,0);v=(0,0,1,-1)
        self.assertEqual(hessian_action(w,u,v),hessian_action(w,v,u))
        self.assertEqual(hessian_action(w,u,u),tuple(2*a[2] for a in jet(w,u)))
    def test_transverse_linear(self):
        self.assertTrue(all(a[1]==0 for a in jet(depolarizing(Q(1,8)),(0,1,-1,0))))
    def test_graph(self):
        w=depolarizing(Q(1,8));v=(0,1,-1,0)
        self.assertEqual(Q(5,3)*stable_graph_coefficient(w,v)+radial_quadratic(w,v),0)
    def test_invalid(self):
        with self.assertRaises(ValueError):jet((1,0,0,0),(1,0,0,0))
