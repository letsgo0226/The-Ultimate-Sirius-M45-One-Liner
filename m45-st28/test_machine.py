import importlib.util
import json
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name("machine.py")
spec = importlib.util.spec_from_file_location("m45_machine", MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestMachine(unittest.TestCase):
    def test_successor(self):
        for n in range(20):
            cert = m.run("1" * n, 100)
            self.assertEqual(cert["status"], "HALTED")
            self.assertEqual("".join(cert["snapshot"]["cells"].values()), "1" * (n + 1))
            self.assertTrue(m.verify(cert))

    def test_pause_and_resume(self):
        first = m.run("11111", 2)
        self.assertEqual(first["status"], "PAUSED")
        second = m.run("", 100, first["snapshot"])
        self.assertEqual(second["status"], "HALTED")
        self.assertEqual("".join(second["snapshot"]["cells"].values()), "111111")

    def test_tamper(self):
        cert = m.run("11")
        cert["trace"][0]["write"] = "_"
        self.assertFalse(m.verify(cert))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            m.run("SK")

if __name__ == "__main__":
    unittest.main()
