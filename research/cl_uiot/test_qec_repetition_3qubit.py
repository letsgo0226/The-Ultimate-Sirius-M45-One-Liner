import unittest
from fractions import Fraction as Q
from qec_repetition_3qubit import *
from quantum_entropy_2level import density

class QECTests(unittest.TestCase):
    def test_kl(self):
        self.assertTrue(correctable(MASKS))
    def test_kl_failure(self):
        self.assertFalse(correctable((0,7)))
    def test_each_error(self):
        for m in MASKS:
            self.assertEqual(decode(flip(encode(Q(3,4),Q(1,4)),m)),density(Q(3,4),Q(1,4)))
    def test_mixture(self):
        self.assertEqual(decode(noisy(Q(1,2),Q(1,2),[Q(1,4)]*4)),density(Q(1,2),Q(1,2)))
    def test_double_flip(self):
        self.assertEqual(decode(flip(encode(1,0),3)),density(0,0))
    def test_invalid(self):
        with self.assertRaises(ValueError):noisy(1,0,[1,1,0,0])
