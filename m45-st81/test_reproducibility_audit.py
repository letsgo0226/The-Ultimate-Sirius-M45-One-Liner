import importlib.util
import hashlib
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st81",Path(__file__).with_name("reproducibility_audit.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestAudit(unittest.TestCase):
    def test_digest(self):
        self.assertEqual(m.digest(b"abc"),hashlib.sha256(b"abc").hexdigest())
    def test_cases_unique(self):
        self.assertEqual(len(m.CASES),11)
        self.assertEqual(len({name for name,_,_ in m.CASES}),len(m.CASES))
        for _,path,_ in m.CASES:
            self.assertTrue((m.ROOT/path).is_file())
    def test_one_stage_repeatable(self):
        _,a=m.run_once("m45-st64/frame_switch.py",[])
        _,b=m.run_once("m45-st64/frame_switch.py",[])
        self.assertEqual(a,b)
if __name__=="__main__":unittest.main()
