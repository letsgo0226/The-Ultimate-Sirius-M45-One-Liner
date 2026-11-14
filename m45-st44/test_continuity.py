import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st44",Path(__file__).with_name("continuity.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.pocket=m.pocket.genesis()
    def test_verify_and_step(self):
        state=m.genesis(self.pocket)
        self.assertTrue(m.verify(state,self.pocket))
        state=m.step(state,self.pocket)
        self.assertTrue(m.verify(state,self.pocket))
        self.assertEqual(len(state["ticks"]),1)
    def test_stop_is_effective(self):
        stopped=m.stop(m.genesis(self.pocket),self.pocket)
        self.assertTrue(m.verify(stopped,self.pocket))
        with self.assertRaises(ValueError):m.step(stopped,self.pocket)
    def test_tamper_even_after_rehash(self):
        state=m.step(m.genesis(self.pocket),self.pocket)
        state["ticks"][0]["action"]="UNAUTHORIZED_ACTION"
        tick=state["ticks"][0]
        tick["sha256"]=m.hash_of({k:v for k,v in tick.items() if k!="sha256"})
        state["sha256"]=m.hash_of({k:v for k,v in state.items() if k!="sha256"})
        self.assertFalse(m.verify(state,self.pocket))
    def test_pocket_binding(self):
        state=m.genesis(self.pocket)
        different=m.pocket.append(self.pocket,m.pocket.pocket.pocket_record("friend",[1],"hello"))
        self.assertFalse(m.verify(state,different))
    def test_limit(self):
        original=m.MAX_TICKS
        try:
            m.MAX_TICKS=1
            state=m.step(m.genesis(self.pocket),self.pocket)
            with self.assertRaises(ValueError):m.step(state,self.pocket)
        finally:m.MAX_TICKS=original
if __name__=="__main__":unittest.main()
