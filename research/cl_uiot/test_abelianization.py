import unittest
from itertools import product
from abelianization import multiply,inverse,decompose,reconstruct,cocycle,extended_product

class TestAbelianization(unittest.TestCase):
    def test_group(self):
        G=list(product(range(4),range(2)))
        comm=set()
        for g in G:
            self.assertEqual(reconstruct(*decompose(g)),g)
            self.assertEqual(multiply(g,inverse(g)),(0,0))
            for h in G:
                self.assertEqual(extended_product(decompose(g),decompose(h)),decompose(multiply(g,h)))
                comm.add(multiply(multiply(multiply(g,h),inverse(g)),inverse(h)))
                for j in G:
                    self.assertEqual(multiply(multiply(g,h),j),multiply(g,multiply(h,j)))
        self.assertEqual(comm,{(0,0),(2,0)})
    def test_cocycle(self):
        Q=list(product(range(2),repeat=2))
        add=lambda a,b:tuple(x^y for x,y in zip(a,b))
        for a,b,c in product(Q,repeat=3):
            self.assertEqual(cocycle(a,b)^cocycle(add(a,b),c),cocycle(b,c)^cocycle(a,add(b,c)))
        self.assertEqual(cocycle((1,0),(1,0)),1)
        self.assertNotEqual(multiply((1,0),(0,1)),multiply((0,1),(1,0)))
    def test_validation(self):
        for g in ((4,0),(0,2),(True,0)):
            with self.assertRaises(ValueError):
                decompose(g)
        with self.assertRaises(ValueError):
            reconstruct((0,0),2)
