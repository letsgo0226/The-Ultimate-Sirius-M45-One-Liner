import unittest
from itertools import combinations
from qec_perfect_5qubit import *

class PerfectCodeTests(unittest.TestCase):
    def test_commute(self):
        self.assertTrue(all(parity(a,b)==0 for a,b in combinations(GENERATORS,2)))
    def test_independence(self):
        self.assertEqual(len(stabilize()),16)
    def test_syndromes(self):
        self.assertEqual(len(table()),16)
    def test_recovery(self):
        self.assertTrue(all(residual(p)=="IIIII" for p in errors()))
    def test_kl(self):
        self.assertTrue(all(any(syndrome(multiply_labels(a,b))) for a,b in combinations(errors(),2)))
    def test_distance(self):
        self.assertEqual(distance(),3)
    def test_double_failure(self):
        self.assertNotIn(residual("XXIII"),stabilize())
