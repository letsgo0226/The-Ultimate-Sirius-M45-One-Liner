import importlib.util
import unittest
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
g=load("st40_regression",Path("m45-st40/g2112.py"))
u=load("st45_regression",Path("m45-st45/unified_machine.py"))

class CrossStageRegression(unittest.TestCase):
    def test_fraction_supported(self):
        self.assertEqual(g.rational(Fraction(1,2)),Fraction(1,2))
        self.assertEqual(g.norm2(g.state(3,[1,0,0])),"1")
    def test_operator_certificate(self):
        for operator in ("identity","rotate","scale","difference"):
            with self.subTest(operator=operator):
                record=g.experiment(3,operator,"1/2")
                self.assertTrue(g.verify(record))
    def test_unified_lifecycle(self):
        state=u.initialize()
        self.assertTrue(u.verify(state))
        state,receipt=u.transition(state,"remember",
            {"name":"Doraemon fictional memory","values":[1,0,2],"message":"Friendship"})
        self.assertEqual(receipt["code"],"1500")
        _,found=u.transition(state,"recall",{"code":1500})
        self.assertEqual(len(found["matches"]),1)
        state,_=u.transition(state,"tick")
        state,_=u.transition(state,"stop")
        self.assertTrue(u.verify(state))
        with self.assertRaises(ValueError):u.transition(state,"tick")
    def test_reject_tampered_state(self):
        state=u.initialize()
        state["pocket"]["events"].append({"fake":True})
        self.assertFalse(u.verify(state))

if __name__=="__main__":unittest.main()
