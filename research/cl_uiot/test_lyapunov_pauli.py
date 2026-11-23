import unittest
from lyapunov_pauli import *
from itertools import product

class LyapunovTests(unittest.TestCase):
    def test_grid(self):
        for z in product(range(-5,6),repeat=3):
            if sum(map(abs,z))<=5:
                w=tuple(Q(x,5) for x in z)
                self.assertLessEqual(lyapunov(step(w)),factor()*lyapunov(w))
    def test_axis(self):self.assertEqual(step((1,0,0)),(Q(-1,4),0,0))
    def test_center(self):self.assertEqual(step((0,0,0)),(0,0,0))
    def test_bound(self):self.assertEqual(bound((1,0,0),2),Q(81,256))
    def test_invalid(self):
        with self.assertRaises(ValueError):step((1,1,1))
        with self.assertRaises(ValueError):bound((0,0,0),-1)
