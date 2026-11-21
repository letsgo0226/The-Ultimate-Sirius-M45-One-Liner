import unittest
from itertools import product
from fcvoc_machine import encode,step,reflect
from fcvoc_spectral import step as spectral,read

class TestNativeSpectral(unittest.TestCase):
    def test_all_configurations(self):
        for q,h,t in product(range(3),range(4),product(range(2),repeat=4)):
            s=(q,h,t)
            for d in (-1,1):
                self.assertEqual(read(encode(s)[2],h),t[h])
                a,b=s,encode(s)
                for _ in range(32):
                    a,b=step(a,d),spectral(b,d)
                    self.assertEqual(encode(a),b)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            read(((1,0),(0,0),(0,0),(0,0)),0)
        with self.assertRaises(ValueError):
            spectral(encode((0,0,(0,0,0,0))),0)
