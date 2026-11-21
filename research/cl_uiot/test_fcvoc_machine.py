import unittest
from itertools import product
from fcvoc_machine import step,reflect,encode,decode,spectral_step,run

class TestFCVOCMachine(unittest.TestCase):
    def test_all_states(self):
        for q,h,t in product(range(3),range(4),product(range(2),repeat=4)):
            s=(q,h,t)
            self.assertEqual(reflect(reflect(s)),s)
            self.assertEqual(decode(encode(s)),s)
            self.assertEqual(reflect(step(s)),step(reflect(s),-1))
            self.assertEqual(encode(step(s)),spectral_step(encode(s)))
            for n in (0,1,8,32):
                self.assertEqual(reflect(run(s,n)),run(reflect(s),n,-1))
    def test_halt_budget(self):
        s=(2,0,(0,0,0,0))
        self.assertEqual(run(s,1024),s)
        with self.assertRaises(ValueError):
            run(s,1025)
        self.assertEqual(step((1,0,(1,0,0,0)))[0],2)
