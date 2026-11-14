import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("tm34",Path(__file__).with_name("tm.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class TestAtomicK(unittest.TestCase):
    def test_all_four(self):
        for x in "SK":
            for y in "SK":
                with self.subTest(x=x,y=y):
                    src="@@K"+x+y
                    cert=m.simulate(src)
                    self.assertEqual(cert["status"],"HALT")
                    self.assertEqual(cert["tape"],x)
                    self.assertTrue(m.verify(src,cert))
    def test_reject(self):
        for src in ("@@KSSS","@@SSK","@@KS","@@KSK@"):
            self.assertEqual(m.simulate(src)["status"],"REJECT")
    def test_pause(self):
        self.assertEqual(m.simulate("@@KSK",2)["status"],"PAUSE")
    def test_tamper(self):
        c=m.simulate("@@KSK")
        c["trace"][0]["write"]="S"
        self.assertFalse(m.verify("@@KSK",c))
if __name__=="__main__":
    unittest.main()
