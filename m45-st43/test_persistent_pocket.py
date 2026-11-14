import importlib.util
import tempfile
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st43",Path(__file__).with_name("persistent_pocket.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PersistentPocketTests(unittest.TestCase):
    def test_append_retrieve(self):
        original=m.genesis()
        r=m.pocket.pocket_record("fictional Doraemon",[1,0,2],"Help others")
        state=m.append(original,r)
        self.assertTrue(m.verify(state))
        self.assertEqual(m.lookup(state,int(r["godel_number"])),[r])
        self.assertEqual(len(original["events"]),0)
    def test_disk_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"pocket.json"
            m.save(path,m.genesis())
            r=m.pocket.pocket_record("friend",[0,1],"hello")
            m.save(path,m.append(m.load(path),r))
            self.assertEqual(len(m.load(path)["events"]),1)
    def test_semantic_tamper_after_rehash(self):
        state=m.append(m.genesis(),m.pocket.pocket_record("friend",[1,0],"hello"))
        item=state["events"][0]
        item["record"]["godel_number"]="999"
        item["record"]["sha256"]=m.pocket.digest({k:v for k,v in item["record"].items() if k!="sha256"})
        item["sha256"]=m.pocket.digest({k:v for k,v in item.items() if k!="sha256"})
        state["sha256"]=m.pocket.digest({k:v for k,v in state.items() if k!="sha256"})
        self.assertFalse(m.verify(state))
    def test_reorder(self):
        state=m.genesis()
        for i in range(2):
            state=m.append(state,m.pocket.pocket_record(str(i),[i],"hello"))
        state["events"].reverse()
        state["sha256"]=m.pocket.digest({k:v for k,v in state.items() if k!="sha256"})
        self.assertFalse(m.verify(state))
    def test_limit(self):
        original=m.MAX_RECORDS
        try:
            m.MAX_RECORDS=1
            state=m.append(m.genesis(),m.pocket.pocket_record("one",[0],"hi"))
            with self.assertRaises(ValueError):
                m.append(state,m.pocket.pocket_record("two",[1],"hi"))
        finally:
            m.MAX_RECORDS=original
    def test_invalid_record(self):
        with self.assertRaises(ValueError):
            m.append(m.genesis(),{"fake":True})

if __name__=="__main__":unittest.main()
