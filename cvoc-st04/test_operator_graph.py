import importlib.util
from pathlib import Path
import unittest
from operator_graph import ContractError, OPERATORS, validate_chain, verify_st43_st44_binding

ROOT = Path(__file__).resolve().parents[1]
def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

st43 = load("cvoc_st04_st43", "m45-st43/persistent_pocket.py")
st44 = load("cvoc_st04_st44", "m45-st44/continuity.py")

class GraphTests(unittest.TestCase):
    def test_native_operator_types(self):
        for name, op in OPERATORS.items():
            self.assertEqual(validate_chain([name], op.input_type), op.output_type)
    def test_reject_cross_machine_conversion(self):
        with self.assertRaises(ContractError):
            validate_chain(["st30.verify", "st38.verify"], "ST30Tape")
    def test_reject_fictional_unimplemented_composition(self):
        with self.assertRaises(ContractError):
            validate_chain(["st43.verify", "st44.verify"], "ST43Pocket")
    def test_reject_unknown_operator(self):
        with self.assertRaises(ContractError):
            validate_chain(["arbitrary.exec"], "RawBytes")
    def test_native_st43_st44_binding(self):
        pocket = st43.genesis()
        state = st44.genesis(pocket)
        self.assertTrue(verify_st43_st44_binding(st43, st44, pocket, state))
        updated = st43.append(pocket, st43.pocket.pocket_record("Sample", [1], "Test"))
        self.assertFalse(verify_st43_st44_binding(st43, st44, updated, state))
    def test_all_edges_read_only(self):
        self.assertTrue(all(not op.writes for op in OPERATORS.values()))

if __name__ == "__main__":
    unittest.main()
