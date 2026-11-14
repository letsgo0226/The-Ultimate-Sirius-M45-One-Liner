import importlib.util
import pathlib
import unittest

path = pathlib.Path(__file__).with_name("self_assignment.py")
spec = importlib.util.spec_from_file_location("st86_self_assignment", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestSelfAssignment(unittest.TestCase):
    def test_owner_ready(self):
        r = mod.decide("letsgo0226", "letsgo0226", False)
        self.assertTrue(r["eligible"])
        self.assertEqual(r["assignee"], "letsgo0226")
        self.assertFalse(r["review_approval_granted"])
        self.assertFalse(r["merge_permitted"])
        self.assertFalse(r["execution_permitted"])
        self.assertTrue(r["independent_review_required"])

    def test_draft(self):
        self.assertFalse(mod.decide("owner", "owner", True)["eligible"])

    def test_external_author(self):
        self.assertIsNone(mod.decide("owner", "other", False)["assignee"])

    def test_merged(self):
        self.assertFalse(mod.decide("owner", "owner", False, True)["eligible"])

    def test_invalid(self):
        for value in ("", " owner ", None):
            with self.assertRaises(ValueError):
                mod.decide(value, "owner", False)
        with self.assertRaises(ValueError):
            mod.decide("owner", "owner", 0)

if __name__ == "__main__":
    unittest.main()
