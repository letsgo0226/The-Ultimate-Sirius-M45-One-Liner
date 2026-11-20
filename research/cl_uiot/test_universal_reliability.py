import unittest
from fractions import Fraction as Q
from universal_reliability import *
from qec_minimum_resources import plan
from zeta_reliability import allocation

class UniversalTests(unittest.TestCase):
    def test_envelope(self):
        self.assertEqual(envelope(Q(1,100),9),Q(1,1000))
    def test_telescoping(self):
        e=Q(1,100)
        a=[telescoping_allocation(e,t) for t in range(20)]
        self.assertEqual(audit_prefix(e,a),e/21)
        self.assertTrue(all(x<=envelope(e,t) for t,x in enumerate(a)))
    def test_lower(self):
        p,e=Q(1,20),Q(1,100)
        for t in (0,10,100):
            n=necessary_depth(p,e,t,6)
            r=plan(p,allocation(e,t),5**6)
            self.assertTrue(r["certified"])
            self.assertLessEqual(5**n,r["data_qubits"])
    def test_unresolved(self):
        self.assertIsNone(necessary_qubits(Q(1,20),Q(1,100),100,0))
    def test_nonmonotone(self):
        with self.assertRaises(ValueError):audit_prefix(1,[Q(1,4),Q(1,2)])
    def test_overspend(self):
        with self.assertRaises(ValueError):audit_prefix(1,[Q(3,4),Q(3,4)])
    def test_invalid(self):
        with self.assertRaises(ValueError):envelope(1,-1)
