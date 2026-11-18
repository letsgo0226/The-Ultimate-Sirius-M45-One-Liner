"""Read-only native verifier integration, pinned by the Git commit running CI."""
import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

st30 = load("cvoc_native_st30", "m45-st30/advance.py")
st38 = load("cvoc_native_st38", "m45-st38/ledger.py")
st43 = load("cvoc_native_st43", "m45-st43/persistent_pocket.py")
st44 = load("cvoc_native_st44", "m45-st44/continuity.py")
st47 = load("cvoc_native_st47", "m45-st47/state_transition.py")

class NativeVerification(unittest.TestCase):
    def test_st30_existing_state_readonly(self):
        state = json.loads((ROOT / "m45-st30/state.json").read_text())
        st30.validate(state)
        before = st30.sha(state)
        successor, record = st30.execute(state, 1)
        self.assertEqual(st30.sha(state), before)
        self.assertEqual(record["previous_state_sha256"], before)
        self.assertEqual(record["next_state_sha256"], st30.sha(successor))

    def test_st38_replay_and_tamper(self):
        ledger = st38.genesis("@@@SKKS", 10)
        self.assertTrue(st38.verify(ledger))
        ledger = st38.advance(ledger, 1)
        self.assertTrue(st38.verify(ledger))
        corrupted = copy.deepcopy(ledger)
        corrupted["records"][0]["previous"] = "INVALID"
        self.assertFalse(st38.verify(corrupted))

    def test_st43_native_memory(self):
        pocket = st43.genesis()
        self.assertTrue(st43.verify(pocket))
        broken = copy.deepcopy(pocket)
        broken["sha256"] = "0" * 64
        self.assertFalse(st43.verify(broken))

    def test_st44_bound_to_st43(self):
        pocket = st43.genesis()
        state = st44.genesis(pocket)
        self.assertTrue(st44.verify(state, pocket))
        next_state = st44.step(state, pocket)
        self.assertTrue(st44.verify(next_state, pocket))
        changed_pocket = st43.append(pocket, st43.pocket.pocket_record("Sample", [1], "Test"))
        self.assertFalse(st44.verify(next_state, changed_pocket))

    def test_st47_native_envelope(self):
        state = st47.initial()
        self.assertTrue(st47.verify(state))
        inspected, receipt = st47.advance(state, 0, "inspect", {})
        self.assertEqual(inspected, state)
        self.assertTrue(st47.verify(inspected))
        bad = copy.deepcopy(state)
        bad["revision"] = 1
        self.assertFalse(st47.verify(bad))

    def test_no_interchangeable_state_schema(self):
        self.assertFalse(st38.verify(st43.genesis()))
        self.assertFalse(st43.verify(st38.genesis("@@@SKKS", 10)))
        self.assertFalse(st47.verify(st43.genesis()))

if __name__ == "__main__":
    unittest.main()
