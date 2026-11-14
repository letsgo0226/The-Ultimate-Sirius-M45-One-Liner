import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("pocket",Path(__file__).with_name("pocket.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PocketTests(unittest.TestCase):
    def test_primes(self):
        self.assertEqual(m.first_primes(5),[2,3,5,7,11])
    def test_exact_roundtrip(self):
        for values in ([0],[1,0,2],[64,64],[0]*16):
            with self.subTest(values=values):
                self.assertEqual(m.decode(m.encode(list(values)),len(values)),list(values))
    def test_projection_all_positive_integers(self):
        self.assertEqual(m.project(1,3),[0,0,0])
        self.assertEqual(m.project(7,3),[0,0,0])
        self.assertEqual(m.project(72,3),[3,2,0])
    def test_noncanonical_rejected(self):
        for n in (1,7,14,420):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):m.decode(n,3)
    def test_pocket(self):
        record=m.pocket_record("fictional friend",[1,0,2],"hello")
        self.assertTrue(m.verify(record))
        self.assertEqual(m.retrieve([record],int(record["godel_number"])),[record])
    def test_rehashed_tamper(self):
        record=m.pocket_record("friend",[1,0],"hello")
        record["godel_number"]="123"
        record["sha256"]=m.digest({k:v for k,v in record.items() if k!="sha256"})
        self.assertFalse(m.verify(record))
    def test_invalid(self):
        with self.assertRaises(ValueError):m.encode([-1])
        with self.assertRaises(ValueError):m.project(0,3)
        with self.assertRaises(ValueError):m.retrieve([{"invalid":True}],10)

if __name__=="__main__":unittest.main()
