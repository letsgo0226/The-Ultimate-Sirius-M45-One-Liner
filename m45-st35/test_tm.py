import importlib.util
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location("st35",Path(__file__).with_name("tm.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestFixedTable(unittest.TestCase):
    def test_all_36(self):
        args=("S","K","@SS","@SK","@KS","@KK")
        for x in args:
            for y in args:
                with self.subTest(x=x,y=y):
                    expr="@@K"+x+y
                    result=m.run(expr)
                    self.assertEqual(result["status"],"HALT")
                    self.assertEqual(result["tape"],x)
                    self.assertTrue(m.verify(expr,result))
    def test_reject_outside_family(self):
        for expr in ("@@KSSS","@@KS","@@K@S@SKK","@@SSK"):
            self.assertEqual(m.run(expr)["status"],"REJECT")
    def test_pause_and_tamper(self):
        result=m.run("@@K@SK@KS",2)
        self.assertEqual(result["status"],"PAUSE")
        full=m.run("@@K@SK@KS")
        full["trace"][0][3]="K"
        self.assertFalse(m.verify("@@K@SK@KS",full))
if __name__=="__main__":
    unittest.main()
