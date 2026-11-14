import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path

spec=importlib.util.spec_from_file_location("g2112",Path(__file__).with_name("g2112.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PrimeOperatorTests(unittest.TestCase):
    def test_first_primes(self):
        self.assertEqual(m.primes(7),[2,3,5,7,11,13,17])
    def test_rotation_exact(self):
        original=m.state(3,[1,0,0])
        rotated=m.apply(original,"rotate")
        self.assertEqual(rotated,{"2":"0","3":"1","5":"0"})
        self.assertEqual(m.norm2(rotated),"1")
    def test_rational_scale(self):
        initial=m.state(2,["1/3","2/3"])
        self.assertEqual(m.apply(initial,"scale","3/2"),{"2":"1/2","3":"1"})
    def test_difference(self):
        self.assertEqual(m.apply(m.state(2,[1,0]),"difference"),{"2":"1","3":"-1"})
    def test_certificate(self):
        for op in ("identity","rotate","scale","difference"):
            with self.subTest(op=op):
                self.assertTrue(m.verify(m.experiment(5,op,"1/2")))
    def test_tamper_rehashed(self):
        cert=m.experiment()
        cert["final"]["2"]="999"
        cert["sha256"]=m.digest({k:v for k,v in cert.items() if k!="sha256"})
        self.assertFalse(m.verify(cert))
    def test_bridge_is_not_time_travel(self):
        b=m.bridge("Hello from 2026")
        self.assertEqual(b["target_year"],2112)
        self.assertIn("NO_TIME_TRAVEL",b["semantics"])
    def test_invalid(self):
        with self.assertRaises(ValueError):m.primes(0)
        with self.assertRaises(ValueError):m.rational(0.1)

if __name__=="__main__":unittest.main()
