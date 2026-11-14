import unittest
from app import calculate, parse

class SKTests(unittest.TestCase):
    def test_nested_s_k(self):
        result = calculate("@@@SKKS", 20)
        self.assertEqual(result["trace"], ["@@@SKKS", "@@KS@KS", "S"])
        self.assertEqual(result["status"], "NORMAL")

    def test_root_k(self):
        self.assertEqual(calculate("@@KSK")["result"], "S")

    def test_budget(self):
        result = calculate("@@@SKKS", 0)
        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertEqual(result["steps"], 0)

    def test_invalid(self):
        for expression in ("", "@S", "X", "SK", "@@@"):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    calculate(expression)

    def test_parse(self):
        self.assertEqual(parse("@SK"), ("S", "K"))

if __name__ == "__main__":
    unittest.main()
