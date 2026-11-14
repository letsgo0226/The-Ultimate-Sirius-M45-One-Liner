import importlib.util
import unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("st45",Path(__file__).with_name("unified_machine.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class UnifiedTests(unittest.TestCase):
    def test_memory_and_recall(self):
        machine=m.initialize()
        machine,result=m.transition(machine,"remember",{"name":"Doraemon (fiction)","values":[1,0,2],"message":"Help others"})
        self.assertEqual(result["code"],"1500")
        self.assertTrue(m.verify(machine))
        same,found=m.transition(machine,"recall",{"code":1500})
        self.assertIs(same,machine)
        self.assertEqual(len(found["matches"]),1)
    def test_tick_stop(self):
        machine=m.initialize()
        machine,_=m.transition(machine,"tick")
        self.assertTrue(m.verify(machine))
        machine,_=m.transition(machine,"stop")
        with self.assertRaises(ValueError):m.transition(machine,"tick")
        self.assertTrue(m.verify(machine))
    def test_no_silent_rebinding(self):
        machine,_=m.transition(m.initialize(),"tick")
        with self.assertRaises(ValueError):
            m.transition(machine,"remember",{"name":"friend","values":[0],"message":"hello"})
    def test_invalid_action(self):
        with self.assertRaises(ValueError):m.transition(m.initialize(),"network")
    def test_tampered_machine(self):
        machine=m.initialize()
        machine["controller"]["enabled"]=False
        self.assertFalse(m.verify(machine))
    def test_inspect(self):
        _,result=m.transition(m.initialize(),"inspect")
        self.assertEqual(result,{"verified":True,"enabled":True,"records":0,"ticks":0})

if __name__=="__main__":unittest.main()
