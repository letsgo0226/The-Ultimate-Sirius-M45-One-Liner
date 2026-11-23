import unittest
from itertools import product
from abelian_fourier import transform,inverse,translate,laplacian,spectral_laplacian

class TestAbelianFourier(unittest.TestCase):
    def test_exhaustive(self):
        for a in product((-1,0,1),repeat=8):
            w=transform(a)
            self.assertEqual(inverse(w),a)
            self.assertEqual(transform(w),tuple(8*v for v in a))
            self.assertEqual(sum(v*v for v in w),8*sum(v*v for v in a))
            self.assertEqual(transform(laplacian(a)),spectral_laplacian(w))
    def test_translation(self):
        for n in range(1,7):
            a=tuple(x*x-3*x for x in range(1<<n))
            w=transform(a)
            for g in range(len(a)):
                self.assertEqual(transform(translate(a,g)),
                    tuple((-1)**((k&g).bit_count()%2)*v for k,v in enumerate(w)))
    def test_direct(self):
        a=(3,-7,2,11,0,1,4,-2)
        self.assertEqual(transform(a),tuple(sum((-1)**((x&k).bit_count()%2)*v
            for x,v in enumerate(a)) for k in range(len(a))))
    def test_validation(self):
        for a in ((),(1,2,3),(1,True),(0,)*8192):
            with self.assertRaises(ValueError):
                transform(a)
        with self.assertRaises(ValueError):
            inverse((1,0))
