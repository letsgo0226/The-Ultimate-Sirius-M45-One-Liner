import unittest
from itertools import product
from fcvoc import mirror,shift,fourier,spectral_shift,inverse

class TestFCVOC(unittest.TestCase):
    def test_exact_conjugacy(self):
        for v in product(range(-2,3),repeat=4):
            self.assertEqual(mirror(mirror(v)),v)
            self.assertEqual(inverse(fourier(v)),v)
            self.assertEqual(fourier(mirror(v)),mirror(fourier(v)))
            for d in (-1,1):
                self.assertEqual(mirror(shift(mirror(v),d)),shift(v,-d))
                self.assertEqual(fourier(shift(v,d)),spectral_shift(fourier(v),d))
    def test_bad_spectrum(self):
        with self.assertRaises(ValueError):
            inverse(((1,0),(0,0),(0,0),(0,0)))
