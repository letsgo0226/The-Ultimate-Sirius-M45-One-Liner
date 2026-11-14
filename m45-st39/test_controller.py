import importlib.util
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location("st39",Path(__file__).with_name("controller.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ControllerTests(unittest.TestCase):
    def test_reaches_exact_normal_form(self):
        state,decisions=m.run(m.ledger_mod.genesis("@@@SKKS"),m.policy())
        self.assertTrue(m.ledger_mod.verify(state))
        self.assertEqual(state["records"][-1]["certificate"]["result"],"S")
        self.assertEqual(decisions[-1],{"action":"STOP","reason":"NORMAL"})
    def test_batch_limit(self):
        state,decisions=m.run(m.ledger_mod.genesis("@@@SKKS"),m.policy(max_batches=1))
        self.assertEqual(len(state["records"]),1)
        self.assertEqual(decisions[-1]["reason"],"BATCH_LIMIT")
    def test_step_limit(self):
        state,decisions=m.run(m.ledger_mod.genesis("@@@SKKS"),m.policy(max_total_steps=1))
        self.assertEqual(decisions[-1]["reason"],"STEP_LIMIT")
    def test_invalid_ledger_blocked(self):
        state=m.ledger_mod.genesis("@@@SKKS")
        state["expression"]="K"
        self.assertEqual(m.inspect(state,m.policy())["action"],"BLOCK")
        with self.assertRaises(ValueError):m.run(state,m.policy())
    def test_resume_after_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"ledger.json"
            state=m.ledger_mod.genesis("@@@SKKS")
            m.ledger_mod.atomic_save(path,m.ledger_mod.advance(state,1))
            resumed,decisions=m.run(m.ledger_mod.load(path),m.policy())
            self.assertEqual(resumed["records"][-1]["certificate"]["result"],"S")
            self.assertEqual(decisions[-1]["reason"],"NORMAL")
    def test_invalid_policy(self):
        with self.assertRaises(ValueError):m.policy(steps_per_batch=0)

if __name__=="__main__":unittest.main()
