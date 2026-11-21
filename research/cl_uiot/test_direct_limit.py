import unittest,itertools
from fractions import Fraction as Q
from direct_limit import apply,embed,norm_squared,coupling

class TestDirectLimit(unittest.TestCase):
    def test_prefixes(self):
        for n in range(1,9):
            for v in itertools.product((-1,0,1),repeat=n):
                w=apply(v)
                self.assertEqual(apply(w),v)
                self.assertEqual(apply(embed(v)),embed(w))
                self.assertLessEqual(norm_squared(w),4*norm_squared(v))
    def test_active(self):
        for k in range(1,33):
            v=(0,)*(2*k-1)+(1,)
            self.assertEqual(apply(v)[-2:],(coupling(k),1))
    def test_invalid(self):
        for v in ([],[0.0],[True]):
            with self.assertRaises(ValueError):
                apply(v)
        with self.assertRaises(ValueError):
            coupling(0)
