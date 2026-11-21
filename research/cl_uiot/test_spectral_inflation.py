import unittest
from itertools import product
from abelian_fourier import transform,laplacian
from spectral_inflation import embed,join,split,spectral_join,spectral_split,spectral_embed,recover

class TestSpectralInflation(unittest.TestCase):
    def test_exhaustive(self):
        for f in product((-1,0,1),repeat=8):
            a,b=split(f)
            A,B=transform(a),transform(b)
            w=transform(f)
            self.assertEqual(spectral_join(A,B),w)
            self.assertEqual(spectral_split(w),(A,B))
            self.assertEqual(recover(w),(a,b))
            self.assertEqual(join(*recover(w)),f)
            self.assertEqual(transform(embed(a)),spectral_embed(A))
            self.assertEqual(sum(v*v for v in w),8*sum(v*v for v in f))
    def test_laplacian_blocks(self):
        for n in range(1,8):
            a=tuple(range(1<<n))
            b=tuple(-x*x for x in a)
            l,r=split(laplacian(join(a,b)))
            self.assertEqual(l,tuple(v+x-y for v,x,y in zip(laplacian(a),a,b)))
            self.assertEqual(r,tuple(v+y-x for v,x,y in zip(laplacian(b),a,b)))
    def test_validation(self):
        for a,b in (((1,),(1,2)),((0,)*4096,(0,)*4096)):
            with self.assertRaises(ValueError):
                join(a,b)
        with self.assertRaises(ValueError):
            spectral_split((1,0))
        with self.assertRaises(ValueError):
            recover((2,0,0,0))
        with self.assertRaises(ValueError):
            split((1,))
