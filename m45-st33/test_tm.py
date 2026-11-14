import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("tm",Path(__file__).with_name("tm.py"))
tm=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tm)

class FixedDeltaTests(unittest.TestCase):
    def test_k_redex(self):
        result=tm.simulate("@@KSK")
        self.assertEqual(result["status"],"HALT")
        self.assertEqual(result["tape"],"S")
        self.assertEqual(result["steps"],11)
        self.assertTrue(tm.verify("@@KSK",result))
    def test_reject_other(self):
        self.assertEqual(tm.simulate("@@@SKKS")["status"],"REJECT")
        self.assertEqual(tm.simulate("@@KSS")["status"],"REJECT")
    def test_budget(self):
        self.assertEqual(tm.simulate("@@KSK",2)["status"],"PAUSE")
    def test_tamper(self):
        result=tm.simulate("@@KSK")
        result["trace"][0]["write"]="K"
        self.assertFalse(tm.verify("@@KSK",result))
if __name__=="__main__":
    unittest.main()
