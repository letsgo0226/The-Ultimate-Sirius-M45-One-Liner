import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st47",Path(__file__).with_name("state_transition.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class StateTests(unittest.TestCase):
    def test_init(self):
        d=m.initial()
        self.assertTrue(m.verify(d))
        self.assertEqual(d["revision"],0)
    def test_cas_and_stop(self):
        d=m.initial()
        d,r=m.advance(d,0,"remember",{"name":"Doraemon","values":[1,0,2],"message":"Help others"})
        self.assertEqual(r["code"],"1500")
        self.assertEqual(d["revision"],1)
        with self.assertRaises(ValueError):m.advance(d,0,"tick")
        d,_=m.advance(d,1,"tick")
        d,_=m.advance(d,2,"stop")
        self.assertEqual(d["revision"],3)
        with self.assertRaises(ValueError):m.advance(d,3,"tick")
    def test_read_only_no_revision(self):
        d=m.initial()
        same,_=m.advance(d,0,"inspect")
        self.assertIs(same,d)
    def test_tampering(self):
        d=m.initial()
        d["revision"]=4
        self.assertFalse(m.verify(d))
    def test_invalid(self):
        with self.assertRaises(ValueError):m.advance(m.initial(),0,"init")
        with self.assertRaises(ValueError):m.advance(m.initial(),True,"tick")

if __name__=="__main__":unittest.main()
