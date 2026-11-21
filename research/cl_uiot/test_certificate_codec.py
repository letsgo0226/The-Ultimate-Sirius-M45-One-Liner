import unittest
from fractions import Fraction as Q
from correspondence import produce,verify
from certificate_codec import G,D,encode,decode,serialize

class TestCertificateCodec(unittest.TestCase):
    def test_bytes(self):
        for b in (b"",bytes(range(256)),b"\x00\xff"*2048):
            self.assertEqual(D(G(b)),b)
        for n in (0,True,2,257,514):
            with self.assertRaises(ValueError):
                D(n)
    def test_records(self):
        for a in range(-8,9):
            for b in range(-8,9):
                r=produce(Q(a,3),Q(b,7))
                self.assertEqual(decode(encode(r)),r)
                self.assertTrue(verify(decode(encode(r))))
    def test_noncanonical(self):
        b=serialize(produce(2,0))
        for bad in (b+b" ",b.replace(b'"q":[2,1]',b'"q":[4,2]'),b"{}",b"null"):
            self.assertNotEqual(bad,b)
            with self.assertRaises(ValueError):
                decode(G(bad))
