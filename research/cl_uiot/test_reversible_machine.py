import unittest
from itertools import product
from reversible_machine import step,backward,encode,decode,spectral_step,spectral_backward

class TestReversibleMachine(unittest.TestCase):
    def test_exhaustive(self):
        for n in (1,2,4,8):
            for t in product((0,1),repeat=n):
                for q,h in product(range(2),range(n)):
                    s=(q,h,t)
                    self.assertEqual(backward(step(s)),s)
                    self.assertEqual(step(backward(s)),s)
                    w=encode(s)
                    self.assertEqual(decode(w),s)
                    self.assertEqual(spectral_step(w),encode(step(s)))
                    self.assertEqual(spectral_backward(w),encode(backward(s)))
                    self.assertEqual(spectral_backward(spectral_step(w)),w)
                    self.assertEqual(spectral_step(spectral_backward(w)),w)
    def test_history_free_roundtrip(self):
        s=(0,0,(1,0,1,1,0,0,0,1))
        w=encode(s)
        for _ in range(100):
            w=spectral_step(w)
        for _ in range(100):
            w=spectral_backward(w)
        self.assertEqual(decode(w),s)
    def test_invalid(self):
        for s in ((2,0,(0,)),(0,1,(0,)),(0,0,(2,)),(0,0,(0,0,0))):
            with self.assertRaises(ValueError):
                step(s)
        with self.assertRaises(ValueError):
            spectral_step((0,0,(1,0)))
