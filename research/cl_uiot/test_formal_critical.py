import unittest
from formal_critical import *

class FormalCriticalTests(unittest.TestCase):
    def test_quadratic(self):self.assertEqual(graph(2),{})
    def test_cubic(self):
        self.assertEqual(graph(3),{(2,1):K(Q(27,2)),(1,2):K(Q(27,2))})
    def test_fourth(self):self.assertEqual(residual(graph(4),4),{})
    def test_fifth(self):self.assertEqual(residual(graph(5),5),{})
    def test_compatible(self):
        self.assertEqual({k:v for k,v in graph(5).items() if sum(k)<=3},graph(3))
    def test_invalid(self):
        with self.assertRaises(ValueError):graph(1)
