import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("exact",Path(__file__).with_name("exact.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class ExactTests(unittest.TestCase):
    def test_normal(self):
        c=m.certify("@@@SKKS")
        self.assertEqual((c["status"],c["result"],c["steps"]),("NORMAL","S",2))
        self.assertTrue(m.verify(c))
    def test_independent_rules(self):
        self.assertTrue(m.check_step("@@KSK","S"))
        self.assertTrue(m.check_step("@@@SKKS","@@KS@KS"))
        self.assertFalse(m.check_step("@@KSK","K"))
    def test_pause(self):
        c=m.certify("@@@SKKS",1)
        self.assertEqual(c["status"],"PAUSED")
        self.assertTrue(m.verify(c))
    def test_cap(self):
        c=m.certify("@@@SKKS",10,5)
        self.assertEqual(c["status"],"CAP_EXCEEDED")
        self.assertTrue(m.verify(c))
    def test_tamper_even_with_rehashed_certificate(self):
        c=m.certify("@@@SKKS")
        c["trace"][0]["after"]="K"
        c["sha256"]=m.sha({k:v for k,v in c.items() if k!="sha256"})
        self.assertFalse(m.verify(c))
    def test_invalid(self):
        with self.assertRaises(ValueError):
            m.certify("@S")
if __name__=="__main__":unittest.main()
