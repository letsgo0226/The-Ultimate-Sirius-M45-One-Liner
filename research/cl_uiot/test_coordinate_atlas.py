import unittest
from itertools import product
from fractions import Fraction as Q
from coordinate_atlas import point,chart,lift,reflect,step,regular_step

class TestAtlas(unittest.TestCase):
    def test_overlap(self):
        for u,v in product(range(-8,9),repeat=2):
            if not (u or v):
                continue
            p=point(u,v)
            for k,valid in (("x",v),("y",u)):
                if valid:
                    self.assertEqual(lift(chart(p,k),k),p)
            if u and v:
                self.assertEqual(chart(p,"x")*chart(p,"y"),1)
            self.assertEqual(reflect(reflect(p)),p)
            self.assertEqual(step(p),regular_step(p))
    def test_crossing(self):
        p=point(1,2)
        path=[]
        for _ in range(5):
            path.append(p)
            p=regular_step(p)
        self.assertEqual(path,[point(1,2),point(1,1),point(1,0),
                               point(-1,1),point(-1,2)])
        with self.assertRaises(ValueError):
            chart(point(1,0),"x")
        self.assertEqual(chart(point(1,0),"y"),0)
    def test_zero_pair(self):
        with self.assertRaises(ValueError):
            point(0,0)
