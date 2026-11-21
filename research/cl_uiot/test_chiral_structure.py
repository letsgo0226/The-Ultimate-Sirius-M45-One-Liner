import unittest
from itertools import product,permutations
from chiral_structure import transport,orbit

class TestChiralStructure(unittest.TestCase):
    def test_conjugacy(self):
        for t in product(range(3),repeat=3):
            for p in permutations(range(3)):
                u=transport(t,p)
                self.assertEqual(tuple(u[p[x]] for x in range(3)),
                                 tuple(p[t[x]] for x in range(3)))
    def test_orbit(self):
        t=(0,0,1)
        g=((1,0,2),(0,2,1))
        a,complete=orbit(t,g)
        self.assertTrue(complete)
        self.assertEqual(len(a),6)
        self.assertEqual(orbit(t,g,1),((t,),False))
        self.assertEqual(orbit(t,()),((t,),True))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            transport((0,1),(0,0))
