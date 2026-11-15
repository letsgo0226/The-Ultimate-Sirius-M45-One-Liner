import unittest
from m45_st88 import G, D, transition

class TestM45ST88(unittest.TestCase):
    def test_roundtrip(self):
        for data in (b"", b"LOVE", bytes(range(256)), b"\\x00\\xff"):
            self.assertEqual(D(G(data)), data)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            D(257)
    def test_transition(self):
        for i in range(12):
            state = transition(i)
            self.assertEqual(state["step"], i)
            self.assertTrue(state["roundtrip"])
            self.assertGreaterEqual(state["uncertainty_bits"], 0)

if __name__ == "__main__":
    unittest.main()
