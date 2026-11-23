import unittest
from fractions import Fraction as Q
from itertools import product
from abelian_fourier import laplacian,transform
from spectral_regularization import project,resolvent,regularized,decompose

class TestRegularization(unittest.TestCase):
    def test_decomposition(self):
        for f in product((-1,0,1),repeat=4):
            parts=decompose(f)
            self.assertEqual(tuple(map(sum,zip(*parts))),f)
            self.assertEqual(tuple(sum(2*j*p[i] for j,p in enumerate(parts)) for i in range(4)),laplacian(f))
            for j,p in enumerate(parts):
                for k,r in enumerate(parts):
                    if j!=k:
                        self.assertEqual(sum(x*y for x,y in zip(p,r)),0)
                self.assertEqual(regularized(f,2*j,2*j),p)
    def test_resolvent(self):
        f=(1,2,4,8,16,32,64,128)
        for lam in (0,2,4,6):
            p=project(f,lam)
            for m in (4,16,64,256):
                z=Q(lam)+Q(1,m)
                v=resolvent(f,z)
                n=3
                self.assertEqual(tuple((n-z)*x-sum(v[i^(1<<j)] for j in range(n)) for i,x in enumerate(v)),f)
                err=tuple(x-y for x,y in zip(regularized(f,lam,z),p))
                self.assertLessEqual(sum(x*x for x in err),Q(1,m*m)*sum(x*x for x in f))
    def test_poles(self):
        with self.assertRaises(ValueError):
            resolvent((1,2),0)
        with self.assertRaises(ValueError):
            regularized((1,2),1,1)
        with self.assertRaises(ValueError):
            regularized((1,2),0,2)
