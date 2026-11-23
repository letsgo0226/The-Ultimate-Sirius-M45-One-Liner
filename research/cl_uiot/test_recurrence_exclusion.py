import unittest
from itertools import product
from recurrence_exclusion import *
class RecurrenceTests(unittest.TestCase):
    def test_grid(self):
        count=0
        for z in product((Q(5,6),Q(9,10),Q(1)),repeat=3):
            try:from_bloch(*z)
            except ValueError:continue
            r=certificate(z)
            self.assertGreaterEqual(r["next_minimum"],r["lower"])
            self.assertTrue(r["vertex_basin"])
            count+=1
        self.assertGreater(count,0)
    def test_endpoint(self):
        for a in (Q(4,5),Q(5,6),Q(9,10),Q(1)):
            self.assertEqual(endpoint_gap(a),(10*a*a-5*a**4-1)/4-scalar(a))
            self.assertGreaterEqual(endpoint_gap(a),0)
    def test_vertex(self):self.assertEqual(certificate((1,1,1))["lower"],1)
    def test_signs(self):
        a=Q(9,10)
        self.assertEqual(certificate((a,a,a)),certificate((a,-a,-a)))
    def test_invalid(self):
        with self.assertRaises(ValueError):certificate((Q(4,5),)*3)
