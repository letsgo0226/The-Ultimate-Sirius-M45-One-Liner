import unittest
from abelian_chiral import compose,neighbors,embed,recover,reconstruct

class TestAbelianChiral(unittest.TestCase):
    def test_group(self):
        for n in range(1,5):
            for x in range(1<<n):
                self.assertEqual(compose(n,x,x),0)
                self.assertEqual(compose(n,x,0),x)
                for y in range(1<<n):
                    self.assertEqual(compose(n,x,y),compose(n,y,x))
                    self.assertEqual(compose(n,compose(n,x,y),y),x)
                    for z in range(1<<n):
                        self.assertEqual(compose(n,compose(n,x,y),z),
                                         compose(n,x,compose(n,y,z)))
    def test_cube(self):
        for n in range(1,9):
            edges=set()
            for x in range(1<<n):
                self.assertEqual(len(set(neighbors(n,x))),n)
                for y in neighbors(n,x):
                    self.assertIn(x,neighbors(n,y))
                    edges.add(tuple(sorted((x,y))))
            self.assertEqual(len(edges),n*(1<<(n-1)))
    def test_split(self):
        for n in range(1,9):
            for x in range(1<<n):
                self.assertEqual(recover(n,embed(n,x)),(x,0))
            for y in range(1<<(n+1)):
                self.assertEqual(reconstruct(n,*recover(n,y)),y)
    def test_bounds(self):
        for n,x in ((0,0),(17,0),(2,4),(2,-1),(2,True)):
            with self.assertRaises(ValueError):
                neighbors(n,x)
        with self.assertRaises(ValueError):
            embed(16,0)
