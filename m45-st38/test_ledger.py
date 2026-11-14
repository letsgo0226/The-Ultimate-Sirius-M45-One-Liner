import importlib.util
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location("st38",Path(__file__).with_name("ledger.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class VerifiedPersistence(unittest.TestCase):
    def test_resume_and_replay(self):
        start=m.genesis("@@@SKKS")
        first=m.advance(start,1)
        self.assertEqual(first["records"][-1]["certificate"]["status"],"PAUSED")
        second=m.advance(first,1)
        self.assertEqual(second["records"][-1]["certificate"]["result"],"S")
        self.assertEqual(second["records"][-1]["certificate"]["status"],"NORMAL")
        self.assertTrue(m.verify(second))
        with self.assertRaises(ValueError):m.advance(second,1)
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"ledger.json"
            m.atomic_save(path,m.genesis("@@@SKKS"))
            m.atomic_save(path,m.advance(m.load(path),1))
            m.atomic_save(path,m.advance(m.load(path),1))
            self.assertEqual(m.load(path)["records"][-1]["certificate"]["result"],"S")
    def test_tampering_even_when_rehashed(self):
        ledger=m.advance(m.genesis("@@@SKKS"),1)
        ledger["records"][0]["certificate"]["trace"][0]["after"]="K"
        item=ledger["records"][0]
        item["certificate"]["sha256"]=m.exact.sha({k:v for k,v in item["certificate"].items() if k!="sha256"})
        item["sha256"]=m.exact.sha({k:v for k,v in item.items() if k!="sha256"})
        ledger["sha256"]=m.exact.sha({k:v for k,v in ledger.items() if k!="sha256"})
        self.assertFalse(m.verify(ledger))
    def test_reorder(self):
        ledger=m.advance(m.advance(m.genesis("@@@SKKS"),1),1)
        ledger["records"].reverse()
        ledger["sha256"]=m.exact.sha({k:v for k,v in ledger.items() if k!="sha256"})
        self.assertFalse(m.verify(ledger))
    def test_invalid_budget(self):
        with self.assertRaises(ValueError):m.advance(m.genesis("S"),0)

if __name__=="__main__":unittest.main()
