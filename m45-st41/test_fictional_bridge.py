import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("bridge",Path(__file__).with_name("fictional_bridge.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class FictionalBridgeTests(unittest.TestCase):
    def test_valid(self):
        f=m.create_fragment()
        self.assertTrue(m.verify(f))
        self.assertIn("不能證明",m.narrative(f))
    def test_tampered(self):
        f=m.create_fragment()
        f["memory_text"]="changed"
        self.assertFalse(m.verify(f))
    def test_rehashed_semantic_tamper(self):
        f=m.create_fragment()
        f["ontology"]="REAL_CONSCIOUSNESS"
        f["sha256"]=m.sha({k:v for k,v in f.items() if k!="sha256"})
        self.assertFalse(m.verify(f))
    def test_year_order(self):
        with self.assertRaises(ValueError):m.create_fragment(2026,2112)
if __name__=="__main__":unittest.main()
