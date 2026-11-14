import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("advance", ROOT / "advance.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestPersistentTM(unittest.TestCase):
    def test_successor_and_pause(self):
        s = json.loads((ROOT / "state.json").read_text())
        m.validate(s)
        paused, first = m.execute(s, 2)
        self.assertEqual(first["status"], "PAUSED")
        self.assertEqual(paused["head"], 2)
        done, second = m.execute(paused, 100)
        self.assertEqual(second["status"], "HALTED")
        self.assertEqual(done["cells"], {"0": "1", "1": "1", "2": "1", "3": "1"})
        self.assertEqual(done["steps"], 4)
        self.assertEqual(second["previous_state_sha256"], m.sha(paused))

    def test_reject_invalid(self):
        s = json.loads((ROOT / "state.json").read_text())
        s["cells"]["1"] = "X"
        with self.assertRaises(ValueError):
            m.validate(s)

    def test_bounded_batch(self):
        s = json.loads((ROOT / "state.json").read_text())
        with self.assertRaises(ValueError):
            m.execute(s, 1001)

if __name__ == "__main__":
    unittest.main()
