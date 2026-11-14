import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("sk_tape", Path(__file__).with_name("sk_tape.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestSKTape(unittest.TestCase):
    def test_encoding(self):
        for s in ["S", "K", "@SK", "@@@SKKS"]:
            self.assertEqual(m.tape_decode(m.tape_encode(s)), s)

    def test_reduction(self):
        start = {"tape": m.tape_encode("@@@SKKS"), "steps": 0}
        end, record = m.advance(start, 30)
        self.assertEqual(m.tape_decode(end["tape"]), "S")
        self.assertEqual(end["steps"], 2)
        self.assertEqual(record["status"], "NORMAL")
        self.assertEqual(m.replay(start, [record]), end)

    def test_pause_resume(self):
        start = {"tape": m.tape_encode("@@@SKKS"), "steps": 0}
        first, a = m.advance(start, 1)
        self.assertEqual(a["status"], "PAUSED")
        last, b = m.advance(first, 1)
        self.assertEqual(m.tape_decode(last["tape"]), "S")
        self.assertEqual(m.replay(start, [a, b]), last)

    def test_tamper_rejected(self):
        start = {"tape": m.tape_encode("@@@SKKS"), "steps": 0}
        _, record = m.advance(start, 2)
        record["trace"][0]["after"] = "K"
        with self.assertRaises(ValueError):
            m.replay(start, [record])

    def test_invalid_tape(self):
        for s in ["", "@S", "SK", "X"]:
            with self.assertRaises(ValueError):
                m.tape_encode(s)
        with self.assertRaises(ValueError):
            m.tape_decode([3])

if __name__ == "__main__":
    unittest.main()
