import importlib.util
import json
import unittest
from pathlib import Path

PATH = Path(__file__).with_name("verify_journal.py")
spec = importlib.util.spec_from_file_location("verify_journal", PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestReplay(unittest.TestCase):
    def test_genesis(self):
        self.assertEqual(m.replay([]), m.genesis())
        self.assertEqual(m.verify_files()["status"], "PASS")

    def test_replay_valid_batch(self):
        state = m.genesis()
        records = []
        for i in range(4):
            read = state["cells"].get(str(state["head"]), "_")
            write, move, nxt = m.TABLE["transitions"][state["state"]][read]
            prev = m.digest(state)
            step = {"q": state["state"], "h": state["head"], "read": read,
                    "write": write, "move": move, "next": nxt}
            state["cells"][str(state["head"])] = write
            state["head"] += {"L": -1, "R": 1, "N": 0}[move]
            state["state"] = nxt
            state["steps"] += 1
            state["generation"] += 1
            rec = {"generation": i + 1, "previous_state_sha256": prev,
                   "next_state_sha256": m.digest(state), "table_sha256": m.digest(m.TABLE),
                   "transitions": [step],
                   "status": "HALTED" if nxt == "HALT" else "PAUSED"}
            rec["record_sha256"] = m.digest(rec)
            records.append(rec)
        self.assertEqual(m.replay(records), state)
        records[0]["transitions"][0]["write"] = "_"
        with self.assertRaises(ValueError):
            m.replay(records)

    def test_tamper_state(self):
        fake = dict(m.genesis())
        fake["head"] = 100
        self.assertNotEqual(fake, m.replay([]))

if __name__ == "__main__":
    unittest.main()
