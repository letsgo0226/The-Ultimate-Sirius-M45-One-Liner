import unittest
from m45_st89 import C,G,D,E,halt
class Tests(unittest.TestCase):
 def test_roundtrip(self):
  for b in (b"",b"LOVE",bytes(range(256))):self.assertEqual(D(G(b)),b)
 def test_entropy(self):
  self.assertEqual(E([]),"0");self.assertEqual(E([1,1]),"0")
 def test_halt(self):
  r=halt(C);self.assertEqual(r["H_final_exact"],"0");self.assertEqual(r["status"],"HALT")
if __name__=="__main__":unittest.main()
