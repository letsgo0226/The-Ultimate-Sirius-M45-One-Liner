import unittest,json
from certificate_codec import G,D,encode,decode,serialize,LIMIT
from correspondence import produce

class EncodingIntegrityTest(unittest.TestCase):
    def test_all_short_words(self):
        seen={G(b"")}
        for a in range(256):
            b=bytes([a])
            g=G(b)
            self.assertNotIn(g,seen)
            seen.add(g)
            self.assertEqual(D(g),b)
            for c in range(256):
                b=bytes([a,c])
                g=G(b)
                self.assertEqual(g,257**2+(a+1)*257+c+1)
                self.assertNotIn(g,seen)
                seen.add(g)
                self.assertEqual(D(g),b)
        self.assertEqual(len(seen),65793)
    def test_integer_domain(self):
        for n in range(1,4096):
            try:
                b=D(n)
            except ValueError:
                self.assertFalse(n==1 or 258<=n<=513)
            else:
                self.assertEqual(G(b),n)
    def test_limits(self):
        b=bytes(range(256))*16
        self.assertEqual(D(G(b)),b)
        for n in (True,0,-1,2,257,G(b)*257+1,G(b)*257):
            with self.assertRaises(ValueError):
                D(n)
        with self.assertRaises(ValueError):
            G(b+b"x")
    def test_noncanonical(self):
        r=produce(2,1)
        b=serialize(r)
        self.assertEqual(decode(encode(r)),r)
        for alt in (b+b" ",b" "+b,b'{"state":"invalid",'+b[1:]):
            with self.assertRaises(ValueError):
                decode(G(alt))
        obj=json.loads(b)
        obj["residual"]={"q":[10,2]}
        with self.assertRaises(ValueError):
            decode(G(json.dumps(obj,sort_keys=True,separators=(",",":")).encode("ascii")))
    def test_not_authentication(self):
        a,b=produce(2,1),produce(2,0)
        self.assertNotEqual(encode(a),encode(b))
        self.assertEqual(decode(encode(b)),b)
